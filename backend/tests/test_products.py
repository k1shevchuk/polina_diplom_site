from decimal import Decimal

from app.models.product import Product, ProductStatus


def test_catalog_lists_only_active_and_supports_filters(client, db_session):
    db_session.add_all(
        [
            Product(
                seller_id=1,
                title="Wooden Bowl",
                description="Handmade wooden bowl for kitchen and decor",
                price=Decimal("25.00"),
                status=ProductStatus.ACTIVE,
                tags=["wood"],
                materials=["oak"],
            ),
            Product(
                seller_id=1,
                title="Draft Item",
                description="Hidden draft",
                price=Decimal("30.00"),
                status=ProductStatus.DRAFT,
                tags=["test"],
                materials=["test"],
            ),
        ]
    )
    db_session.commit()

    response = client.get("/api/v1/catalog")
    assert response.status_code == 200
    data = response.json()
    assert data["meta"]["total"] == 1
    assert data["items"][0]["title"] == "Wooden Bowl"

    search = client.get("/api/v1/catalog?q=wooden")
    assert search.status_code == 200
    assert search.json()["meta"]["total"] == 1

    empty = client.get("/api/v1/catalog?min_price=100")
    assert empty.status_code == 200
    assert empty.json()["meta"]["total"] == 0
