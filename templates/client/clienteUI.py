from datetime import datetime
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

        butaun_finalizar = st.button("Fechar Pedido")
        if butaun_finalizar:
            ClienteUI.fecharpedido()

        # "Listar Produtos", "Adicionar Produto no Carrinho", "Fechar Pedido", "Ver Meus Pedidos"
        tab1, tab2, tab3, tab4= st.tabs(["Visualizar Carrinho", "Adicionar Produto", "Remover Produto", "Meus Pedidos"])
        with tab1: ClienteUI.listar()
        with tab2: ClienteUI.inserir()
        with tab3: ClienteUI.remover()
        with tab4: ClienteUI.meuspedidos()

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
            df = pd.DataFrame([{"Descrição": p.descricao, "Preço": p.preco, "estoque": p.estoque} for p in produtos_cliente])
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
                    # Verifica se o produto já existe no carrinho
                    vendaitens_cliente = [item for item in View.vendaitem_listar() if item.idvenda == id_venda_atual]
                    if any(item.idproduto == idProduto for item in vendaitens_cliente):
                        st.warning("Este produto já está no carrinho.")
                    else:
                        # Atualizar estoque e inserir produto
                        View.produto_atualizar(idProduto, produto_escolhido.descricao, produto_escolhido.preco, novo_estoque, produto_escolhido.idCategoria)
                        View.vendaitem_inserir(quantidade, preco, id_venda_atual, idProduto)
                        st.success("Produto inserido com sucesso!")
                        time.sleep(2)
                        st.rerun()

            else:
                st.error("Não há produtos disponíveis na categoria selecionada.")
        else:
            st.write("Nenhuma produto disponível.")

    def remover():
        # Filtra as vendas do cliente
        cliente_id = st.session_state.get("cliente_id")
        vendas_cliente = View.vendas_cliente(cliente_id)  # Lista de vendas do cliente
        if not vendas_cliente:
            st.warning("Nenhuma venda encontrada.")
            return

        id_venda_atual = vendas_cliente[-1].id  # Id da venda atual

        # Carrinho mais recente (aberto)
        vendaitens_cliente = [vendaitem for vendaitem in View.vendaitem_listar() if vendaitem.idvenda == id_venda_atual]
        todos_os_produtos = View.produto_listar()

        # Filtrando os produtos no carrinho
        produtos_cliente = []
        for vendaitem in vendaitens_cliente:
            for produto in todos_os_produtos:
                if vendaitem.idproduto == produto.id:
                    produtos_cliente.append(produto)
                    break

        # Caso o carrinho esteja vazio
        if not produtos_cliente:
            st.info("Nenhum produto no carrinho para remover.")
            return

        # Seleção do produto a ser removido
        produto_excluir = st.selectbox("Selecione o produto", [produto.descricao for produto in produtos_cliente])

        # Usando o parâmetro default no next()
        idProduto = next((produto.id for produto in produtos_cliente if produto.descricao == produto_excluir), None)
        if idProduto is None:
            st.error("Erro ao identificar o produto selecionado.")
            return

        id_vendaitem_excluir = next((item.id for item in vendaitens_cliente if item.idproduto == idProduto), None)
        if id_vendaitem_excluir is None:
            st.error("Erro ao identificar o item no carrinho.")
            return

        # Atualização do estoque do produto
        produto_selecionado = Produtos.listar_id(idProduto)
        venda_item = VendaItens.listar_id(id_vendaitem_excluir)

        if not venda_item:
            st.error("Erro ao buscar o item da venda.")
            return

        # Ajustar estoque
        novo_estoque = produto_selecionado.estoque + venda_item.qtd

        # Botão para exclusão
        if st.button("Excluir"):
            View.produto_atualizar(idProduto, produto_selecionado.descricao, produto_selecionado.preco,novo_estoque, produto_selecionado.idCategoria)
            View.vendaitem_excluir(id_vendaitem_excluir)
            st.success("Produto removido do carrinho com sucesso!")
            time.sleep(2)
            st.rerun()

    def meuspedidos():
        # filtra as vendas do cliente
        cliente_id = st.session_state.get("cliente_id")
        vendas_cliente = View.vendas_cliente(cliente_id)  # Lista de vendas do cliente
        id_venda_atual = vendas_cliente[-1].id  # Id da venda atual

        vendaitens_cliente = [vendaitem for vendaitem in View.vendaitem_listar() if vendaitem.idvenda == id_venda_atual]

        total = 0
        for itens in vendaitens_cliente:
            total += itens.preco

        vendas_cliente[-1].total = total

        if len(vendas_cliente) == 0: 
            st.write("Nenhum produto cadastrado")
        else:    
            dic = []
            for obj in vendas_cliente: dic.append(obj.__dict__)
            df = pd.DataFrame([{"data": v.data, "total": v.total, "carrinho": v.carrinho} for v in vendas_cliente])
            st.dataframe(df)

    def fecharpedido():
        # Filtra as vendas do cliente
        cliente_id = st.session_state.get("cliente_id")
        vendas_cliente = View.vendas_cliente(cliente_id)  # Lista de vendas do cliente
        if not vendas_cliente:
            st.warning("Nenhuma venda encontrada.")
            return

        id_venda_atual = vendas_cliente[-1].id  # Id da venda atual

        # Carrinho mais recente (aberto)
        vendaitens_cliente = [vendaitem for vendaitem in View.vendaitem_listar() if vendaitem.idvenda == id_venda_atual]

        total_venda_atual = 0
        for itens in vendaitens_cliente:
            total_venda_atual += itens.preco

        if total_venda_atual > 0:
            # Atualizando/encerrando venda
            View.venda_atualizar(id_venda_atual, vendas_cliente[-1].data, False, total_venda_atual, cliente_id)

            # Criando novo carrinho
            View.venda_inserir(datetime.now(), True, 0, cliente_id)
            st.success("Venda Finalizada com sucesso")
        else:
            st.error("A compra não foi finalizada, Carrinho vazio")