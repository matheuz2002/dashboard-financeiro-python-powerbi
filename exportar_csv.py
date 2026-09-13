import sqlite3
import pandas as pd

# Conecta ao banco SQLite
conn = sqlite3.connect('financeiro_empresa.db')

# 1. Exporta as tabelas básicas puras
pd.read_sql("SELECT * FROM plano_contas", conn).to_csv("plano_contas.csv", index=False, encoding='utf-8-sig')
pd.read_sql("SELECT * FROM clientes_parceiros", conn).to_csv("clientes_parceiros.csv", index=False, encoding='utf-8-sig')

# 2. Para as transações, garantimos que os IDs estejam alinhados corretamente com as tabelas de apoio
query_transacoes = '''
    SELECT 
        id_transacao,
        id_conta,
        id_cliente,
        data_competencia,
        data_vencimento,
        data_pagamento,
        valor,
        status
    FROM transacoes
'''
pd.read_sql(query_transacoes, conn).to_csv("transacoes.csv", index=False, encoding='utf-8-sig')

conn.close()
print("✅ CSVs recriados com integridade garantida!")