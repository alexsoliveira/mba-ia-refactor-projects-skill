from dataclasses import dataclass

from src.utils.constants import CATEGORIAS_VALIDAS, STATUS_PEDIDO_VALIDOS


class ValidationError(ValueError):
    pass


@dataclass(frozen=True)
class ProductPayload:
    nome: str
    descricao: str
    preco: float
    estoque: int
    categoria: str


def validate_product_payload(data: dict | None) -> ProductPayload:
    if not data:
        raise ValidationError("Dados inválidos")
    if "nome" not in data:
        raise ValidationError("Nome é obrigatório")
    if "preco" not in data:
        raise ValidationError("Preço é obrigatório")
    if "estoque" not in data:
        raise ValidationError("Estoque é obrigatório")

    nome = str(data["nome"]).strip()
    descricao = str(data.get("descricao", "")).strip()
    categoria = str(data.get("categoria", "geral")).strip()

    try:
        preco = float(data["preco"])
    except (TypeError, ValueError) as error:
        raise ValidationError("Preço inválido") from error

    try:
        estoque = int(data["estoque"])
    except (TypeError, ValueError) as error:
        raise ValidationError("Estoque inválido") from error

    if preco < 0:
        raise ValidationError("Preço não pode ser negativo")
    if estoque < 0:
        raise ValidationError("Estoque não pode ser negativo")
    if len(nome) < 2:
        raise ValidationError("Nome muito curto")
    if len(nome) > 200:
        raise ValidationError("Nome muito longo")
    if categoria not in CATEGORIAS_VALIDAS:
        raise ValidationError(f"Categoria inválida. Válidas: {list(CATEGORIAS_VALIDAS)}")

    return ProductPayload(
        nome=nome,
        descricao=descricao,
        preco=preco,
        estoque=estoque,
        categoria=categoria,
    )


def validate_user_payload(data: dict | None) -> dict:
    if not data:
        raise ValidationError("Dados inválidos")

    nome = str(data.get("nome", "")).strip()
    email = str(data.get("email", "")).strip()
    senha = str(data.get("senha", "")).strip()
    if not nome or not email or not senha:
        raise ValidationError("Nome, email e senha são obrigatórios")
    return {"nome": nome, "email": email, "senha": senha}


def validate_login_payload(data: dict | None) -> dict:
    if not data:
        raise ValidationError("Dados inválidos")

    email = str(data.get("email", "")).strip()
    senha = str(data.get("senha", "")).strip()
    if not email or not senha:
        raise ValidationError("Email e senha são obrigatórios")
    return {"email": email, "senha": senha}


def validate_order_payload(data: dict | None) -> dict:
    if not data:
        raise ValidationError("Dados inválidos")

    usuario_id = data.get("usuario_id")
    itens = data.get("itens", [])
    if not usuario_id:
        raise ValidationError("Usuario ID é obrigatório")
    if not itens:
        raise ValidationError("Pedido deve ter pelo menos 1 item")
    return {"usuario_id": usuario_id, "itens": itens}


def validate_order_status(status: str) -> str:
    if status not in STATUS_PEDIDO_VALIDOS:
        raise ValidationError("Status inválido")
    return status

