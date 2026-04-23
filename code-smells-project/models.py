from src.models.order_model import (
    create_order as criar_pedido,
    get_all_orders as get_todos_pedidos,
    get_orders_by_user as get_pedidos_usuario,
    get_sales_report as relatorio_vendas,
    update_order_status as atualizar_status_pedido,
)
from src.models.product_model import (
    create_product as criar_produto,
    delete_product as deletar_produto,
    get_all_products as get_todos_produtos,
    get_product_by_id as get_produto_por_id,
    search_products as buscar_produtos,
    update_product as atualizar_produto,
)
from src.models.user_model import (
    create_user as criar_usuario,
    get_all_users as get_todos_usuarios,
    get_user_by_id as get_usuario_por_id,
    login_user as login_usuario,
)

__all__ = [
    "atualizar_produto",
    "atualizar_status_pedido",
    "buscar_produtos",
    "criar_pedido",
    "criar_produto",
    "criar_usuario",
    "deletar_produto",
    "get_pedidos_usuario",
    "get_produto_por_id",
    "get_todos_pedidos",
    "get_todos_produtos",
    "get_todos_usuarios",
    "get_usuario_por_id",
    "login_usuario",
    "relatorio_vendas",
]
