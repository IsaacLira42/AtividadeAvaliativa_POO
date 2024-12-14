import os
import json

from typing import List, Optional

from models.cliente import Cliente


class Clientes:
    objetos = []  # Lista de Clientes

    @classmethod
    def inserir(cls, obj: Cliente) -> None:
        cls.abrir()

        id = 0
        for cliente in cls.objetos:
            if cliente.id > id:
                id = cliente.id
        obj.id = id + 1
        
        cls.objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls) -> List[Cliente]:
        cls.abrir()

        lista_clientes = cls.objetos

        if len(lista_clientes) == 0:
            return []
        else:
            return lista_clientes 
    
    @classmethod
    def listar_id(cls, id: int) -> Optional[Cliente]:
        cls.abrir()

        for cliente in cls.objetos:
            if cliente.id == id:
                return cliente
            
        # print("Cliente não encontado")
        return None

    @classmethod
    def atualizar(cls, obj: Cliente) -> None:
        cls.abrir()

        for cliente in cls.objetos:
            if cliente.id == obj.id:
                cliente.nome = obj.nome
                cliente.email = obj.email
                cliente.fone = obj.fone

                # print("Cliente Atualizado com sucesso!")

                cls.salvar()
                return
        # print("Cliente não encontrado")
        
    @classmethod
    def excluir(cls, id: int) -> None:
        cls.abrir()
        cls.objetos = [cliente for cliente in cls.objetos if cliente.id != id]
        cls.salvar()
        # print("Cliente removido com sucesso!")
            

    ############ Outros métodos ############################
    @classmethod
    def abrir(cls) -> None:
        if not os.path.exists("Clientes.json"):
            with open("Clientes.json", mode="w") as arquivo:
                json.dump([], arquivo)
        
        with open("Clientes.json", mode="r") as arquivo:
            cls.objetos = [Cliente(**obj) for obj in json.load(arquivo)]

    @classmethod
    def salvar(cls) -> None:
        with open("Clientes.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars)