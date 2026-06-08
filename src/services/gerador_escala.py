import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from datetime import date, timedelta
from src.context.database import (
    listar_integrantes, salvar_escala, reset_status_area,
    registrar_feedback, obter_dados_treino
)

DIAS_ESCALA = {
    "Domingo": {"weekday": 6, "indice_disp": 6},
    "Quarta": {"weekday": 2, "indice_disp": 4},
    "Sexta": {"weekday": 4, "indice_disp": 5},
}
ORDEM_DIAS = list(DIAS_ESCALA)
INDICE_DISP = {dia: dados["indice_disp"] for dia, dados in DIAS_ESCALA.items()}

modelo = None
feature_names = None


def _train_model():
    global modelo, feature_names
    dados_reais = obter_dados_treino()

    if not dados_reais:
        raise ValueError("Nao ha dados reais suficientes para treinar o modelo.")

    df = pd.DataFrame(dados_reais)
    print(f"Treinando APENAS com {len(df)} exemplos reais.")

    df_encoded = pd.get_dummies(df, columns=["prioridade", "area", "dia_semana", "integrante_id"])

    X = df_encoded.drop("target", axis=1)
    y = df_encoded["target"]

    if y.nunique() < 2:
        raise ValueError("Os dados reais ainda nao possuem variacao suficiente para treinar o modelo.")

    modelo = DecisionTreeClassifier(criterion="gini", max_depth=5, random_state=42)
    modelo.fit(X, y)#relacao entre x e y, treina o modelo
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
    return features.reindex(columns=feature_names, fill_value=0) #realinha as colunas na ordem do treino


def _probabilidade_de_escala(integrante, dia):
    features = _preparar_features(integrante, dia)
    classes = getattr(modelo, "classes_", []) #O modelo tem duas classes escalado e não escalado

    if len(classes) == 1:
        return 1.0 if classes[0] == 1 else 0.0

    probs = modelo.predict_proba(features)[0] ##Calcula a probabilidade
    classes_lista = list(classes)
    if 1 in classes_lista:
        idx_classe_1 = classes_lista.index(1)
        return probs[idx_classe_1]

    return float(probs[-1])


def selecionar_por_area_ml(integrantes, area_alvo, dia):
    _ensure_model()
    idx = INDICE_DISP[dia]

    candidatos = [ #filtra os candidatos por area
        i for i in integrantes
        if i[2] == area_alvo and i[idx] == 1
    ]
    if not candidatos:
        return None, []

    classificados = []
    for integ in candidatos:
        prob = _probabilidade_de_escala(integ, dia)
        classificados.append((integ, prob))

    classificados.sort(key=lambda x: (-x[1], x[0][0])) #ordena e escolhe o maior(melhor)
    escolhido = classificados[0][0]
    return escolhido, candidatos


def _proximas_datas():
    hoje = date.today()
    datas = {}
    for nome, dados in DIAS_ESCALA.items():
        weekday = dados["weekday"]
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
