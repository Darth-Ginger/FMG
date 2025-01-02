from datetime import datetime
from pytz import timezone
from typing import Any, Dict, Optional
from loguru import logger
import yaml, os, sys, threading

class ConfigAble:
    
    _instance = None
    _lock = threading.Lock() # Thread-safe singleton
    
    DEFAULT_CONFIG_PATH = 'config.yaml'
    DEFAULT_CONFIG: Dict[str, Any] = {
        'Logger': {
            'log_level': 'INFO',
            'log_file': None,
            'rotation': '10 MB',
            'retention': '30 days',
            'compression': None,
            'timezone': 'UTC',
            'clock_style': '12'
        }
    }
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ConfigAble, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, config_path=None):
        if not hasattr(self, '_initialized'):
            self._initialized = True # Ensure initialization only occurs once
            self.config_path = config_path
            if self.config_path is None:
                self.config_path = self.DEFAULT_CONFIG_PATH
            self.config: Dict[str, Any] = self.load_config()
            self._configure_logger()
            

    def load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path) or os.stat(self.config_path).st_size == 0:
            logger.warning(f"Configuration file not found or empty at {self.config_path}. Generating default configuration.")
            self._generate_default_config()
            return self.DEFAULT_CONFIG
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file) or {}
                return {**self.DEFAULT_CONFIG, **config} # Merge default and user configuration
        except FileNotFoundError:
            logger.warning(f"Configuration file not found at {self.config_path}. Using default settings.")
            return {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration: {e}")
            return self.DEFAULT_CONFIG
        except Exception as e:
            logger.error(f"Unexpected error loading configuration: {e}")
            return self.DEFAULT_CONFIG

    def _generate_default_config(self) -> None:
            """Generates a default configuration file."""
            try:
                with open(self.config_path, 'w') as file:
                    yaml.dump(self.DEFAULT_CONFIG, file, default_flow_style=False)
                    logger.info(f"Default configuration written to {self.config_path}.")
            except IOError as e:
                logger.error(f"Failed to write default configuration to {self.config_path}: {e}")

    def _configure_logger(self) -> None:
        """ Configures the Loguru logger based on the loaded configuration."""
        logger_config = self.get_config('Logger', {})
        log_level = logger_config.get('log_level', 'INFO')
        log_file = logger_config.get('log_file', None)
        rotation = logger_config.get('rotation', '10 MB')
        retention = logger_config.get('retention', '30 days')
        compression = logger_config.get('compression', None)
        timezone_str = logger_config.get('timezone', 'UTC')
        clock_style = logger_config.get('clock_style', '12')
        
        # Set timezone
        tz = timezone(timezone_str)
        
        # Set clock style
        if clock_style == '12':
            logger.configure(
                patcher=lambda record: record.update(
                    time=datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S %p')
                )
            )
        else:
            logger.configure(
                patcher=lambda record: record.update(
                    time=datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
                )
            )
        
        logger.remove() # Remove default logger
        logger.add(
            sys.stderr, 
            level=log_level,
            format="{time} | {level} | {message}",
            colorize=True
            ) # Console Logging
        
        if log_file:
            logger.add(
                log_file, 
                level=log_level, 
                rotation=rotation, 
                retention=retention, 
                compression=compression,
                format="{time} | {level} | {message}",
                )
            with open(log_file, 'a') as f:
                headers = [
                    f"Logger Initialized @ {datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S %p')}", 
                    f"Initializing {sys.argv[0]}"
                    ]
                
                max_len = max(len(header) for header in headers) + 20
                decorator = '=' * max_len
                centered_headers = [header.center(max_len, ' ') for header in headers]
                
                header = f"\n{decorator}\n{'\n'.join(centered_headers)}\n{decorator}\n"
                f.write(header)
            
        logger.success(f"Logger Initialized")
    
    def get_logger(self) -> Any:
        return logger
    
    def get_config(self, section: str, default: Optional[Any] = None) -> Any:
        """
        Retrieves a configuration option from the loaded configuration using dot notation.

        Args:
            section (str): The dot-separated configuration section to retrieve.
            default (Optional[Any], optional): The default value to return if not found. Defaults to None.

        Returns:
            Any: The configuration option value
        """
        keys = section.split('.')
        value = self.config
        for key in keys:
            value = value.get(key, default if key == keys[-1] else {})
            if value == {}:
                break
        return value

    
# Example usage
if __name__ == "__main__":
    # Instantiate ConfigAble
    config_manager = ConfigAble(config_path='config.yaml')

    # Get the logger
    log = config_manager.get_logger()

    # Access configurations
    # noise_gen_config = config_manager.get_config('NoiseGenerator', default={})

    # Log example message
    log.success("ConfigAble initialized successfully.")
    # log.debug(f"NoiseGenerator configuration: {noise_gen_config}")

