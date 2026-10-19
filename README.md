# Análise de dados Dataset Duolingo

> **Análise Exploratória de Dados e Dashboard Interativo sobre Retenção de Memória, Repetição Espaçada (SRS) e Dificuldade Lexical com dados reais do Duolingo.**

Dashboard: https://felipe-duolingo-analytics.streamlit.app/

---

## Sobre o Projeto

Este projeto analisa o comportamento de estudantes de idiomas no aplicativo Duolingo, utilizando o **Duolingo SLAM Dataset**. O objetivo é investigar como o tempo decorrido sem prática afeta a taxa de retenção de memória, identificar quais classes gramaticais oferecem maior resistência cognitiva e analisar o padrão de engajamento dos alunos.

Além da pesquisa e validação estatística documentada no Jupyter Notebook, foi desenvolvido um dashboard interativo em Streamlit para exploração dinâmica dos dados.

---

**Fonte:** Duolingo Spaced Repetition Data (Settles & Meeder, 2016), Harvard Dataverse
- **Tamanho:** ~13 milhões de registros de prática de estudantes reais.
- **Recorte usado:** amostra de 200.000 linhas do arquivo (5.130 usuários), por limite de memória.

## Principais Descobertas

### 1. Validação Empírica da Curva do Esquecimento (Ebbinghaus)
* **Retenção Imediata:** Alunos que revisam o vocabulário em **até 1 dia** apresentam taxa média de acerto de **~90,6%**.
* **Decaimento Temporal:** Conforme o intervalo sem prática aumenta, a taxa de acerto cai progressivamente, atingindo **~84,5%** na faixa de 3 meses a 1 ano.
* **Repetição Espaçada (SRS):** O resultado valida a necessidade de algoritmos de repetição espaçada para reativar a memória antes que o vocabulário atinja o limiar crítico de esquecimento.


### 2. Dificuldade de Vocabulário: Substantivos vs. Palavras Gramaticais
* **Palavras Mais Fáceis (~98% de acerto):** Dominadas por **substantivos concretos** (ex: *family, carne, poisson, oil, pantalón*). Por possuírem imagem mental tangível e significado autônomo, são retidas com muito mais facilidade.
* **Palavras Mais Difíceis (~75% a 79% de acerto):** Concentram **conectivos, preposições, artigos e verbos flexionados** (ex: *on, that, que, den, va, sobre*). Por representarem relações conceituais abstratas que dependem de sintaxe e regência, exigem maior esforço cognitivo.

### 3. Distribuição de Engajamento
* A mediana de exercícios praticados por aluno é de apenas **23 lições** (enquanto a média é de ~39), evidenciando o forte atrito de retenção de novos usuários no início da jornada.
* Em contrapartida, um grupo reduzido atinge centenas de sessões (máximo registrado de **798 lições**).

---

## Tecnologias Utilizadas

* **Python 3.14**
* **Pandas & NumPy**
* **Matplotlib & Seaborn**
* **Streamlit**

---

## Autor

Desenvolvido por **Felipe**.  
* [LinkedIn](https://www.linkedin.com/in/felipe-marques-33b304305/)
