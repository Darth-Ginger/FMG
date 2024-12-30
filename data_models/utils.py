from pydantic import BaseModel

class Utils:
    """Static class for utility functions."""

    @staticmethod
    def serialize_model_to_dict(model: BaseModel) -> dict:
        """Convert a Pydantic model to a dictionary."""
        return model.model_dump()

    @staticmethod
    def validate_and_load(data: dict, model: BaseModel) -> BaseModel:
        """Validate raw data against a Pydantic model."""
        return model.model_validate(data)
