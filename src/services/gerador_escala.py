import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from datetime import date, timedelta
from src.context.database import (
    listar_integrantes, salvar_escala, reset_status_area,
    registrar_feedback, obter_dados_treino
)

ORDEM_DIAS = ["Domingo", "Quarta", "Sexta"]
INDICE_DISP = {"Quarta": 4, "Sexta": 5, "Domingo": 6}
DIAS_SEMANA = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]

modelo = None
feature_names = None


def _dataset_minimo():
    """Dataset de fallback para a primeira execucao."""
    dados = []
    prioridades = {"Baixa": 0, "Media": 1, "Alta": 2, "Maxima": 3}
    for integrante_id in range(1, 13):
        for dia_semana in DIAS_SEMANA:
            for area in ["Som", "Projecao", "Fotografia"]:
                for disp in [0, 1]:
                    for prio in ["Baixa", "Media", "Alta", "Maxima"]:
                        for part_rec in [0, 1]:
                            for seguidas in [0, 1]:
                                score_base = prioridades[prio] + (1 if area != "Som" else 0)
                                penalidade = (part_rec * 2) + seguidas + (1 if dia_semana == "Domingo" else 0)
                                dados.append({
                                    "integrante_id": integrante_id,
                                    "dia_semana": dia_semana,
                                    "disponivel_dia": disp,
                                    "prioridade": prio,
                                    "participacao_recente": part_rec,
                                    "escalas_seguidas": seguidas,
                                    "area": area,
                                    "target": 1 if disp and score_base >= penalidade else 0
                                })
    return pd.DataFrame(dados)


def _train_model():
    global modelo, feature_names
    dados_reais = obter_dados_treino()

    if len(dados_reais) >= 5:
        df = pd.DataFrame(dados_reais)
        print(f"Treinando APENAS com {len(df)} exemplos reais.")
    else:
        df = _dataset_minimo()
        if dados_reais:
            df_real = pd.DataFrame(dados_reais)
            df = pd.concat([df, df_real], ignore_index=True)
            print(f"⚠️ Poucos dados reais ({len(dados_reais)}). Usando dataset sintético mínimo + real.")

    df_encoded = pd.get_dummies(df, columns=["prioridade", "area", "dia_semana", "integrante_id"])

    X = df_encoded.drop("target", axis=1)
    y = df_encoded["target"]

    if y.nunique() < 2:
        complemento = _dataset_minimo()
        complemento = complemento[complemento["target"] != y.iloc[0]]
        if not complemento.empty:
            df = pd.concat([df, complemento], ignore_index=True)
            df_encoded = pd.get_dummies(df, columns=["prioridade", "area", "dia_semana", "integrante_id"])
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
        "integrante_id": integrante[0],
        "dia_semana": dia,
        "disponivel_dia": disp_dia,
        "participacao_recente": part_rec,
        "escalas_seguidas": escalas,
        "prioridade": prioridade,
        "area": area,
    }
    features = pd.DataFrame([data])
    features = pd.get_dummies(features, columns=["prioridade", "area", "dia_semana", "integrante_id"])
    return features.reindex(columns=feature_names, fill_value=0)


def _probabilidade_de_escala(integrante, dia):
    features = _preparar_features(integrante, dia)
    classes = getattr(modelo, "classes_", [])

    if len(classes) == 1:
        return 1.0 if classes[0] == 1 else 0.0

    probs = modelo.predict_proba(features)[0]
    classes_lista = list(classes)
    if 1 in classes_lista:
        idx_classe_1 = classes_lista.index(1)
        return probs[idx_classe_1]

    return float(probs[-1])


def selecionar_por_area_ml(integrantes, area_alvo, dia):
    _ensure_model()
    idx = INDICE_DISP[dia]

    candidatos = [
        i for i in integrantes
        if i[2] == area_alvo and i[idx] == 1
    ]
    if not candidatos:
        return None, []

    classificados = []
    for integ in candidatos:
        prob = _probabilidade_de_escala(integ, dia)
        classificados.append((integ, prob))

    classificados.sort(key=lambda x: (-x[1], x[0][0]))
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

    for dia in ORDEM_DIAS:
        data = datas[dia]
        escolhidos = {}
        escolhidos_ids = {}

        for area in ["Som", "Projecao", "Fotografia"]:
            escolhido, todos_candidatos = selecionar_por_area_ml(integrantes, area, dia)
            if escolhido:
                nome = escolhido[1]
                id_int = escolhido[0]
                escolhidos[area] = nome
                escolhidos_ids[area] = id_int

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
    plt.title("Arvore de Decisao Atualizada")
    plt.show()
