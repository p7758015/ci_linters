def test_create_recipe(client):
    payload = {
        "title": "Паста карбонара",
        "cook_time_minutes": 20,
        "ingredients": ["паста", "бекон", "яйцо"],
        "description": "Очень вкусная паста",
    }

    response = client.post("/recipes", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["title"] == payload["title"]
    assert data["cook_time_minutes"] == payload["cook_time_minutes"]
    assert data["views"] == 0
    assert data["ingredients"] == payload["ingredients"]
    assert data["description"] == payload["description"]

def test_list_recipes(client):
    client.post(
        "/recipes",
        json={
            "title": "Суп",
            "cook_time_minutes": 15,
            "ingredients": ["вода", "картошка"],
            "description": "Простой суп",
        },
    )

    response = client.get("/recipes")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    recipe = data[0]
    assert "id" in recipe
    assert "title" in recipe
    assert "cook_time_minutes" in recipe
    assert "views" in recipe

def test_get_recipe_increments_views(client):
    create_resp = client.post(
        "/recipes",
        json={
            "title": "Чай",
            "cook_time_minutes": 5,
            "ingredients": ["вода", "чай"],
            "description": "Просто чай",
        },
    )

    recipe_id = create_resp.json()["id"]

    resp1 = client.get(f"/recipes/{recipe_id}")
    assert resp1.status_code == 200
    assert resp1.json()["views"] == 1

    resp2 = client.get(f"/recipes/{recipe_id}")
    assert resp2.status_code == 200
    assert resp2.json()["views"] == 2
