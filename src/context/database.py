import sqlite3 
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "data", "iamem.db"))
SEED_SQL_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "data", "seed_integrantes.sql"))

def url_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = url_connection()
    cursor = conn.cursor()

    # Tabela de integrantes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='integrantes'")
    tabela_existe = cursor.fetchone() is not None

    if not tabela_existe:
        cursor.execute('''
            CREATE TABLE integrantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                area TEXT NOT NULL,
                prioridade TEXT NOT NULL,
                disponivel_quarta INTEGER DEFAULT 1,
                disponivel_sexta INTEGER DEFAULT 1,
                disponivel_domingo INTEGER DEFAULT 1,
                participacao_recente INTEGER DEFAULT 0,
                escalas_seguidas INTEGER DEFAULT 0
            )
        ''')
    else:
        for dia in ["quarta", "sexta", "domingo"]:
            try:
                cursor.execute(f"ALTER TABLE integrantes ADD COLUMN disponivel_{dia} INTEGER DEFAULT 1")
            except:
                pass

    # Tabela de escalas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS escalas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_escala TEXT,
            som TEXT,
            projecao TEXT,
            fotografia TEXT
        )
    ''')

    # Tabela de feedback para ML
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback_escala (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_escala TEXT NOT NULL,
            area TEXT NOT NULL,
            integrante_id INTEGER NOT NULL,
            foi_escalado INTEGER NOT NULL,
            disponivel_dia INTEGER,
            prioridade TEXT,
            participacao_recente INTEGER,
            escalas_seguidas INTEGER,
            area_atuacao TEXT,
            avaliacao INTEGER,
            FOREIGN KEY (integrante_id) REFERENCES integrantes(id)
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM integrantes")
    qtd_integrantes = cursor.fetchone()[0]
    if qtd_integrantes == 0 and os.path.exists(SEED_SQL_PATH):
        with open(SEED_SQL_PATH, "r", encoding="utf-8") as arquivo_seed:
            cursor.executescript(arquivo_seed.read())
        print(f"Mocks iniciais carregados a partir de: {SEED_SQL_PATH}")

    conn.commit()
    conn.close()
    print(f"Banco de dados inicializado em: {DB_PATH}")

# --- CRUD Integrantes ---
def cadastrar_integrante(nome, area, prioridade, 
                         disponivel_quarta=1, disponivel_sexta=1, disponivel_domingo=1,
                         participacao_recente=0, escalas_seguidas=0):
    conn = url_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO integrantes (nome, area, prioridade, 
                                 disponivel_quarta, disponivel_sexta, disponivel_domingo,
                                 participacao_recente, escalas_seguidas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, area, prioridade, 
          disponivel_quarta, disponivel_sexta, disponivel_domingo,
          participacao_recente, escalas_seguidas))
    conn.commit()
    conn.close()

def listar_integrantes():
    conn = url_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM integrantes")
    integrantes = cursor.fetchall()
    conn.close()
    return integrantes

def editar_integrante_completo(integrante_id, nome, area, prioridade, 
                               disponivel_quarta, disponivel_sexta, disponivel_domingo,
                               participacao_recente, escalas_seguidas):
    conn = url_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE integrantes
        SET nome = ?, area = ?, prioridade = ?,
            disponivel_quarta = ?, disponivel_sexta = ?, disponivel_domingo = ?,
            participacao_recente = ?, escalas_seguidas = ?
        WHERE id = ?
    ''', (nome, area, prioridade,
          disponivel_quarta, disponivel_sexta, disponivel_domingo,
          participacao_recente, escalas_seguidas, integrante_id))
    conn.commit()
    conn.close()

def deletar_integrante(integrante_id):
    conn = url_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM integrantes WHERE id = ?", (integrante_id,))
    conn.commit()
    conn.close()

# --- Escalas ---
def salvar_escala(nome_som, nome_projecao, nome_fotografia, data=None):
    conn = url_connection()
    cursor = conn.cursor()
    if data is None:
        cursor.execute('''
            INSERT INTO escalas (som, projecao, fotografia)
            VALUES (?, ?, ?)
        ''', (nome_som, nome_projecao, nome_fotografia))
    else:
        cursor.execute('''
            INSERT INTO escalas (data_escala, som, projecao, fotografia)
            VALUES (?, ?, ?, ?)
        ''', (data, nome_som, nome_projecao, nome_fotografia))
    conn.commit()
    conn.close()

def listar_escalas():
    conn = url_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM escalas ORDER BY data_escala DESC")
    escalas = cursor.fetchall()
    conn.close()
    return escalas

def listar_escalas_recentes(limit=9):
    conn = url_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT data_escala, som, projecao, fotografia
        FROM escalas
        WHERE data_escala IS NOT NULL
        ORDER BY data_escala DESC, id DESC
        LIMIT ?
    """, (limit,))
    escalas = cursor.fetchall()
    conn.close()
    return escalas

# --- Status dos integrantes ---
def reset_status_area(area, ids_selecionados):
    conn = url_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE integrantes 
        SET participacao_recente = 0, escalas_seguidas = 0
        WHERE area = ?
    """, (area,))
    for id_int in ids_selecionados:
        cursor.execute("""
            UPDATE integrantes 
            SET participacao_recente = 1,
                escalas_seguidas = escalas_seguidas + 1
            WHERE id = ?
        """, (id_int,))
    conn.commit()
    conn.close()

# --- Feedback para ML ---
def registrar_feedback(data_escala, area, integrante_id, foi_escalado,
                       disponivel_dia, prioridade, participacao_recente, escalas_seguidas,
                       avaliacao=None):
    conn = url_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback_escala (data_escala, area, integrante_id, foi_escalado,
                                     disponivel_dia, prioridade, participacao_recente,
                                     escalas_seguidas, area_atuacao, avaliacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data_escala, area, integrante_id, foi_escalado,
          disponivel_dia, prioridade, participacao_recente, escalas_seguidas,
          area, avaliacao))
    conn.commit()
    conn.close()

def obter_dados_treino():
    conn = url_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT data_escala, integrante_id, disponivel_dia, prioridade,
               participacao_recente, escalas_seguidas, area_atuacao, avaliacao
        FROM feedback_escala
        WHERE avaliacao IS NOT NULL
    ''')
    dados = cursor.fetchall()
    conn.close()

    dias_pt = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]
    return [
        {
            "dia_semana": dias_pt[datetime.fromisoformat(d[0]).weekday()] if d[0] else None,
            "integrante_id": d[1],
            "disponivel_dia": d[2],
            "prioridade": d[3],
            "participacao_recente": d[4],
            "escalas_seguidas": d[5],
            "area": d[6],
            "target": d[7]
        }
        for d in dados
    ]

def buscar_integrante_por_id(id_int):
    conn = url_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM integrantes WHERE id = ?", (id_int,))
    integrante = cursor.fetchone()
    conn.close()
    return integrante
