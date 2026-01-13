"""A model containing company subcategory-related models."""

from pydantic import BaseModel, ConfigDict

class SubcategoryDTO(BaseModel):
    """A model representing DTO for company subcategory data."""

    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

