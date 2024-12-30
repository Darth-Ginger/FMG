import os
import time
from loguru import logger
import sys
import yaml
from singleton_decorator import singleton



class LoguruWrapper:
    """
    A wrapper around Loguru for flexible logging configuration and usage.
    Centralized logging setup supporting global and class-specific configurations.
    """
    
    _instance = None
    DEFAULT_CONFIG_PATH = '../config.yaml'
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoguruWrapper, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_path=None, conf=None):
        if not hasattr(self, '_initialized'):
            self._initialized = True  # Prevent reinitialization
            if config_path is None and conf is None:
                config_path = self.DEFAULT_CONFIG_PATH
            if conf is None:
                self.config = self._load_config(config_path)
            else:
                self.config = conf
            self.global_config = self.config.get('Logger', {}).get('Global', {})
            self._configure_logger()

    def _load_config(self, path) -> dict:
        """Loads the YAML configuration file."""
        try:
            with open(path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.warning(f"Configuration file not found at {path}. Using default settings.")
            return {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration: {e}")
            return {}

    def _configure_logger(self) -> None:
        """Configures the Loguru logger based on the loaded configuration."""
        logger.remove()  # Remove default Loguru handler

        # Default global configuration
        global_log_level       = self.global_config.get('log_level', 'INFO')
        global_log_file        = self.global_config.get('log_file', None)
        # if global_log_file is not None:
            # global_log_file    = os.path.join(os.getcwd(), self.global_config.get('log_file', None))
        global_log_rotation    = self.global_config.get('log_rotation', '10 MB')
        global_log_retention   = self.global_config.get('log_retention', '30 days')
        global_log_compression = self.global_config.get('log_compression', None)

        # Configure global logging
        if global_log_file is not None:
            logger.add(
                global_log_file,
                level=global_log_level,
                rotation=global_log_rotation,
                retention=global_log_retention,
                compression=global_log_compression
            )
            if not os.path.exists(global_log_file):
                with open(global_log_file, 'w') as f:
                    f.write(f"\n{"*" * 60}\n New Log File Created at {time.strftime('%Y-%m-%d %H:%M:%S')} \n{"*" * 60}\n")
                logger.warning(f"Log file not found at {global_log_file}. Creating new file.")
                
            with open(global_log_file, 'a') as f:
                f.write(f"\n{"*" * 10} Log running at {time.strftime('%Y-%m-%d %H:%M:%S')} {"*" * 10}\n")

        # Configure console logging
        logger.add(sys.stderr, level=global_log_level)
        

    @staticmethod
    def get_logger():
        """Returns the Loguru logger instance."""
        return logger

    @staticmethod
    def log_exception(exc):
        """Logs an exception with traceback."""
        logger.exception(f"Exception occurred: {exc}")

    @staticmethod
    def log_message(level: str, message: str):
        """Logs a message at the specified log level."""
        logger.log(level, message)

    @staticmethod
    def info(message):
        """Logs an INFO message."""
        logger.info(message)
        
    @staticmethod
    def debug(message):
        """Logs a DEBUG message."""
        logger.debug(message)
        
    @staticmethod
    def log(level="INFO", input=False, output=False, exception=True):
        """
        A decorator to log specified events (inputs, outputs, exceptions) for a function.
        
        :param level: Log level for the messages (default: INFO).
        :param input: Whether to log function inputs (default: False).
        :param output: Whether to log function outputs (default: False).
        :param exception: Whether to log exceptions (default: True).
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                if input:
                    logger.log(level, f"Entering {func.__name__} with args={args}, kwargs={kwargs}")
                try:
                    result = func(*args, **kwargs)
                    if output:
                        logger.log(level, f"Exiting {func.__name__} with result={result}")
                    return result
                except Exception as e:
                    if exception:
                        logger.exception(f"Exception in {func.__name__}: {e}")
                    raise
            return wrapper
        return decorator

# Example usage
if __name__ == "__main__":
    log_wrapper = LoguruWrapper()
    log = LoguruWrapper.get_logger()

    @LoguruWrapper.log(level="DEBUG", input=True, output=True, exception=True)
    def example_function(x, y):
        return x + y

    log.info("This is an info message.")
    try:
        example_function(5, 3)
    except Exception as e:
        log.error(f"Error occurred: {e}")
