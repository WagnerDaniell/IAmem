# IAmem - Documentacao Tecnica e Academica

## 1. Introducao

O **IAmem** e um sistema desktop desenvolvido em Python para automatizar a geracao de escalas da midia da igreja. O projeto foi pensado para reduzir o trabalho manual de organizacao e para distribuir os integrantes de forma mais inteligente ao longo da semana.

A solucao utiliza **Machine Learning supervisionado** como mecanismo principal de decisao. O codigo mantem apenas filtros minimos de viabilidade, como:

- area correta;
- disponibilidade no dia.

Todo o restante da escolha final e responsabilidade da arvore de decisao.

O sistema nao se comporta como uma simples ordenacao por prioridade. Em vez disso, ele aprende padroes a partir de:

- disponibilidade por dia;
- prioridade do integrante;
- participacao recente;
- escalas seguidas;
- area de atuacao;
- dia da semana;
- identificador do integrante;
- feedback humano registrado apos a geracao.

Esse fluxo transforma o sistema em uma solucao orientada principalmente por ML, com validacoes minimas antes da previsao.

---

## 2. Objetivo

O objetivo do projeto e automatizar o processo de criacao de escalas, mantendo a decisao:

- mais rapida;
- mais organizada;
- mais inteligente;
- mais proxima da realidade da equipe.

Alm de gerar a escala, o sistema tambem aprende com o retorno humano, permitindo um ciclo continuo de melhoria.

---

## 3. Tecnologias Utilizadas

| Tecnologia | Funcao |
| --- | --- |
| Python | Linguagem principal do sistema |
| CustomTkinter | Interface grafica |
| SQLite | Persistencia local dos dados |
| Pandas | Manipulacao dos dados de treino |
| Scikit-learn | Modelo de Machine Learning |
| Matplotlib | Visualizacao da arvore de decisao |

---

## 4. Estrutura do Projeto

### Arquivos principais

| Arquivo | Responsabilidade |
| --- | --- |
| [`main.py`](./main.py) | Ponto de entrada da aplicacao |
| [`src/context/database.py`](./src/context/database.py) | Inicializacao do banco e operacoes CRUD |
| [`src/services/gerador_escala.py`](./src/services/gerador_escala.py) | Treino do modelo e geracao da escala |
| [`src/view/interface.py`](./src/view/interface.py) | Janela principal |
| [`src/view/integrantes.py`](./src/view/integrantes.py) | Cadastro e edicao de integrantes |
| [`src/view/escalas.py`](./src/view/escalas.py) | Tela de geracao e feedback das escalas |

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

## 5. Visao Geral do Sistema

O sistema segue um ciclo simples e continuo:

1. o usuario cadastra os integrantes;
2. o sistema armazena disponibilidade, prioridade e historico;
3. a escala e gerada automaticamente;
4. o resultado e exibido na interface;
5. o usuario avalia os nomes sugeridos;
6. o feedback e salvo no banco;
7. o modelo e re-treinado com base nas avaliacoes validas.

Esse fluxo faz com que o sistema aprenda ao longo do tempo sem depender de regras manuais para decidir o resultado final.

---

## 6. Fluxo de Geracao da Escala

Esta secao descreve o processo completo, em ordem exata, desde o clique do usuario ate a exibicao da escala.

### 6.1 Fluxo geral

| Etapa | O que acontece |
| --- | --- |
| 1 | O usuario clica em **Gerar Escala da Semana** |
| 2 | A interface chama `gerar_escala_semana()` |
| 3 | O sistema garante que o modelo esteja carregado |
| 4 | Os integrantes sao lidos do banco SQLite |
| 5 | O sistema calcula as proximas datas de Domingo, Quarta e Sexta |
| 6 | Para cada dia, o sistema percorre as areas Som, Projecao e Fotografia |
| 7 | Os candidatos sao filtrados por area e disponibilidade |
| 8 | Cada candidato e convertido em features numericas/categoricas |
| 9 | A arvore de decisao estima a probabilidade de escolha |
| 10 | O modelo escolhe o candidato com maior probabilidade entre os viaveis |
| 11 | A escala e salva no banco |
| 12 | O historico e atualizado |
| 13 | O feedback tecnico de contexto e registrado |
| 14 | O resultado e exibido na interface |

### 6.2 Pseudo-fluxo tecnico

```text
Clique em "Gerar Escala"
    ↓
Carregar integrantes do banco
    ↓
Calcular datas da semana
    ↓
Para cada dia
    ↓
    Para cada area
        ↓
        Filtrar disponiveis
        ↓
        Montar features
        ↓
        Passar pela arvore de decisao
        ↓
        Selecionar candidato final
        ↓
        Registrar no banco
    ↓
Salvar escala semanal
    ↓
Atualizar historico e feedback
    ↓
Exibir resultado
```

---

## 7. Quando o Feedback e Usado

Este ponto e central para entender o comportamento do sistema.

### 7.1 Feedback durante a geracao

Quando a escala e gerada, o sistema grava uma linha em `feedback_escala` para cada candidato considerado.

Nessa etapa:

- `foi_escalado` recebe `1` para o escolhido;
- os demais candidatos recebem `0`;
- `avaliacao` permanece `NULL`.

Isso significa que o sistema esta registrando **contexto de geracao**, mas ainda nao esta aprendendo supervisionadamente com esse dado.

### 7.2 Feedback manual do usuario

Depois da geracao, o usuario pode avaliar a escala com:

- 👍 para uma boa escolha;
- 👎 para uma escolha ruim.

Quando isso acontece:

- o campo `avaliacao` recebe um valor;
- esse valor passa a ser o rotulo de aprendizado do modelo.

### 7.3 Quando o modelo aprende de fato

O modelo so considera os registros de `feedback_escala` que tenham:

- `avaliacao IS NOT NULL`

Em termos praticos:

- gerar a escala nao treina o modelo sozinho;
- o aprendizado acontece quando o humano avalia os resultados;
- o proximo treino usa apenas avaliacoes validas.

### 7.4 Ciclo de aprendizado

```text
Gerar escala
    ↓
Salvar contexto dos candidatos
    ↓
Usuario avalia
    ↓
Gravar avaliacao no banco
    ↓
Re-treinar o modelo
    ↓
Usar aprendizado na proxima geracao
```

---

## 8. Modelo de Machine Learning

### 8.1 Tipo de modelo

O modelo utilizado e uma **Arvore de Decisao** (`DecisionTreeClassifier`), da biblioteca `scikit-learn`.

### 8.2 Justificativa da escolha

A arvore de decisao foi escolhida porque:

- e simples de interpretar;
- funciona bem com relacoes condicionais;
- permite visualizar a logica de decisao;
- se adapta bem a problemas com atributos mistos;
- e util quando queremos explicar por que uma escolha foi feita.

### 8.3 Entradas do modelo

| Feature | Descricao |
| --- | --- |
| `disponivel_dia` | Indica se o integrante esta disponivel naquele dia |
| `prioridade` | Nivel de prioridade cadastrado |
| `participacao_recente` | Indica se o integrante participou recentemente |
| `escalas_seguidas` | Quantidade de escalas consecutivas |
| `area` | Area de atuacao do integrante |
| `dia_semana` | Dia da escala avaliado |
| `integrante_id` | Identificador do integrante |

### 8.4 Saida do modelo

| Saida | Significado |
| --- | --- |
| `1` | Escalar |
| `0` | Nao escalar |

### 8.5 Como o treino funciona

O treino usa:

- dados reais ja avaliados;
- um dataset minimo de fallback quando ainda existem poucos dados.

Isso evita falhas na primeira execucao e garante que o modelo tenha condicoes de operar mesmo em fase inicial.

---

## 9. Logica de Selecao

O sistema usa a arvore de decisao de forma direta sobre os candidatos viaveis. Nao ha bonus, penalidades ou excecoes manuais na decisao final.

### 9.1 Elementos que compoem a decisao

| Componente | Efeito |
| --- | --- |
| Probabilidade da arvore | Mede a tendencia de escolha |
| Filtros minimos | Eliminam candidatos fora da area ou indisponiveis |

### 9.2 Papel dos filtros minimos

Os filtros minimos nao decidem quem ganha a vaga. Eles apenas garantem que a arvore receba candidatos que fazem sentido para aquela area e para aquele dia.

### 9.3 Papel do modelo

| Parte | Responsabilidade |
| --- | --- |
| ML | Escolher o candidato com maior probabilidade aprendida |
| Filtros minimos | Garantir viabilidade operacional |

---

## 10. Banco de Dados

O banco e local e fica em:

```text
data/iamem.db
```

### 10.1 Tabelas principais

#### `integrantes`

Armazena os dados base de cada integrante.

| Campo | Funcao |
| --- | --- |
| `id` | Identificador |
| `nome` | Nome do integrante |
| `area` | Area de atuacao |
| `prioridade` | Prioridade cadastrada |
| `disponivel_quarta` | Disponibilidade na quarta-feira |
| `disponivel_sexta` | Disponibilidade na sexta-feira |
| `disponivel_domingo` | Disponibilidade no domingo |
| `participacao_recente` | Se participou recentemente |
| `escalas_seguidas` | Quantidade de escalas seguidas |

#### `escalas`

Armazena a escala gerada por dia.

| Campo | Funcao |
| --- | --- |
| `id` | Identificador |
| `data_escala` | Data da escala |
| `som` | Nome escalado para som |
| `projecao` | Nome escalado para projecao |
| `fotografia` | Nome escalado para fotografia |

#### `feedback_escala`

Armazena o historico usado para aprendizado supervisionado.

| Campo | Funcao |
| --- | --- |
| `data_escala` | Data relacionada a decisao |
| `area` | Area da decisao |
| `integrante_id` | Integrante avaliado |
| `foi_escalado` | Indica se foi o escolhido |
| `disponivel_dia` | Disponibilidade naquele dia |
| `prioridade` | Prioridade no momento da decisao |
| `participacao_recente` | Historico recente |
| `escalas_seguidas` | Sequencia de escalas |
| `area_atuacao` | Area original do integrante |
| `avaliacao` | Rotulo supervisionado definido pelo usuario |

Esses dois campos extras, `dia_semana` e `integrante_id`, sao importantes porque permitem que o feedback tenha efeito mais especifico sobre a combinacao pessoa + contexto.

---

## 11. Dados de Demonstracao

O projeto pode carregar um seed inicial caso a tabela `integrantes` esteja vazia.

### Arquivo de seed

[`data/seed_integrantes.sql`](./data/seed_integrantes.sql)

### Objetivo

Esses dados existem para:

- facilitar testes iniciais;
- permitir visualizar a escala logo no primeiro uso;
- evitar uma aplicacao vazia durante demonstracoes;
- fornecer exemplos supervisionados iniciais para o modelo.

### Regra de carregamento

O seed e executado apenas se:

- a tabela `integrantes` existir;
- e estiver vazia.

Se ja houver dados reais, o seed nao e reaplicado.

---

## 12. Fluxo de Feedback e Re-treino

### 12.1 Fluxo operacional

| Acao | Resultado |
| --- | --- |
| Gerar escala | Registra contexto tecnico no banco |
| Avaliar com 👍 ou 👎 | Define o rotulo supervisionado |
| Clicar em 👍 ou 👎 | Atualiza o feedback usado no proximo treino |

### 12.2 Quando o modelo usa os dados de feedback

O uso acontece somente quando:

- o registro possui `avaliacao`;
- o sistema faz o re-treino a partir do feedback registrado.

### 12.3 Consequencia pratica

O sistema melhora com o tempo, mas apenas se houver:

- avaliacoes reais;
- historico suficiente;
- consistencia nos dados cadastrados.

---

## 13. Limitacoes e Observacoes

Mesmo sendo funcional, o sistema possui limitacoes naturais:

- depende da qualidade dos dados cadastrados;
- depende do feedback humano;
- com pouco historico, o aprendizado e limitado;
- a arvore de decisao depende da qualidade do treino;
- com poucos dados reais, o sistema ainda usa fallback sintetico.

---

## 14. Como Executar

### Requisitos

Instalar as dependencias do `requirements.txt`.

### Execucao

```bash
python main.py
```

Ao iniciar:

- o banco e inicializado;
- o seed e carregado, se necessario;
- a interface principal e aberta.

---

## 15. Sintese Academica

Do ponto de vista academico, o IAmem pode ser descrito como um sistema de apoio a decisao baseado em Machine Learning supervisionado, com filtros minimos de viabilidade.

Essa abordagem permite:

- automatizar a geracao de escalas;
- incorporar conhecimento humano;
- registrar historico;
- aprender com avaliacoes;
- manter a distribuicao de integrantes mais coerente com os dados.

---

## 16. Resumo Tecnico do Pipeline

```text
Cadastro de integrantes
    ↓
Persistencia em SQLite
    ↓
Treino da arvore com feedback avaliado
    ↓
Geracao da escala semanal
    ↓
Filtragem por disponibilidade e area
    ↓
Predicao do modelo
    ↓
Selecao do integrante
    ↓
Salvamento da escala
    ↓
Coleta de feedback humano
    ↓
Novo treino
```

---

## 17. Conclusao

O IAmem foi projetado para unir automacao e aprendizado supervisionado em um unico fluxo de trabalho. Na pratica, isso produz uma solucao mais explicavel do que um modelo puramente estatistico e mais inteligente do que uma regra fixa manual.

O resultado e um sistema que:

- gera escalas automaticamente;
- aprende com avaliacoes;
- respeita criterios operacionais minimos;
- mantem a logica clara para manutencao e apresentacao.
