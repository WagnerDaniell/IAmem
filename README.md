# 📄 PRD — IAmém

## Sistema Inteligente de Escalas da Mídia da Igreja

---

# 📌 Visão Geral

O **IAmém** é um sistema desktop inteligente desenvolvido para automatizar a criação das escalas da mídia da igreja.

O projeto utiliza conceitos de:

* Inteligência Artificial
* Machine Learning
* Automação de processos

para gerar escalas automaticamente com base em:

* disponibilidade
* prioridade
* frequência de participação
* área de atuação

O sistema será desenvolvido totalmente em Python, utilizando interface gráfica simples para facilitar o uso e reduzir a complexidade do projeto.

---

# 🎯 Objetivo do Projeto

Automatizar a criação das escalas da mídia da igreja, reduzindo:

* tempo gasto na organização manual
* conflitos de escala
* repetições excessivas
* erros humanos

O sistema deverá analisar os integrantes cadastrados e gerar automaticamente a melhor escala possível para cada culto ou evento.

---

# 🧠 Inteligência Artificial e Machine Learning

O sistema utilizará:

* Machine Learning supervisionado
* Árvore de Decisão (Decision Tree)

para auxiliar automaticamente na escolha dos integrantes mais adequados para cada função.

---

# 🌳 Modelo de Machine Learning Escolhido

## Árvore de Decisão

A Árvore de Decisão foi escolhida por:

* simplicidade de implementação
* fácil interpretação
* boa adaptação ao problema
* tomada de decisão baseada em critérios

O modelo analisará:

* disponibilidade
* prioridade
* participação recente
* quantidade de escalas seguidas
* área de atuação

para decidir automaticamente:

* escalar ou não escalar determinado integrante.

---

# ⚙️ Funcionamento da IA

A IA tomará decisões com base em perguntas lógicas.

Exemplo:

```text id="7llg67"
Integrante está disponível?
 ├── Não → Não escala
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

# 🖥️ Tecnologias Utilizadas

| Tecnologia    | Função                    |
| ------------- | ------------------------- |
| Python        | Desenvolvimento principal |
| CustomTkinter | Interface gráfica         |
| scikit-learn  | Machine Learning          |
| SQLite        | Banco de dados local      |

---

# 👤 Cadastro de Integrantes

O sistema permitirá cadastrar integrantes contendo:

* Nome
* Área de atuação
* Prioridade
* Disponibilidade
* Participação recente
* Quantidade de escalas seguidas

---

# 📌 Áreas Disponíveis

* Som
* Projeção
* Fotografia

---

# 📌 Exemplo de Cadastro

| Nome       | Área       | Prioridade | Disponível |
| ---------- | ---------- | ---------- | ---------- |
| Washington | Som        | Alta       | Sim        |
| Nayara     | Fotografia | Máxima     | Sim        |

---

# 🤖 Geração Automática da Escala

Ao clicar no botão “Gerar Escala”, o sistema irá:

1. Buscar integrantes cadastrados
2. Verificar disponibilidade
3. Aplicar prioridades
4. Analisar participação recente
5. Aplicar a Árvore de Decisão
6. Selecionar os melhores integrantes
7. Gerar automaticamente a escala

---

# 📋 Exemplo de Resultado

```text id="z2sazj"
SOM:
- Washington

PROJEÇÃO:
- Lailla

FOTOGRAFIA:
- Nayara
```

---

# 📌 Regras Inteligentes do Sistema

As regras do sistema serão representadas através dos atributos cadastrados dos integrantes.

Exemplo:

| Integrante | Prioridade |
| ---------- | ---------- |
| Washington | Alta       |
| Nayara     | Máxima     |
| Rivail     | Média      |

A IA utilizará essas informações para aprender padrões de escolha.

---

# 🧩 Requisitos Funcionais

## RF01

O sistema deve permitir cadastrar integrantes.

## RF02

O sistema deve permitir editar integrantes.

## RF03

O sistema deve armazenar disponibilidade.

## RF04

O sistema deve gerar escalas automaticamente.

## RF05

O sistema deve aplicar prioridades.

## RF06

O sistema deve evitar repetição excessiva de integrantes.

## RF07

O sistema deve exibir a escala gerada.

---

# 🛡️ Requisitos Não Funcionais

## RNF01

O sistema deverá funcionar localmente.

## RNF02

O sistema deverá possuir interface simples e intuitiva.

## RNF03

O sistema deverá utilizar banco de dados SQLite.

## RNF04

O sistema deverá possuir baixo consumo de recursos.

## RNF05

O sistema deverá gerar escalas rapidamente.

---

# 🧠 Estrutura de Dados da IA

## Entradas (Features)

| Feature              | Descrição                          |
| -------------------- | ---------------------------------- |
| Disponível           | Integrante disponível              |
| Prioridade           | Nível de prioridade                |
| Participação recente | Participou recentemente            |
| Escalas seguidas     | Quantidade de escalas consecutivas |
| Área                 | Área de atuação                    |

---

## Saída da IA

| Resultado   |
| ----------- |
| Escalar     |
| Não escalar |

---

# 🔄 Fluxo BPMN — Usuário

```text id="s4wr2u"
[Início]
   ↓
Usuário abre sistema
   ↓
Cadastra integrantes
   ↓
Define disponibilidade
   ↓
Clica em "Gerar Escala"
   ↓
Sistema envia dados para IA
   ↓
IA analisa critérios
   ↓
Sistema gera escala automática
   ↓
Usuário visualiza resultado
   ↓
[Fim]
```

---

# 🤖 Fluxo BPMN — Inteligência Artificial

```text id="fbl8m5"
[Início]
   ↓
Receber integrantes cadastrados
   ↓
Verificar disponibilidade
   ↓
Separar integrantes por área
   ↓
Analisar prioridades
   ↓
Verificar participação recente
   ↓
Aplicar Árvore de Decisão
   ↓
Selecionar melhores integrantes
   ↓
Gerar escala
   ↓
Exibir resultado
   ↓
[Fim]
```

---

# 📈 Possíveis Melhorias Futuras

* Histórico completo de escalas
* Dashboard administrativo
* Integração com WhatsApp
* Exportação em PDF
* Aprendizado contínuo da IA
* Sistema multi-igrejas

---

# ✅ MVP — Versão Inicial

A primeira versão do sistema terá:

* Cadastro de integrantes
* Interface gráfica simples
* Banco SQLite
* Geração automática de escalas
* Árvore de decisão básica
* Exibição da escala gerada

---

# 🎯 Diferencial do Projeto

O diferencial do IAmém é utilizar Inteligência Artificial de forma prática e acessível para resolver um problema real enfrentado pelas equipes de mídia das igrejas.

O sistema automatiza decisões de escala utilizando Machine Learning com Árvore de Decisão, tornando o processo:

* mais rápido
* mais organizado
* mais equilibrado
* menos manual.
