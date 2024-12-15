import datetime
from typing import List, Optional

from models.cliente import Cliente
from models.clientes import Clientes
from models.categoria import Categoria
from models.categorias import Categorias
from models.produto import Produto
from models.produtos import Produtos
from models.venda import Venda
from models.vendas import Vendas
from models.vendaitem import VendaItem
from models.vendaitens import VendaItens

class View:
    ############ Métodos sobre Clientes ############
    @classmethod 
    def cliente_inserir(cls, nome: str, email:str, fone: str, senha: str) -> None:
        obj_cliente = Cliente(0, nome, email,fone, senha)
        Clientes.inserir(obj_cliente)
    @classmethod
    def cliente_listar(cls) -> List[Cliente]:
        return Clientes.listar()
    @classmethod
    def cliente_atualizar(cls, id: int, nome: str, email:str, fone: str, senha: str) -> None:
        obj_cliente = Cliente(id, nome, email,fone, senha)
        Clientes.atualizar(obj_cliente)
    @classmethod
    def cliente_excluir(cls, id: int) -> None:
        Clientes.excluir(id)
    # Métodos sobre Sessão ############
    @staticmethod
    def cliente_admin():
        # Verificar se o admin existe
        for c in Clientes.listar():
            if c.email == "admin": return None
        # se não existir, cria um admin com as credenciais padrão.
        View.cliente_inserir("admin", "admin", "(00) 0 0000-0000", "admin")    
    @staticmethod
    def cliente_autenticar(email, senha):
        for c in Clientes.listar():
            if c.email == email and c.senha == senha:
                return { "id" : c.id, "nome" : c.nome }
        return None  


    ############ Métodos sobre Categorias ############
    @classmethod
    def categoria_inserir(cls, descricao: str) -> None:
        obj_categoria = Categoria(0, descricao)
        Categorias.inserir(obj_categoria)
    @classmethod
    def categoria_listar(cls) -> List[Categoria]:
        return Categorias.listar()
    @classmethod
    def categoria_atualizar(cls, id: int, descricao: str) -> None:
        obj_categoria = Categoria(id, descricao)
        Categorias.atualizar(obj_categoria)
    @classmethod
    def categoria_excluir(cls, id: int) -> None:
        Categorias.excluir(id)

    ############ Métodos sobre Produtos ############
    @classmethod
    def produto_inserir(cls, descricao: str, preco: float, estoque: int, idcategoria: int) -> None:
        obj_produto = Produto(0, descricao, preco, estoque, idcategoria)
        Produtos.inserir(obj_produto)
    @classmethod
    def produto_listar(cls) -> List[Produto]:
        return Produtos.listar()
    @classmethod
    def produto_atualizar(cls, id: int, descricao: str, preco: float, estoque: int, idcategoria: int) -> None:
        obj_produto = Produto(id, descricao, preco, estoque, idcategoria)
        Produtos.atualizar(obj_produto)
    @classmethod
    def produto_excluir(cls, id: int) -> None:
        Produtos.excluir(id)

    
    ############ Métodos sobre Vendas ############
    @classmethod
    def venda_inserir(cls, data: datetime, carrinho: bool, total: float, idCliente: int) -> None:
        obj_venda = Venda(0, data, carrinho, total, idCliente)
        Vendas.inserir(obj_venda)
    @classmethod
    def venda_listar(cls) -> List[Venda]:
        return Vendas.listar()
    @classmethod
    def venda_atualizar(cls, id: int, data: datetime, carrinho: bool, total: float, idCliente: int) -> None:
        obj_venda = Venda(id, data, carrinho, total, idCliente)
        Vendas.atualizar(obj_venda)
    @classmethod
    def venda_excluir(cls, id: int) -> None:
        Vendas.excluir(id)


    ############ Métodos sobre VendaItens ############
    @classmethod
    def vendaitem_inserir(cls, qtd: int, preco: float, idvenda: int, idproduto: int) -> None:
        obj_item = VendaItem(0, qtd, preco, idvenda, idproduto)
        VendaItens.inserir(obj_item)
    @classmethod
    def vendaitem_listar(cls) -> List[VendaItem]:
        return VendaItens.listar()
    @classmethod
    def vendaitem_atualizar(cls, id: int, qtd: int, preco: float, idvenda: int, idproduto: int) -> None:
        obj_item = VendaItem(id, qtd, preco, idvenda, idproduto)
        VendaItens.atualizar(obj_item)
    @classmethod
    def vendaitem_excluir(cls, id: int) -> None:
        VendaItens.excluir(id)