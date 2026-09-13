import sqlite3
from datetime import datetime, timedelta
from faker import Faker
import random
import os

# Remove o banco antigo para recriar do zero
if os.path.exists('financeiro_empresa.db'):
    os.remove('financeiro_empresa.db')

fake = Faker('pt_BR')
conn = sqlite3.connect('financeiro_empresa.db')
cursor = conn.cursor()

# 1. Criação das Tabelas
cursor.execute('''
CREATE TABLE plano_contas (
    id_conta INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_conta TEXT NOT NULL,
    tipo TEXT NOT NULL 
)''')

cursor.execute('''
CREATE TABLE clientes_parceiros (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo_cliente TEXT NOT NULL, 
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL
)''')

cursor.execute('''
CREATE TABLE transacoes (
    id_transacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_conta INTEGER,
    id_cliente INTEGER,
    data_competencia DATE,
    data_vencimento DATE,
    data_pagamento DATE,
    valor REAL,
    status TEXT, 
    FOREIGN KEY (id_conta) REFERENCES plano_contas(id_conta),
    FOREIGN KEY (id_cliente) REFERENCES clientes_parceiros(id_cliente)
)''')
conn.commit()

# 2. Inserir Plano de Contas (IDs de 1 a 6 garantidos)
contas_fixas = [
    ('Receita de Vendas de Serviços', 'Receita'),
    ('Receita de Consultoria', 'Receita'),
    ('Custos Operacionais', 'Despesa'),
    ('Despesas com Marketing', 'Despesa'),
    ('Folha de Pagamento', 'Despesa'),
    ('Aluguel e Infraestrutura', 'Despesa')
]
cursor.executemany("INSERT INTO plano_contas (nome_conta, tipo) VALUES (?, ?)", contas_fixas)
conn.commit()

# 3. Inserir Clientes (IDs de 1 a 50 garantidos)
for _ in range(50):
    nome = fake.company() if random.choice([True, False]) else fake.name()
    tipo = 'PJ' if len(nome) > 20 else 'PF'
    cidade = fake.city()
    estado = fake.state_abbr()
    cursor.execute("INSERT INTO clientes_parceiros (nome, tipo_cliente, cidade, estado) VALUES (?, ?, ?, ?)", 
                   (nome, tipo, cidade, estado))
conn.commit()

# 4. Inserir Transações com IDs dinâmicos baseados nas tabelas reais
status_opcoes = ['Pago', 'Pendente', 'Cancelado']
pesos_status = [0.70, 0.25, 0.05] 

# Descobre quantos IDs reais existem nas tabelas de apoio
cursor.execute("SELECT COUNT(*) FROM plano_contas")
total_contas = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM clientes_parceiros")
total_clientes = cursor.fetchone()[0]

for _ in range(500):
    id_conta = random.randint(1, total_contas)       # Sorteia apenas dentro do que realmente existe!
    id_cliente = random.randint(1, total_clientes)   # Sorteia apenas dentro dos clientes reais!
    
    dias_atras = random.randint(0, 365)
    data_comp = datetime.now() - timedelta(days=dias_atras)
    data_venc = data_comp + timedelta(days=random.choice([15, 30, 45]))
    
    status = random.choices(status_opcoes, weights=pesos_status)[0]
    
    if status == 'Pago':
        data_pag = data_venc + timedelta(days=random.randint(-5, 10))
        data_pag_str = data_pag.strftime('%Y-%m-%d')
    else:
        data_pag_str = None

    if id_conta in [1, 2]:
        valor = round(random.uniform(3000.0, 15000.0), 2)
    else:
        valor = round(random.uniform(500.0, 8000.0), 2)

    cursor.execute('''
        INSERT INTO transacoes (id_conta, id_cliente, data_competencia, data_vencimento, data_pagamento, valor, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (id_conta, id_cliente, data_comp.strftime('%Y-%m-%d'), data_venc.strftime('%Y-%m-%d'), data_pag_str, valor, status))


conn.commit()
conn.close()
print("✅ Banco recriado com integridade referencial perfeita!")