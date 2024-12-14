
class Cliente:
    def __init__(self, id: int, nome: str, email: str, fone: str, senha: str) -> None:
        self.id = id
        self.nome = nome
        self.email = email
        self.fone = fone
        self.senha = senha
        
    def __str__(self) -> str:
        return f"{self.id} - {self.nome} - {self.email} - {self.fone}"