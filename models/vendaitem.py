
class VendaItem:
    def __init__(self, id: int, qtd: int, preco: float, idvenda: int, idproduto: int) -> None:
        self.id = id
        self.qtd = qtd
        self.preco = preco
        self.idvenda = idvenda
        self.idproduto = idproduto

    def __str__(self) -> str:
        return f"{self.id} - {self.qtd} - {self.preco} - {self.idvenda} - {self.idproduto}"