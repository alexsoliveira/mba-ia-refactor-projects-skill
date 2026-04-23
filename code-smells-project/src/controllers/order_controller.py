from src.models.order_model import get_all_orders, get_orders_by_user, get_sales_report
from src.services.order_service import create_order_workflow, update_order_status_workflow
from src.utils.validators import validate_order_payload, validate_order_status


def create_order_response(data: dict | None) -> tuple[dict, int]:
    payload = validate_order_payload(data)
    result = create_order_workflow(payload["usuario_id"], payload["itens"])
    if "erro" in result:
        return {"erro": result["erro"], "sucesso": False}, 400

    return {
        "dados": {"pedido_id": result["pedido_id"], "total": result["total"]},
        "sucesso": True,
        "mensagem": "Pedido criado com sucesso",
    }, 201


def get_user_orders_response(user_id: int) -> tuple[dict, int]:
    return {"dados": get_orders_by_user(user_id), "sucesso": True}, 200


def get_all_orders_response() -> tuple[dict, int]:
    return {"dados": get_all_orders(), "sucesso": True}, 200


def update_order_status_response(order_id: int, data: dict | None) -> tuple[dict, int]:
    status = validate_order_status((data or {}).get("status", ""))
    update_order_status_workflow(order_id, status)
    return {"sucesso": True, "mensagem": "Status atualizado"}, 200


def get_sales_report_response() -> tuple[dict, int]:
    return {"dados": get_sales_report(), "sucesso": True}, 200

