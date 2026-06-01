# src/services/gerador_escala.py
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from datetime import date, timedelta
from src.context.database import (
    listar_integrantes, salvar_escala, reset_status_area,
    registrar_feedback, obter_dados_treino, listar_escalas_recentes
)

PRIORIDADES_INT = {"Maxima": 4, "Alta": 3, "Media": 2, "Baixa": 1}
ORDEM_DIAS = ["Domingo", "Quarta", "Sexta"]
INDICE_DISP = {"Quarta": 4, "Sexta": 5, "Domingo": 6}
PRIORIDADE_BONUS = {"Maxima": 0.20, "Alta": 0.12, "Media": 0.05, "Baixa": 0.0}
NOME_FIXO_POR_AREA = {"Som": {"Washington"}}
PENALIDADE_PARTICIPACAO_RECENTE = 0.18
PENALIDADE_ESCALAS_SEGUIDAS = 0.10
PENALIDADE_REPETICAO_SEMANAL = 0.30
PENALIDADE_REPETICAO_HISTORICA = 0.35

modelo = None
feature_names = None

def _dataset_minimo():
    """Dataset mínimo de fallback (apenas para não travar na primeira execução)."""
    dados = []
    for disp in [0, 1]:
        for prio in ["Baixa", "Media", "Alta", "Maxima"]:
            dados.append({
                "disponivel_dia": disp,
                "prioridade": prio,
                "participacao_recente": 0,
                "escalas_seguidas": 0,
                "area": "Som",
                "target": 1 if disp and prio in ("Alta", "Maxima") else 0
            })
    return pd.DataFrame(dados)

def _train_model():
    global modelo, feature_names
    dados_reais = obter_dados_treino()  # lista de dicts com features + target

    if len(dados_reais) >= 5:
        df = pd.DataFrame(dados_reais)
        print(f"✅ Treinando APENAS com {len(df)} exemplos reais.")
    else:
        df = _dataset_minimo()
        if dados_reais:
            df_real = pd.DataFrame(dados_reais)
            df = pd.concat([df, df_real], ignore_index=True)
            print(f"⚠️ Poucos dados reais ({len(dados_reais)}). Usando dataset sintético mínimo + real.")

    df_encoded = pd.get_dummies(df, columns=["prioridade", "area"])
    ref_prioridade = "prioridade_Baixa"
    ref_area = "area_Som"
    for col in [ref_prioridade, ref_area]:
        if col in df_encoded.columns:
            df_encoded.drop(col, axis=1, inplace=True)

    X = df_encoded.drop("target", axis=1)
    y = df_encoded["target"]

    # Garante que o modelo tenha as duas classes quando o histórico ainda está enviesado.
    if y.nunique() < 2:
        complemento = _dataset_minimo()
        complemento = complemento[complemento["target"] != y.iloc[0]]
        if not complemento.empty:
            df = pd.concat([df, complemento], ignore_index=True)
            df_encoded = pd.get_dummies(df, columns=["prioridade", "area"])
            for col in [ref_prioridade, ref_area]:
                if col in df_encoded.columns:
                    df_encoded.drop(col, axis=1, inplace=True)
            X = df_encoded.drop("target", axis=1)
            y = df_encoded["target"]

    modelo = DecisionTreeClassifier(criterion="gini", max_depth=5, random_state=42)
    modelo.fit(X, y)
    feature_names = X.columns.tolist()

def _ensure_model():
    if modelo is None:
        _train_model()

def _preparar_features(integrante, dia):
    _, _, area, prioridade, disp_quarta, disp_sexta, disp_domingo, part_rec, escalas = integrante
    idx = INDICE_DISP[dia]
    disp_dia = integrante[idx]

    data = {
        "disponivel_dia": disp_dia,
        "participacao_recente": part_rec,
        "escalas_seguidas": escalas,
        "prioridade_Media": 1 if prioridade == "Media" else 0,
        "prioridade_Alta": 1 if prioridade == "Alta" else 0,
        "prioridade_Maxima": 1 if prioridade == "Maxima" else 0,
        "area_Projecao": 1 if area == "Projecao" else 0,
        "area_Fotografia": 1 if area == "Fotografia" else 0,
    }
    return pd.DataFrame([data])[feature_names]

def _nome_integrante(integrante):
    return integrante[1]

def _esta_na_regra_fixa(integrante, area_alvo):
    return _nome_integrante(integrante) in NOME_FIXO_POR_AREA.get(area_alvo, set())

def _score_candidato(integrante, prob, bloqueado):
    prioridade = integrante[3]
    participacao_recente = integrante[7]
    escalas_seguidas = integrante[8]

    score = prob
    score += PRIORIDADE_BONUS.get(prioridade, 0.0)
    score -= PENALIDADE_PARTICIPACAO_RECENTE * participacao_recente
    score -= PENALIDADE_ESCALAS_SEGUIDAS * min(escalas_seguidas, 5)

    if bloqueado:
        score -= PENALIDADE_REPETICAO_SEMANAL

    return score

