import os
import json
from typing import List, Optional
from .produto import Produto

class Produtos:
    objetos = []  # Lista de Produtos

    @classmethod
    def inserir(cls, obj: Produto) -> None:
        cls.abrir()

        id = 0
        for produto in cls.objetos:
            if produto.id > id:
                id = produto.id
        obj.id = id + 1

        cls.objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls) -> List[Produto]:
        cls.abrir()

        lista_produtos = cls.objetos

        if len(lista_produtos) == 0:
            return []
        else:
            return lista_produtos

    @classmethod
    def listar_id(cls, id: int) -> Optional[Produto]:
        cls.abrir()

        for produto in cls.objetos:
            if produto.id == id:
                return produto

        print("Produto não encontrado")
        return None

    @classmethod
    def atualizar(cls, obj: Produto) -> None:
        cls.abrir()

        for produto in cls.objetos:
            if produto.id == obj.id:
                produto.descricao = obj.descricao
                produto.preco = obj.preco
                produto.estoque = obj.estoque
                produto.idCategoria = obj.idCategoria

                print("Produto atualizado com sucesso!")

                cls.salvar()
                return
        print("Produto não encontrado")

    @classmethod
    def excluir(cls, id: int) -> None:
        cls.abrir()
        cls.objetos = [produto for produto in cls.objetos if produto.id != id]
        cls.salvar()
        print("Produto removido com sucesso!")

    ############ Outros métodos ############################
    @classmethod
    def abrir(cls) -> None:
        if not os.path.exists("Produtos.json"):
            with open("Produtos.json", mode="w") as arquivo:
                json.dump([], arquivo)

        with open("Produtos.json", mode="r") as arquivo:
            cls.objetos = [Produto(**obj) for obj in json.load(arquivo)]

    @classmethod
    def salvar(cls) -> None:
        with open("Produtos.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars)
