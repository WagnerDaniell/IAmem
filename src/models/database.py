import sqlite3 
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "data", "iamem.db"))

def url_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok = True)

    conn = url_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS integrantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            area TEXT NOT NULL,   -- Som, Projecao, Fotografia
            prioridade TEXT NOT NULL,   -- Baixa, Media, Alta, Maxima
            disponivel INTEGER DEFAULT 1,   -- 1 para Sim, 0 para Nâo
            participacao_recente INTEGER DEFAULT 0,   -- 1 para Sim, 0 para Não
            escalas_seguidas INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS escalas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_escala TEXT DEFAULT (DATE('now')),   -- Salva a data da escala automaticamente
            som TEXT,
            projecao TEXT,
            fotografia TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Banco de dados inicializado em: {DB_PATH}")

def cadastrar_integrante(nome, area, prioridade, disponivel=1, participacao_recente=0, escalas_seguidas=0):
    conn = url_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO integrantes (nome, area, prioridade, disponivel, participacao_recente, escalas_seguidas)
        VALUES (?, ?, ?, ?, ?, ?)  
    ''', (nome, area, prioridade, disponivel, participacao_recente, escalas_seguidas))

    conn.commit()
    conn.close()

def listar_integrantes():
    conn = url_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM integrantes")
    integrantes = cursor.fetchall()
    
    conn.close()
    return integrantes

def editar_disponibilidade(integrante_id, nova_disponibilidade):
    conn = url_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE integrantes 
        SET disponivel = ? 
        WHERE id = ?
    """, (nova_disponibilidade, integrante_id))
    
    conn.commit()
    conn.close()

def editar_integrante_completo(integrante_id, nome, area, prioridade, disponivel, participacao_recente, escalas_seguidas):
    conn = url_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE integrantes
        SET nome = ?, area = ?, prioridade = ?, disponivel = ?, participacao_recente = ?, escalas_seguidas = ?
        WHERE id = ?
    ''', (nome, area, prioridade, disponivel, participacao_recente, escalas_seguidas, integrante_id))

    conn.commit()
    conn.close()

def salvar_escala(nome_som, nome_projecao, nome_fotografia):
    conn = url_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO escalas (som, projecao, fotografia)
        VALUES (?, ?, ?)
    ''', (nome_som, nome_projecao, nome_fotografia))

    conn.commit()
    conn.close()

                        