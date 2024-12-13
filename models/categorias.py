import os
import json
from typing import List, Optional
from .categoria import Categoria

class Categorias:
    objetos = []  # Lista de Categorias

    @classmethod
    def inserir(cls, obj: Categoria) -> None:
        cls.abrir()

        id = 0
        for categoria in cls.objetos:
            if categoria.id > id:
                id = categoria.id
        obj.id = id + 1

        cls.objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls) -> List[Categoria]:
        cls.abrir()

        lista_categorias = cls.objetos

        if len(lista_categorias) == 0:
            return []
        else:
            return lista_categorias

    @classmethod
    def listar_id(cls, id: int) -> Optional[Categoria]:
        cls.abrir()

        for categoria in cls.objetos:
            if categoria.id == id:
                return categoria

        print("Categoria não encontrada")
        return None

    @classmethod
    def atualizar(cls, obj: Categoria) -> None:
        cls.abrir()

        for categoria in cls.objetos:
            if categoria.id == obj.id:
                categoria.descricao = obj.descricao

                print("Categoria atualizada com sucesso!")

                cls.salvar()
                return
        print("Categoria não encontrada")

    @classmethod
    def excluir(cls, id: int) -> None:
        cls.abrir()
        cls.objetos = [categoria for categoria in cls.objetos if categoria.id != id]
        cls.salvar()
        print("Categoria removida com sucesso!")

    ############ Outros métodos ############################
    @classmethod
    def abrir(cls) -> None:
        if not os.path.exists("Categorias.json"):
            with open("Categorias.json", mode="w") as arquivo:
                json.dump([], arquivo)

        with open("Categorias.json", mode="r") as arquivo:
            cls.objetos = [Categoria(**obj) for obj in json.load(arquivo)]

    @classmethod
    def salvar(cls) -> None:
        with open("Categorias.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars)
