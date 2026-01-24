from typing import Generator, List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import asc, desc
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


def get_db() -> Generator[Session, None, None]:
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
def create_recipe(
    recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> schemas.RecipeDetail:
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
        id=int(db_recipe.id),
        title=str(db_recipe.title),
        cook_time_minutes=int(db_recipe.cook_time_minutes),
        views=int(db_recipe.views),
        ingredients=db_recipe.ingredients.split("|"),
        description=str(db_recipe.description),
    )


@app.get(
    "/recipes",
    response_model=List[schemas.RecipeListItem],
    summary="Получить список рецептов",
    tags=["recipes"],
)
def list_recipes(
    db: Session = Depends(get_db),  # noqa: B008
) -> List[schemas.RecipeListItem]:
    query = db.query(models.Recipe)
    recipes = query.order_by(
        desc(models.Recipe.views),
        asc(models.Recipe.cook_time_minutes),
    ).all()

    return [
        schemas.RecipeListItem(
            id=int(r.id),
            title=str(r.title),
            cook_time_minutes=int(r.cook_time_minutes),
            views=int(r.views),
        )
        for r in recipes
    ]


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeDetail,
    summary="Получить детальный рецепт",
    tags=["recipes"],
)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),  # noqa: B008
) -> schemas.RecipeDetail:
    recipe: models.Recipe | None = (
        db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    )
    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рецепт не найден",
        )

    recipe.views += 1  # type: ignore[assignment]
    db.commit()
    db.refresh(recipe)

    return schemas.RecipeDetail(
        id=int(recipe.id),
        title=str(recipe.title),
        cook_time_minutes=int(recipe.cook_time_minutes),
        views=int(recipe.views),
        ingredients=recipe.ingredients.split("|"),
        description=str(recipe.description),
    )