def _historico_recente():
    historico = listar_escalas_recentes(limit=9)
    frequencia = {}
    for _, som, projecao, fotografia in historico:
        for nome in [som, projecao, fotografia]:
            if nome:
                frequencia[nome] = frequencia.get(nome, 0) + 1
    return frequencia

def _score_candidato_com_historico(integrante, prob, bloqueado, frequencia_historica):
    score = _score_candidato(integrante, prob, bloqueado)
    nome = integrante[1]
    repeticoes = frequencia_historica.get(nome, 0)
    if repeticoes:
        score -= PENALIDADE_REPETICAO_HISTORICA * repeticoes
    return score

def _probabilidade_de_escala(integrante, dia):
    features = _preparar_features(integrante, dia)
    classes = getattr(modelo, "classes_", [])

    # Quando o treino ficou com apenas uma classe, o sklearn devolve uma coluna só.
    if len(classes) == 1:
        return 1.0 if classes[0] == 1 else 0.0

    probs = modelo.predict_proba(features)[0]
    if len(probs) == 1:
        return probs[0] if classes[0] == 1 else 1.0 - probs[0]

    if 1 in classes:
        idx_classe_1 = list(classes).index(1)
        return probs[idx_classe_1]

    return float(probs[-1])

def selecionar_por_area_ml(integrantes, area_alvo, dia, ids_bloqueados=None):
    _ensure_model()
    if ids_bloqueados is None:
        ids_bloqueados = set()
    idx = INDICE_DISP[dia]
    frequencia_historica = _historico_recente()

    candidatos = [
        i for i in integrantes
        if i[2] == area_alvo and i[idx] == 1
    ]
    if not candidatos:
        return None, []

    candidatos_frescos = [i for i in candidatos if i[0] not in ids_bloqueados]
    candidatos_para_uso = candidatos_frescos if candidatos_frescos else candidatos

    if area_alvo in NOME_FIXO_POR_AREA:
        for candidato in candidatos_para_uso:
            if _esta_na_regra_fixa(candidato, area_alvo):
                return candidato, candidatos

    classificados = []
    for integ in candidatos_para_uso:
        prob = _probabilidade_de_escala(integ, dia)
        bloqueado = integ[0] in ids_bloqueados
        score = _score_candidato_com_historico(integ, prob, bloqueado, frequencia_historica)
        classificados.append((integ, score))

    classificados.sort(
        key=lambda x: (
            -x[1],
            -PRIORIDADES_INT.get(x[0][3], 0),
            x[0][8],
            x[0][0]
        )
    )
    escolhido = classificados[0][0]
    return escolhido, candidatos

def _proximas_datas():
    hoje = date.today()
    alvos = {"Quarta": 2, "Sexta": 4, "Domingo": 6}
    datas = {}
    for nome, weekday in alvos.items():
        dias = (weekday - hoje.weekday()) % 7
        if dias == 0:
            dias = 7
        datas[nome] = (hoje + timedelta(days=dias)).isoformat()
    return datas

def gerar_escala_semana():
    _ensure_model()
    integrantes = listar_integrantes()
    datas = _proximas_datas()
    resultado = {}
    ids_usados = set()

    for dia in ORDEM_DIAS:
        data = datas[dia]
        escolhidos = {}
        escolhidos_ids = {}
        for area in ["Som", "Projecao", "Fotografia"]:
            escolhido, todos_candidatos = selecionar_por_area_ml(integrantes, area, dia, ids_usados)
            if escolhido:
                nome = escolhido[1]
                id_int = escolhido[0]
                escolhidos[area] = nome
                escolhidos_ids[area] = id_int
                if not _esta_na_regra_fixa(escolhido, area):
                    ids_usados.add(id_int)

                for candidato in todos_candidatos:
                    foi_escalado = 1 if candidato[0] == escolhido else 0
                    idx = INDICE_DISP[dia]
                    disp_dia = candidato[idx]
                    registrar_feedback(
                        data, area, candidato[0], foi_escalado,
                        disponivel_dia=disp_dia,
                        prioridade=candidato[3],
                        participacao_recente=candidato[7],
                        escalas_seguidas=candidato[8],
                        avaliacao=None
                    )
            else:
                escolhidos[area] = None
                escolhidos_ids[area] = None

        salvar_escala(
            data=data,
            nome_som=escolhidos.get("Som"),
            nome_projecao=escolhidos.get("Projecao"),
            nome_fotografia=escolhidos.get("Fotografia")
        )
        resultado[dia] = (data, escolhidos, escolhidos_ids)

    # Atualiza status (agora usando os IDs coletados)
    for dia in ORDEM_DIAS:
        _, _, ids_dict = resultado[dia]
        for area in ["Som", "Projecao", "Fotografia"]:
            id_int = ids_dict.get(area)
            if id_int is not None:
                reset_status_area(area, [id_int])
            else:
                reset_status_area(area, [])

    return resultado

def retreinar_modelo():
    _train_model()
    plt.figure(figsize=(15, 8))
    plot_tree(modelo, feature_names=feature_names, filled=True, rounded=True)
    plt.title("Árvore de Decisão Atualizada")
    plt.show()
