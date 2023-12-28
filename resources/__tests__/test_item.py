def test_create_item_in_store(client, fresh_jwt, created_store_id):
    response = client.post(
        "/item",
        json={"name": "Test Item", "price": 10.5, "store_id": created_store_id},
        headers={"Authorization": f"Bearer {fresh_jwt}"},
    )

    assert response.status_code == 201
    assert response.json["name"] == "Test Item"
    assert response.json["price"] == 10.5
    assert response.json["store"] == {"id": created_store_id, "name": "Test Store"}


def test_create_item_with_store_id_not_found(client, fresh_jwt):
    # Note that this will fail if foreign key constraints are enabled.
    response = client.post(
        "/item",
        json={"name": "Test Item", "price": 10.5, "store_id": 1},
        headers={"Authorization": f"Bearer {fresh_jwt}"},
    )

    assert response.status_code == 201
    assert response.json["name"] == "Test Item"
    assert response.json["price"] == 10.5
    assert response.json["store"] is None


def test_create_item_with_unknown_data(client, fresh_jwt):
    response = client.post(
        "/item",
        json={
            "name": "Test Item",
            "price": 10.5,
            "store_id": 1,
            "unknown_field": "unknown",
        },
        headers={"Authorization": f"Bearer {fresh_jwt}"},
    )

    assert response.status_code == 422
    assert response.json["errors"]["json"]["unknown_field"] == ["Unknown field."]


def test_create_item_with_non_fresh_jwt(client, jwt):
    response = client.post(
        "/item",
        json={"name": "Test Item", "price": 10.5, "store_id": 1},
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert response.status_code == 401
    assert response.json == {
        "description": "The token is not fresh.",
        "error": "fresh_token_required",
    }


def test_delete_item(client, admin_jwt, created_item_id):
    response = client.delete(
        f"/item/{created_item_id}",
        headers={"Authorization": f"Bearer {admin_jwt}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Item deleted."


def test_delete_item_without_admin(client, jwt, created_item_id):
    response = client.delete(
        f"/item/{created_item_id}",
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert response.status_code == 401
    assert response.json["message"] == "Admin privilege required."


def test_update_item(client, jwt, created_item_id):
    response = client.put(
        f"/item/{created_item_id}",
        json={"name": "Test Item (updated)", "price": 12.5},
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert response.status_code == 200
    assert response.json["name"] == "Test Item (updated)"
    assert response.json["price"] == 12.5


def test_get_all_items(client, fresh_jwt, jwt):
    response = client.post(
        "/item",
        json={"name": "Test Item", "price": 10.5, "store_id": 1},
        headers={"Authorization": f"Bearer {fresh_jwt}"},
    )
    response = client.post(
        "/item",
        json={"name": "Test Item 2", "price": 10.5, "store_id": 1},
        headers={"Authorization": f"Bearer {fresh_jwt}"},
    )

    response = client.get(
        "/item",
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["name"] == "Test Item"
    assert response.json[0]["price"] == 10.5
    assert response.json[1]["name"] == "Test Item 2"


def test_get_all_items_empty(client, jwt):
    response = client.get(
        "/item",
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert response.status_code == 200
    assert len(response.json) == 0


def test_get_item_details(client, jwt, created_item_id, created_store_id):
    response = client.get(
        f"/item/{created_item_id}",
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert response.status_code == 200
    assert response.json["name"] == "Test Item"
    assert response.json["price"] == 10.5
    assert response.json["store"] == {"id": created_store_id, "name": "Test Store"}


def test_get_item_details_with_tag(client, jwt, created_item_id, created_tag_id):
    client.post(f"/item/{created_item_id}/tag/{created_tag_id}")
    response = client.get(
        f"/item/{created_item_id}",
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert response.status_code == 200
    assert response.json["name"] == "Test Item"
    assert response.json["price"] == 10.5
    assert response.json["tags"] == [{"id": created_tag_id, "name": "Test Tag"}]


def test_get_item_detail_not_found(client, jwt):
    response = client.get(
        "/item/1",
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}
