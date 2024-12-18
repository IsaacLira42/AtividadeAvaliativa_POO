

class Produto:
    def __init__(self, id: int, descricao: str, preco: float, estoque: int, idCategoria: int) -> None:
        self.id = id
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.idCategoria = idCategoria
    
    def __str__(self) -> str:
        return f"{self.id} - {self.descricao} - {self.preco:.2f} - {self.estoque} - {self.idCategoria}"