"""A model containing category-related models."""

from pydantic import BaseModel, ConfigDict

class CategoryDTO(BaseModel):
    """A model representing DTO for category data."""

    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )
