import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / 'meu_banco.sqlite')

cursor = conexao.cursor()

def criar_tabela(conexao, cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome varchar(100),
            email varchar(100)
    )
    ''')
    conexao.commit()

def inserir_registro(conexao, cursor, nome, email):
    data = (nome, email)
    cursor.execute('INSERT INTO clientes (nome, email) VALUES (?,?)', data)
    conexao.commit()

def atualizar_registro(conexao, cursor, nome, email, id):
    data = (nome, email, id)
    cursor.execute('UPDATE clientes SET nome=?, email=? WHERE id=?', data)
    conexao.commit()

def excluir_registro(conexao, cursor, id):
    data = (id,)
    cursor.execute('DELETE FROM clientes WHERE id=?', data)
    conexao.commit()


def inserir_muitos(conexao, cursor, dados):
    cursor.executemany('INSERT INTO clientes (nome, email) VALUES (?,?)', dados)
    conexao.commit()

dados = [
    ('Guilherme', 'gui@gmail.com'),
    ('Joao', 'joao@gmail.com')
]

inserir_muitos(conexao, cursor, dados)