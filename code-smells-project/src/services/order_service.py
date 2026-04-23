from src.models.order_model import create_order, update_order_status


def create_order_workflow(usuario_id: int, itens: list[dict]) -> dict:
    result = create_order(usuario_id, itens)
    if "erro" in result:
        return result

    order_id = result["pedido_id"]
    result["notificacoes"] = [
        f"ENVIANDO EMAIL: Pedido {order_id} criado para usuario {usuario_id}",
        "ENVIANDO SMS: Seu pedido foi recebido!",
        "ENVIANDO PUSH: Novo pedido recebido pelo sistema",
    ]
    return result


def update_order_status_workflow(order_id: int, new_status: str) -> list[str]:
    update_order_status(order_id, new_status)
    notifications: list[str] = []
    if new_status == "aprovado":
        notifications.append(f"NOTIFICAÇÃO: Pedido {order_id} foi aprovado! Preparar envio.")
    if new_status == "cancelado":
        notifications.append(f"NOTIFICAÇÃO: Pedido {order_id} cancelado. Devolver estoque.")
    return notifications

