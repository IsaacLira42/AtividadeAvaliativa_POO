

class Categoria:
    def __init__(self, id: int, descricao: str) -> None:
        self.id = id
        self.descricao = descricao

    def __str__(self) -> str:
        return f"{self.id} - {self.descricao}"