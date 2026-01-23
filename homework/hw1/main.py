from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Recipe Book API",
    description=(
        "API кулинарной книги. "
        "Позволяет создавать рецепты, получать список популярных рецептов "
        "и просматривать детальную информацию."
    ),
    version="1.0.0",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/recipes",
    response_model=schemas.RecipeDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый рецепт",
    tags=["recipes"],
)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = models.Recipe(
        title=recipe.title,
        cook_time_minutes=recipe.cook_time_minutes,
        views=0,
        ingredients="|".join(recipe.ingredients),
        description=recipe.description,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return schemas.RecipeDetail(
        id=db_recipe.id,
        title=db_recipe.title,
        cook_time_minutes=db_recipe.cook_time_minutes,
        views=db_recipe.views,
        ingredients=db_recipe.ingredients.split("|"),
        description=db_recipe.description,
    )


@app.get(
    "/recipes",
    response_model=List[schemas.RecipeListItem],
    summary="Получить список рецептов",
    tags=["recipes"],
)
def list_recipes(db: Session = Depends(get_db)):
    recipes = (
        db.query(models.Recipe)
        .order_by(
            models.Recipe.views.desc(),
            models.Recipe.cook_time_minutes.asc(),
        )
        .all()
    )
    return [
        schemas.RecipeListItem(
            id=r.id,
            title=r.title,
            cook_time_minutes=r.cook_time_minutes,
            views=r.views,
        )
        for r in recipes
    ]


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeDetail,
    summary="Получить детальный рецепт",
    tags=["recipes"],
)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рецепт не найден",
        )

    recipe.views += 1
    db.commit()
    db.refresh(recipe)

    return schemas.RecipeDetail(
        id=recipe.id,
        title=recipe.title,
        cook_time_minutes=recipe.cook_time_minutes,
        views=recipe.views,
        ingredients=recipe.ingredients.split("|"),
        description=recipe.description,
    )
