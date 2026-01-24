from typing import List

from pydantic import BaseModel, Field


class RecipeBase(BaseModel):
    title: str = Field(..., description="Название блюда")
    cook_time_minutes: int = Field(
        ..., ge=1, description="Время приготовления в минутах"
    )
    ingredients: List[str] = Field(..., description="Список ингредиентов")
    description: str = Field(..., description="Текстовое описание рецепта")


class RecipeCreate(RecipeBase):
    pass


class RecipeListItem(BaseModel):
    id: int
    title: str
    cook_time_minutes: int
    views: int

    class Config:
        orm_mode = True


class RecipeDetail(RecipeBase):
    id: int
    views: int

    class Config:
        orm_mode = True
