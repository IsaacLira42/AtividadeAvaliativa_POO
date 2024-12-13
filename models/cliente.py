
class Cliente:
    def __init__(self, id: int, nome: str, email: str, fone: str) -> None:
        self.id = id
        self.nome = nome
        self.email = email
        self.fone = fone
    def __str__(self) -> str:
        return f"{self.id} - {self.nome} - {self.email} - {self.fone}"