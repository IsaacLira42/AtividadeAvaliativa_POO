import datetime

class Venda:
    def __init__(self, id: int, data: datetime, carrinho: bool, total: float, idCliente: int) -> None:
        self.id = id
        self.data = data
        self.carrinho = carrinho
        self.total = total
        self.idCliente = idCliente

    def __str__(self) -> str:
        return f"{self.id} - {self.data} - {self.carrinho} - {self.total:.2f} - {self.idCliente}"
        