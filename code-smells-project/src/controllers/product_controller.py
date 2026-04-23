from src.models.product_model import (
    create_product,
    delete_product,
    get_all_products,
    get_product_by_id,
    search_products,
    update_product,
)
from src.utils.validators import validate_product_payload


def list_products_response() -> tuple[dict, int]:
    products = get_all_products()
    return {"dados": products, "sucesso": True}, 200


def get_product_response(product_id: int) -> tuple[dict, int]:
    product = get_product_by_id(product_id)
    if product:
        return {"dados": product, "sucesso": True}, 200
    return {"erro": "Produto não encontrado", "sucesso": False}, 404


def create_product_response(data: dict | None) -> tuple[dict, int]:
    payload = validate_product_payload(data)
    product_id = create_product(
        payload.nome,
        payload.descricao,
        payload.preco,
        payload.estoque,
        payload.categoria,
    )
    return {"dados": {"id": product_id}, "sucesso": True, "mensagem": "Produto criado"}, 201


def update_product_response(product_id: int, data: dict | None) -> tuple[dict, int]:
    existing_product = get_product_by_id(product_id)
    if not existing_product:
        return {"erro": "Produto não encontrado"}, 404

    payload = validate_product_payload(data)
    update_product(
        product_id,
        payload.nome,
        payload.descricao,
        payload.preco,
        payload.estoque,
        payload.categoria,
    )
    return {"sucesso": True, "mensagem": "Produto atualizado"}, 200


def delete_product_response(product_id: int) -> tuple[dict, int]:
    product = get_product_by_id(product_id)
    if not product:
        return {"erro": "Produto não encontrado"}, 404
    delete_product(product_id)
    return {"sucesso": True, "mensagem": "Produto deletado"}, 200


def search_products_response(term: str, category: str | None, minimum_price: float | None, maximum_price: float | None) -> tuple[dict, int]:
    results = search_products(term, category, minimum_price, maximum_price)
    return {"dados": results, "total": len(results), "sucesso": True}, 200

