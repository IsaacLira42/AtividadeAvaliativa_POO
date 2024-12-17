import os
import json
from typing import List, Optional
from datetime import datetime
from .venda import Venda

class Vendas:
    objetos = []  # Lista de Vendas

    @classmethod
    def inserir(cls, obj: Venda) -> None:
        cls.abrir()

        id = 0
        for venda in cls.objetos:
            if venda.id > id:
                id = venda.id
        obj.id = id + 1

        cls.objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls) -> List[Venda]:
        cls.abrir()

        lista_vendas = cls.objetos

        if len(lista_vendas) == 0:
            return []
        else:
            return lista_vendas

    @classmethod
    def listar_id(cls, id: int) -> Optional[Venda]:
        cls.abrir()

        for venda in cls.objetos:
            if venda.id == id:
                return venda

        print("Venda não encontrada")
        return None

    @classmethod
    def atualizar(cls, obj: Venda) -> None:
        cls.abrir()

        for venda in cls.objetos:
            if venda.id == obj.id:
                venda.data = obj.data
                venda.carrinho = obj.carrinho
                venda.total = obj.total
                venda.idCliente = obj.idCliente

                #print("Venda atualizada com sucesso!")

                cls.salvar()
                return
        #print("Venda não encontrada")

    @classmethod
    def excluir(cls, id: int) -> None:
        cls.abrir()
        cls.objetos = [venda for venda in cls.objetos if venda.id != id]
        cls.salvar()
        #print("Venda removida com sucesso!")

    ############ Outros métodos ############################
    @classmethod
    def abrir(cls) -> None:
        if not os.path.exists("Vendas.json"):
            with open("Vendas.json", mode="w") as arquivo:
                json.dump([], arquivo)

        with open("Vendas.json", mode="r") as arquivo:
            vendas_data = json.load(arquivo)
            cls.objetos = []
            for venda in vendas_data:
                venda['data'] = datetime.fromisoformat(venda['data'])  # Converte a string para datetime
                cls.objetos.append(Venda(**venda))

    @classmethod
    def salvar(cls) -> None:
        vendas_data = []
        for venda in cls.objetos:
            venda_data = vars(venda)
            venda_data['data'] = venda_data['data'].isoformat()  # Converte datetime para string
            vendas_data.append(venda_data)

        with open("Vendas.json", mode="w") as arquivo:
            json.dump(vendas_data, arquivo, indent=4)
