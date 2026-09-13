import sqlite3

# Conexão ao banco de dados 
conn = sqlite3.connect('financeiro_empresa.db')
cursor = conn.cursor()

print("="*60)
print(" 📊 RELATÓRIOS FINANCEIROS ESTRATÉGICOS ")
print("="*60)

# --- CONSULTA 1: Faturamento Total e Volume por Categoria (Receitas vs Despesas) ---
# --- CONSULTA 1: Faturamento Total e Volume por Categoria (Receitas vs Despesas) ---
print("\n[1] Resumo Financeiro por Categoria de Conta:")
query_1 = '''
    SELECT 
        T.nome_conta,
        T.tipo,
        COUNT(TR.id_transacao) AS total_transacoes,
        SUM(TR.valor) AS valor_total
    FROM transacoes TR
    JOIN plano_contas T ON TR.id_conta = T.id_conta
    WHERE TR.status = 'Pago'
    GROUP BY T.nome_conta, T.tipo
    ORDER BY valor_total DESC;
'''
cursor.execute(query_1)
for linha in cursor.fetchall():
    print(f"Conta: {linha[0]} | Tipo: {linha[1]} | Transações: {linha[2]} | Valor Total: R$ {linha[3]:,.2f}")


# --- CONSULTA 2: Aging List / Contas em Atraso ou Pendentes ---
print("\n[2] Contas Pendentes e Risco de Inadimplência (Por Cliente):")
query_2 = '''
    SELECT 
        C.nome AS cliente,
        C.tipo_cliente,
        C.cidade,
        COUNT(TR.id_transacao) AS qtd_titulos_pendentes,
        SUM(TR.valor) AS valor_pendente
    FROM transacoes TR
    JOIN clientes_parceiros C ON TR.id_cliente = C.id_cliente
    WHERE TR.status = 'Pendente'
    GROUP BY C.nome, C.tipo_cliente, C.cidade
    ORDER BY valor_pendente DESC
    LIMIT 5;
'''
cursor.execute(query_2)
for linha in cursor.fetchall():
    print(f"Cliente: {linha[0]} ({linha[1]}) - {linha[2]} | Títulos Pendentes: {linha[3]} | Valor Total Devido: R$ {linha[4]:,.2f}")


# --- CONSULTA 3: Fluxo de Caixa Consolidado (Receitas vs Despesas Pagas) ---
print("\n[3] Balanço Consolidado (Entradas vs Saídas Realizadas):")
query_3 = '''
    SELECT 
        T.tipo,
        SUM(TR.valor) AS total_movimentado
    FROM transacoes TR
    JOIN plano_contas T ON TR.id_conta = T.id_conta
    WHERE TR.status = 'Pago'
    GROUP BY T.tipo;
'''
cursor.execute(query_3)
balanco = cursor.fetchall()
total_receitas = 0
total_despesas = 0

for tipo, valor in balanco:
    if tipo == 'Receita':
        total_receitas = valor
    else:
        total_despesas = valor

lucro_liquido = total_receitas - total_despesas

print(f"Total de Entradas (Receitas): R$ {total_receitas:,.2f}")
print(f"Total de Saídas (Despesas):   R$ {total_despesas:,.2f}")
print(f"--------------------------------------------------")
print(f"Resultado Líquido do Caixa:   R$ {lucro_liquido:,.2f}")
print("="*60)

conn.close()