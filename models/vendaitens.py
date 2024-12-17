import os
import json
from typing import List, Optional

from .vendaitem import VendaItem

# Arquivo: venda_items.py
class VendaItens:
    objetos = []  # Lista de VendaItem

    @classmethod
    def inserir(cls, obj: VendaItem) -> None:
        cls.abrir()

        id = 0
        for item in cls.objetos:
            if item.id > id:
                id = item.id
        obj.id = id + 1

        cls.objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls) -> List[VendaItem]:
        cls.abrir()
        return cls.objetos if cls.objetos else []

    @classmethod
    def listar_id(cls, id: int) -> Optional[VendaItem]:
        cls.abrir()

        for item in cls.objetos:
            if item.id == id:
                return item

        print("Item não encontrado")
        return None

    @classmethod
    def atualizar(cls, obj: VendaItem) -> None:
        cls.abrir()

        for item in cls.objetos:
            if item.id == obj.id:
                item.qtd = obj.qtd
                item.preco = obj.preco
                item.idvenda = obj.idvenda
                item.idproduto = obj.idproduto

                #print("Item atualizado com sucesso!")

                cls.salvar()
                return
        #print("Item não encontrado")

    @classmethod
    def excluir(cls, id: int) -> None:
        cls.abrir()
        cls.objetos = [item for item in cls.objetos if item.id != id]
        cls.salvar()
        #print("Item removido com sucesso!")

    ############ Outros métodos ############################
    @classmethod
    def abrir(cls) -> None:
        if not os.path.exists("VendaItems.json"):
            with open("VendaItems.json", mode="w") as arquivo:
                json.dump([], arquivo)

        with open("VendaItems.json", mode="r") as arquivo:
            cls.objetos = [VendaItem(**obj) for obj in json.load(arquivo)]

    @classmethod
    def salvar(cls) -> None:
        with open("VendaItems.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars)