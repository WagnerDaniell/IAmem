# IAmém - Documentação Técnica e Acadêmica

## 1. Introdução

O **IAmém** é um sistema desktop desenvolvido em Python para automatizar a geração de escalas da mídia da igreja. O projeto foi pensado para reduzir o trabalho manual de organização e para distribuir os integrantes de forma mais equilibrada ao longo da semana.

A solução combina dois elementos principais:

- **Machine Learning**, para estimar a melhor escolha com base em dados históricos;
- **regras de negócio**, para respeitar limitações práticas como descanso, repetição excessiva e exceções específicas.

O sistema não se comporta como uma simples ordenação por prioridade. Em vez disso, ele tenta equilibrar:

- disponibilidade por dia;
- prioridade do integrante;
- participação recente;
- escalas seguidas;
- área de atuação;
- feedback humano registrado após a geração.

---

## 2. Objetivo

O objetivo do projeto é automatizar o processo de criação de escalas, mantendo a decisão:

- mais rápida;
- mais organizada;
- mais justa;
- mais próxima da realidade da equipe.

Além de gerar a escala, o sistema também aprende com o retorno humano, permitindo um ciclo contínuo de melhoria.

---

## 3. Tecnologias Utilizadas

| Tecnologia | Função |
| --- | --- |
| Python | Linguagem principal do sistema |
| CustomTkinter | Interface gráfica |
| SQLite | Persistência local dos dados |
| Pandas | Manipulação dos dados de treino |
| Scikit-learn | Modelo de Machine Learning |
| Matplotlib | Visualização da árvore de decisão |

---

## 4. Estrutura do Projeto

### Arquivos principais

| Arquivo | Responsabilidade |
| --- | --- |
| [`main.py`](./main.py) | Ponto de entrada da aplicação |
| [`src/context/database.py`](./src/context/database.py) | Inicialização do banco e operações CRUD |
| [`src/services/gerador_escala.py`](./src/services/gerador_escala.py) | Treino do modelo e geração da escala |
| [`src/view/interface.py`](./src/view/interface.py) | Janela principal |
| [`src/view/integrantes.py`](./src/view/integrantes.py) | Cadastro e edição de integrantes |
| [`src/view/escalas.py`](./src/view/escalas.py) | Tela de geração e feedback das escalas |

### Estrutura de pastas

```text
IAmem/
├── data/
│   ├── iamem.db
│   └── seed_integrantes.sql
├── src/
│   ├── context/
│   │   └── database.py
│   ├── services/
│   │   └── gerador_escala.py
│   └── view/
│       ├── interface.py
│       ├── integrantes.py
│       └── escalas.py
├── main.py
├── README.md
└── DOCUMENTACAO.md
```

---

## 5. Visão Geral do Sistema

O sistema segue um ciclo simples e contínuo:

1. o usuário cadastra os integrantes;
2. o sistema armazena disponibilidade, prioridade e histórico;
3. a escala é gerada automaticamente;
4. o resultado é exibido na interface;
5. o usuário avalia os nomes sugeridos;
6. o feedback é salvo no banco;
7. o modelo é re-treinado com base nas avaliações válidas.

Esse fluxo transforma o sistema em uma solução **híbrida**, pois ele não depende apenas da árvore de decisão, nem apenas de regras fixas.

---

## 6. Fluxo de Geração da Escala

Esta seção descreve o processo completo, em ordem exata, desde o clique do usuário até a exibição da escala.

### 6.1 Fluxo geral

| Etapa | O que acontece |
| --- | --- |
| 1 | O usuário clica em **Gerar Escala da Semana** |
| 2 | A interface chama `gerar_escala_semana()` |
| 3 | O sistema garante que o modelo esteja carregado |
| 4 | Os integrantes são lidos do banco SQLite |
| 5 | O sistema calcula as próximas datas de Domingo, Quarta e Sexta |
| 6 | Para cada dia, o sistema percorre as áreas Som, Projecao e Fotografia |
| 7 | Os candidatos são filtrados por área e disponibilidade |
| 8 | Cada candidato é convertido em features numéricas/categóricas |
| 9 | A árvore de decisão estima a probabilidade de escolha |
| 10 | O score final recebe ajustes de regras de negócio |
| 11 | O integrante com maior pontuação é selecionado |
| 12 | A escala é salva no banco |
| 13 | O histórico é atualizado |
| 14 | O feedback técnico de contexto é registrado |
| 15 | O resultado é exibido na interface |

### 6.2 Pseudo-fluxo técnico

```text
Clique em "Gerar Escala"
    ↓
Carregar integrantes do banco
    ↓
Calcular datas da semana
    ↓
Para cada dia
    ↓
    Para cada área
        ↓
        Filtrar disponíveis
        ↓
        Montar features
        ↓
        Passar pela árvore de decisão
        ↓
        Aplicar regras de negócio
        ↓
        Selecionar candidato final
        ↓
        Registrar no banco
    ↓
Salvar escala semanal
    ↓
Atualizar histórico e feedback
    ↓
Exibir resultado
```

---

## 7. Quando o Feedback é Usado

Este ponto é central para entender o comportamento do sistema.

### 7.1 Feedback durante a geração

Quando a escala é gerada, o sistema grava uma linha em `feedback_escala` para cada candidato considerado.

Nessa etapa:

- `foi_escalado` recebe `1` para o escolhido;
- os demais candidatos recebem `0`;
- `avaliacao` permanece `NULL`.

Isso significa que o sistema está registrando **contexto de geração**, mas ainda não está aprendendo supervisionadamente com esse dado.

### 7.2 Feedback manual do usuário

Depois da geração, o usuário pode avaliar a escala com:

- 👍 para uma boa escolha;
- 👎 para uma escolha ruim.

Quando isso acontece:

- o campo `avaliacao` recebe um valor;
- esse valor passa a ser o rótulo de aprendizado do modelo.

### 7.3 Quando o modelo aprende de fato

O modelo só considera os registros de `feedback_escala` que tenham:

- `avaliacao IS NOT NULL`

Em termos práticos:

- gerar a escala não treina o modelo sozinho;
- o aprendizado acontece quando o humano avalia os resultados;
- o próximo treino usa apenas avaliações válidas.

### 7.4 Ciclo de aprendizado

```text
Gerar escala
    ↓
Salvar contexto dos candidatos
    ↓
Usuário avalia
    ↓
Gravar avaliacao no banco
    ↓
Re-treinar o modelo
    ↓
Usar aprendizado na próxima geração
```

---

## 8. Modelo de Machine Learning

### 8.1 Tipo de modelo

O modelo utilizado é uma **Árvore de Decisão** (`DecisionTreeClassifier`), da biblioteca `scikit-learn`.

### 8.2 Justificativa da escolha

A árvore de decisão foi escolhida porque:

- é simples de interpretar;
- funciona bem com regras condicionais;
- permite visualizar a lógica de decisão;
- se adapta bem a problemas com atributos mistos;
- é útil quando queremos explicar por que uma escolha foi feita.

### 8.3 Entradas do modelo

| Feature | Descrição |
| --- | --- |
| `disponivel_dia` | Indica se o integrante está disponível naquele dia |
| `prioridade` | Nível de prioridade cadastrado |
| `participacao_recente` | Indica se o integrante participou recentemente |
| `escalas_seguidas` | Quantidade de escalas consecutivas |
| `area` | Área de atuação do integrante |

### 8.4 Saída do modelo

| Saída | Significado |
| --- | --- |
| `1` | Escalar |
| `0` | Não escalar |

### 8.5 Como o treino funciona

O treino usa:

- dados reais já avaliados;
- um dataset mínimo de fallback quando ainda existem poucos dados.

Isso evita falhas na primeira execução e garante que o modelo tenha condições de operar mesmo em fase inicial.

---

## 9. Lógica de Seleção

O sistema não usa apenas a árvore de decisão de forma isolada. Ele calcula uma pontuação final combinando o resultado do modelo com regras de negócio.

### 9.1 Elementos que compõem o score

| Componente | Efeito |
| --- | --- |
| Probabilidade da árvore | Mede a tendência de escolha |
| Bônus de prioridade | Favorece prioridades mais altas |
| Penalidade por participação recente | Reduz repetição excessiva |
| Penalidade por escalas seguidas | Reduz sobrecarga |
| Penalidade por repetição histórica | Evita repetir o mesmo nome com muita frequência |
| Regra fixa | Pode sobrescrever a pontuação em casos específicos |

### 9.2 Regra especial do Washington

Em `Som`, o sistema possui uma exceção explícita para **Washington**.

Na prática:

- se ele estiver disponível;
- e estiver na área correta;
- ele é priorizado.

Essa regra foi tratada como exceção de negócio, e não como comportamento geral do modelo.

### 9.3 Equilíbrio entre ML e regras

| Parte | Responsabilidade |
| --- | --- |
| ML | Estimar a melhor tendência de escolha |
| Regras | Garantir equilíbrio e comportamento esperado |

Isso é importante porque o sistema é híbrido: o modelo prevê, mas as regras impedem decisões ruins ou repetitivas.

---

## 10. Banco de Dados

O banco é local e fica em:

```text
data/iamem.db
```

### 10.1 Tabelas principais

#### `integrantes`

Armazena os dados base de cada integrante.

| Campo | Função |
| --- | --- |
| `id` | Identificador |
| `nome` | Nome do integrante |
| `area` | Área de atuação |
| `prioridade` | Prioridade cadastrada |
| `disponivel_quarta` | Disponibilidade na quarta-feira |
| `disponivel_sexta` | Disponibilidade na sexta-feira |
| `disponivel_domingo` | Disponibilidade no domingo |
| `participacao_recente` | Se participou recentemente |
| `escalas_seguidas` | Quantidade de escalas seguidas |

#### `escalas`

Armazena a escala gerada por dia.

| Campo | Função |
| --- | --- |
| `id` | Identificador |
| `data_escala` | Data da escala |
| `som` | Nome escalado para som |
| `projecao` | Nome escalado para projeção |
| `fotografia` | Nome escalado para fotografia |

#### `feedback_escala`

Armazena o histórico usado para aprendizado supervisionado.

| Campo | Função |
| --- | --- |
| `data_escala` | Data relacionada à decisão |
| `area` | Área da decisão |
| `integrante_id` | Integrante avaliado |
| `foi_escalado` | Indica se foi o escolhido |
| `disponivel_dia` | Disponibilidade naquele dia |
| `prioridade` | Prioridade no momento da decisão |
| `participacao_recente` | Histórico recente |
| `escalas_seguidas` | Sequência de escalas |
| `area_atuacao` | Área original do integrante |
| `avaliacao` | Rótulo supervisionado definido pelo usuário |

---

## 11. Dados de Demonstração

O projeto pode carregar um seed inicial caso a tabela `integrantes` esteja vazia.

### Arquivo de seed

[`data/seed_integrantes.sql`](./data/seed_integrantes.sql)

### Objetivo

Esses dados existem para:

- facilitar testes iniciais;
- permitir visualizar a escala logo no primeiro uso;
- evitar uma aplicação vazia durante demonstrações.

### Regra de carregamento

O seed é executado apenas se:

- a tabela `integrantes` existir;
- e estiver vazia.

Se já houver dados reais, o seed não é reaplicado.

---

## 12. Fluxo de Feedback e Re-treino

### 12.1 Fluxo operacional

| Ação | Resultado |
| --- | --- |
| Gerar escala | Registra contexto técnico no banco |
| Avaliar com 👍 ou 👎 | Define o rótulo supervisionado |
| Clicar em re-treinar | Recalcula o modelo com dados avaliados |

### 12.2 Quando o modelo usa os dados de feedback

O uso acontece somente quando:

- o registro possui `avaliacao`;
- o sistema precisa treinar novamente;
- o usuário aciona o re-treino manual.

### 12.3 Consequência prática

O sistema melhora com o tempo, mas apenas se houver:

- avaliações reais;
- histórico suficiente;
- consistência nos dados cadastrados.

---

## 13. Limitações e Observações

Mesmo sendo funcional, o sistema possui limitações naturais:

- depende da qualidade dos dados cadastrados;
- depende do feedback humano;
- com pouco histórico, o aprendizado é limitado;
- a árvore de decisão não substitui completamente regras humanas;
- o resultado final é híbrido, não puramente estatístico.

---

## 14. Como Executar

### Requisitos

Instalar as dependências do `requirements.txt`.

### Execução

```bash
python main.py
```

Ao iniciar:

- o banco é inicializado;
- o seed é carregado, se necessário;
- a interface principal é aberta.

---

## 15. Síntese Acadêmica

Do ponto de vista acadêmico, o IAmém pode ser descrito como um sistema de apoio à decisão baseado em Machine Learning supervisionado, com pós-processamento por regras de negócio.

Essa abordagem permite:

- automatizar a geração de escalas;
- incorporar conhecimento humano;
- registrar histórico;
- aprender com avaliações;
- manter a distribuição de integrantes mais equilibrada.

---

## 16. Resumo Técnico do Pipeline

```text
Cadastro de integrantes
    ↓
Persistência em SQLite
    ↓
Treino da árvore com feedback avaliado
    ↓
Geração da escala semanal
    ↓
Filtragem por disponibilidade e área
    ↓
Score do modelo + regras de negócio
    ↓
Seleção do integrante
    ↓
Salvamento da escala
    ↓
Coleta de feedback humano
    ↓
Novo treino
```

---

## 17. Conclusão

O IAmém foi projetado para unir automação, aprendizado supervisionado e regras de negócio em um único fluxo de trabalho. Na prática, isso produz uma solução mais explicável do que um modelo puramente estatístico e mais inteligente do que uma regra fixa manual.

O resultado é um sistema que:

- gera escalas automaticamente;
- aprende com avaliações;
- evita repetição excessiva;
- respeita exceções reais da equipe;
- mantém a lógica clara para manutenção e apresentação.

