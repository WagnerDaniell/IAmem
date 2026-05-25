# 📄 PRD — IAmém

## Sistema Inteligente de Escalas da Mídia da Igreja

---

# 📌 Visão Geral

O **IAmém** é um sistema web inteligente desenvolvido para automatizar a criação das escalas da mídia da igreja.

O projeto busca unir conceitos de:

* Inteligência Artificial
* Machine Learning
* Automação de processos

em uma solução prática capaz de gerar escalas automaticamente com base em regras, prioridades e disponibilidade dos integrantes.

O sistema será desenvolvido de forma simples utilizando:

* Backend em Python com Flask
* Frontend em React
* Machine Learning com scikit-learn

---

# 🎯 Objetivo do Projeto

Automatizar o processo de criação das escalas da mídia da igreja, reduzindo:

* tempo gasto na organização manual
* conflitos de escala
* repetições excessivas
* erros humanos

Além disso, o sistema deverá auxiliar na distribuição equilibrada dos integrantes entre os cultos e eventos.

---

# 🧠 Inteligência Artificial e Machine Learning

O sistema utilizará:

* Machine Learning supervisionado
* Árvore de Decisão (Decision Tree)

para auxiliar automaticamente na seleção dos integrantes mais adequados para cada função.

---

# 🌳 Modelo de Machine Learning Escolhido

## Árvore de Decisão

O modelo de Árvore de Decisão foi escolhido por:

* simplicidade de implementação
* fácil interpretação
* boa adaptação ao problema
* tomada de decisão baseada em regras

A árvore analisará critérios como:

* disponibilidade
* prioridade
* frequência recente de participação
* área de atuação
* histórico de escalas

---

# 📌 Funcionamento da IA

A IA analisará perguntas como:

```text id="n5y5yu"
Integrante está disponível?
 ├── Não → Não participa
 └── Sim
       ↓
Possui prioridade alta?
 ├── Sim → Escalar
 └── Não
       ↓
Participou recentemente?
 ├── Sim → Evitar repetição
 └── Não → Escalar
```

---

# ⚙️ Funcionalidades do Sistema

## 👤 Cadastro de Integrantes

O administrador poderá cadastrar:

* Nome
* Área de atuação
* Prioridade
* Disponibilidade

### Áreas disponíveis:

* Som
* Projeção
* Fotografia

---

## 📅 Cadastro de Cultos/Eventos

O administrador poderá:

* Criar cultos
* Definir datas
* Definir quantidade necessária por área

---

## 🤖 Geração Automática de Escala

O sistema irá:

* analisar disponibilidade
* verificar prioridades
* evitar repetições excessivas
* aplicar regras especiais
* gerar escala automaticamente

---

## 📋 Visualização da Escala

O administrador poderá:

* visualizar escala gerada
* editar manualmente caso necessário

---

# 📌 Regras do Sistema

## 🎚️ Som

* Washington possui prioridade máxima
* Caso indisponível:

  * Wagner
  * Heitor

---

## 📽️ Projeção

Sistema realiza rodízio entre:

* Liberanic
* Lailla
* Theo Henry

Evitando repetições consecutivas.

---

## 📸 Fotografia

* Nayara possui prioridade máxima
* Rivail poderá entrar em eventos especiais ou revezamentos

---

# 🧩 Requisitos Funcionais

## RF01

O sistema deve permitir cadastrar integrantes.

## RF02

O sistema deve permitir cadastrar cultos/eventos.

## RF03

O sistema deve permitir definir disponibilidade.

## RF04

O sistema deve gerar escalas automaticamente.

## RF05

O sistema deve aplicar prioridades definidas.

## RF06

O sistema deve evitar repetições excessivas.

## RF07

O sistema deve exibir a escala gerada.

---

# 🛡️ Requisitos Não Funcionais

## RNF01

O sistema deverá possuir interface simples e intuitiva.

## RNF02

O backend será desenvolvido em Python.

## RNF03

O frontend será desenvolvido em React.

## RNF04

O sistema utilizará banco de dados SQLite.

## RNF05

O sistema deverá possuir resposta rápida na geração das escalas.

---

# 🖥️ Tecnologias Utilizadas

## Backend

* Python
* Flask

## Frontend

* React

## Machine Learning

* scikit-learn

## Banco de Dados

* SQLite

---

# 🗂️ Estrutura Básica do Sistema

## Frontend

Telas:

* Login simples
* Cadastro de integrantes
* Cadastro de cultos
* Geração de escala
* Visualização da escala

---

## Backend

Rotas principais:

```text id="ofefy2"
/integrantes
/cultos
/gerar-escala
```

---

# 📊 Estrutura de Dados para IA

## Entradas da Árvore de Decisão

| Critério             | Descrição                       |
| -------------------- | ------------------------------- |
| Disponibilidade      | Se o integrante está disponível |
| Prioridade           | Nível de prioridade             |
| Participação recente | Se participou recentemente      |
| Área                 | Área de atuação                 |
| Frequência           | Quantidade de escalas seguidas  |

---

## Saída do Modelo

| Resultado   |
| ----------- |
| Escalar     |
| Não escalar |

---

# 🎯 Diferencial do Projeto

O diferencial do IAmém é utilizar Inteligência Artificial de forma simples e prática para resolver um problema real enfrentado pelas igrejas na organização das equipes de mídia.

O sistema reduz:

* tempo de organização
* conflitos
* escalas repetitivas
* esforço manual

automatizando decisões através de Machine Learning com Árvore de Decisão.
