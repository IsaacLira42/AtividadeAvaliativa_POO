import streamlit as st
import pandas as pd
from view import View
import time

class VizualizarPedidosUI:
    def main():
        st.header("Histórico de Pedidos")
        
        todos_os_pedidos = View.venda_listar()

        if len(todos_os_pedidos) == 0: 
            st.write("Nenhum pedidio cadastrado")
        else:    
            dic = []
            for obj in todos_os_pedidos: dic.append(obj.__dict__)
            df = pd.DataFrame([{"Id": v.id, "Data": v.data, "Carrinho": v.carrinho, "Total": v.total, "IdCliente": v.idCliente} for v in todos_os_pedidos])
            st.dataframe(df)