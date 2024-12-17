import streamlit as st
import pandas as pd
from view import View
import time

class ReajustarPrecosUI:
    def main():
        st.header("Reajuste de Preços")

        produtos = View.produto_listar()

        if len(produtos) == 0: 
            st.write("Nenhum produto cadastrado")
        else:
            reajuste = st.number_input("Reajuste (%)")
            valor = (100 + (reajuste)) / 100

            butaun = st.button("Reajustar")

            if butaun:
                for produto in produtos:
                    View.produto_atualizar(produto.id, produto.descricao, produto.preco*valor, produto.estoque, produto.idCategoria)

                st.success(f"Preços reajustados em {reajuste}%")
                time.sleep(2)
                st.rerun()