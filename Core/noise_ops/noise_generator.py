from typing import List, Dict, Any, Type
import numpy as np

from Utilities import configAble

class NoiseGenerator:
    """
    A class to manage noise generation operations dynamically via a dictionary.
    """
    
    config_manager = configAble.ConfigAble(config_path='config.yaml')
    log = config_manager.get_logger()
    
    noise_ops: Dict[str, Type[callable]] = {}
    num_processes: int = config_manager.get_config('NoiseGenerator.num_processes', default=1)
    
    @classmethod
    def register_op(cls, name: str, op: Type[callable]):
        """
        Register a new noise operation.
        
        Args:
            name (str)            : The name of the operation. (e.g., "perlin")
            op   (Type[callable]) : The operation class.
        """
        cls.noise_ops[name] = op
        
    @classmethod
    def deregister_op(cls, name: str):
        """
        Deregister a noise operation.
        
        Args:
            name (str): The name of the operation to deregister.
        """
        if name in cls.noise_ops:
            del cls.noise_ops[name]
            
    @classmethod
    def list_ops(cls) -> List[str]:
        """
        Lists all registered noise operations.
        
        Returns:
            List[str]: A list of registered noise operations.
        """
        return list(cls.noise_ops.keys())
        
    @classmethod
    def execute_op(
            cls, 
            op: str, 
            map_data: np.ndarray,
            settings: Dict[str, Any] = None, 
            **kwargs
        ) -> np.ndarray:
        """
        Executes the specified noise operation.

        Args:
            op (str): The name of the operation to execute.
            map_data (np.ndarray): The map data to use for the operation.
            settings (Dict[str, Any], optional): The settings to use for the operation. Defaults to None.

        Returns:
            Transformed 2D numpy array.
        """
        if op not in cls.noise_ops:
            cls.log.error(f"Unknown noise operation: {op}")
            raise ValueError(f"Unknown noise operation: {op}")
        
        cls.log.info(f"Executing noise operation: {op}")
        return cls.noise_ops[op](map_data, settings, **kwargs)
    
    