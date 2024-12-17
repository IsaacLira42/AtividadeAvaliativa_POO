import streamlit as st
import pandas as pd
from view import View
import time

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

class ClienteUI:
    def main():
        st.header("Área do Cliente")

        # "Listar Produtos", "Adicionar Produto no Carrinho", "Fechar Pedido", "Ver Meus Pedidos"
        tab1, tab2, tab3 = st.tabs(["Listar Produtos", "Adicionar Produto no carrinho", "Remover Produto do carrinho"])
        with tab1: ClienteUI.listar()
        with tab2: ClienteUI.inserir()
        with tab3: ClienteUI.remover()
        #with tab4: ClienteUI.atualizar()

    def listar():
        # filtra as vendas do cliente
        cliente_id = st.session_state.get("cliente_id")
        vendas_cliente = View.vendas_cliente(cliente_id)  # Lista de vendas do cliente
        id_venda_atual = vendas_cliente[-1].id  # Id da venda atual

        vendaitens_cliente = [vendaitem for vendaitem in View.vendaitem_listar() if vendaitem.idvenda == id_venda_atual]
        todos_os_produtos = View.produto_listar()

        produtos_cliente = []

        for vendaitem in vendaitens_cliente:
            for produto in todos_os_produtos:
                if vendaitem.idproduto == produto.id:
                    produtos_cliente.append(produto)
                    break

        if len(produtos_cliente) == 0: 
            st.write("Nenhum produto cadastrado")
        else:    
            dic = []
            for obj in produtos_cliente: dic.append(obj.__dict__)
            df = pd.DataFrame([{"Descrição": p.descricao, "Preço": p.preco, "Estoque": p.estoque} for p in produtos_cliente])
            st.dataframe(df)

    def inserir():
        # Filtra as vendas do cliente
        cliente_id = st.session_state.get("cliente_id")
        vendas_cliente = View.vendas_cliente(cliente_id)  # Lista de vendas do cliente
        id_venda_atual = vendas_cliente[-1].id  # Id da venda atual

        # Listar categorias
        categorias = View.categoria_listar()
        if len(categorias) > 0:
            categoria_selecionada = st.selectbox("Selecione a categoria", [categoria.descricao for categoria in categorias])
            idCategoria = next(categoria.id for categoria in categorias if categoria.descricao == categoria_selecionada)

            # Filtrar os produtos da categoria selecionada
            todos_os_produtos = View.produto_listar()
            produtos_da_categoria_selecionada = [produto for produto in todos_os_produtos if produto.idCategoria == idCategoria]

            if len(produtos_da_categoria_selecionada) > 0:
                # Selecionar o produto e obter o ID dele
                produto_selecionado = st.selectbox("Selecione o produto", [produto.descricao for produto in produtos_da_categoria_selecionada])
                idProduto = next(produto.id for produto in produtos_da_categoria_selecionada if produto.descricao == produto_selecionado)

                produto_escolhido = Produtos.listar_id(idProduto)   # Produto escolhido

                quantidade = st.number_input("Quantidade do produto", min_value=1, step=1)

                # Calcular o preço
                preco = produto_escolhido.preco * quantidade

                # Atualizar o estoque do produo selecionad
                novo_estoque = produto_escolhido.estoque - quantidade

                # Botão para inserir o produto
                if st.button("Inserir"):
                    if novo_estoque < 0:
                        st.error("Estoque insuficiente!")
                    else:
                        produto_escolhido.estoque = novo_estoque
                        View.vendaitem_inserir(quantidade, preco, id_venda_atual, idProduto)
                        st.success("Produto inserido com sucesso!")
                        time.sleep(2)
                        st.rerun()
            else:
                st.error("Não há produtos disponíveis na categoria selecionada.")
        else:
            st.write("Nenhuma produto disponível.")