import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Duolingo - Análise de Aprendizado",
    page_icon="🦉",
    layout="wide"
)

# Paleta oficial Duolingo
VERDE_DUO = "#58cc02"
VERDE_ESCURO = "#46a302"
VERMELHO_DUO = "#ff4b4b"

@st.cache_data
def carregar_dados():
    caminho_amostra = "data/duolingo_sample_200k.csv.gz"
    caminho_completo = "data/settles.acl16.learning_traces.13m.csv.gz"
    caminho = caminho_amostra if os.path.exists(caminho_amostra) else caminho_completo

    df = pd.read_csv(caminho, nrows=200_000)
    df["palavra_limpa"] = df["lexeme_string"].str.split("/").str[0]
    df["dias_sem_revisao"] = df["delta"] / 86400
    
    periodos = [-1, 1, 7, 14, 30, 90, 365, float("inf")]
    labels = ["Até 1 dia", "1 a 7 dias", "7 a 14 dias", "14 a 30 dias", "1 a 3 meses", "3 meses a 1 ano", "Mais de 1 ano"]
    df["faixa_tempo"] = pd.cut(df["dias_sem_revisao"], bins=periodos, labels=labels)
    return df

df = carregar_dados()

# Barra lateral com filtros
st.sidebar.title("Análise Idiomas (SRS) - Duolingo")
st.sidebar.markdown("Explore os padrões de memorização e aprendizado.")

idiomas = {
    "Todos": "Todos os idiomas",
    "en": "Inglês (en)",
    "es": "Espanhol (es)",
    "fr": "Francês (fr)",
    "de": "Alemão (de)",
    "it": "Italiano (it)",
    "pt": "Português (pt)"
}

opcao_idioma = st.sidebar.selectbox("Filtrar por Idioma:", list(idiomas.keys()), format_func=lambda x: idiomas[x])
freq_minima = st.sidebar.slider("Frequência mínima da palavra:", 20, 120, 60, step=10)

if opcao_idioma != "Todos":
    df_filtrado = df[df["learning_language"] == opcao_idioma]
else:
    df_filtrado = df

# Título da página
st.title("🦉 Análise de Aprendizado de Idiomas")
st.caption("Métricas de retenção de memória, esquecimento e vocabulário no Duolingo")

# Indicadores (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Exercícios", f"{len(df_filtrado):,}".replace(",", "."))
col2.metric("Média de Acerto", f"{df_filtrado['p_recall'].mean() * 100:.1f}%")
col3.metric("Total de Usuários", f"{df_filtrado['user_id'].nunique():,}".replace(",", "."))
col4.metric("Palavras Únicas", f"{df_filtrado['palavra_limpa'].nunique():,}".replace(",", "."))

st.divider()

# Abas de navegação
aba1, aba2, aba3 = st.tabs(["Curva do Esquecimento", "Dificuldade das Palavras", "Engajamento dos Alunos"])

with aba1:
    st.subheader("Curva do Esquecimento (Ebbinghaus)")
    st.write("Relação entre o tempo decorrido desde a última revisão e a taxa de acerto do aluno.")

    retencao = df_filtrado.groupby("faixa_tempo", observed=False).agg(
        total_exercicios=("p_recall", "count"),
        taxa_acerto=("p_recall", "mean")
    ).reset_index()

    col_graf, col_tab = st.columns([3, 2])

    with col_graf:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        sns.lineplot(
            data=retencao,
            x="faixa_tempo",
            y="taxa_acerto",
            marker="o",
            color=VERDE_DUO,
            linewidth=3,
            markersize=8,
            ax=ax
        )
        ax.set_ylim(0.75, 1.0)
        ax.set_xlabel("Tempo sem Revisão")
        ax.set_ylabel("Taxa Média de Acerto (p_recall)")
        ax.grid(True, linestyle="--", alpha=0.4)
        plt.xticks(rotation=20)
        st.pyplot(fig)

    with col_tab:
        tabela_exibicao = retencao.copy()
        tabela_exibicao["taxa_acerto"] = (tabela_exibicao["taxa_acerto"] * 100).map("{:.2f}%".format)
        tabela_exibicao.columns = ["Faixa de Tempo", "Exercícios", "Taxa de Acerto"]
        st.dataframe(tabela_exibicao, hide_index=True, width="stretch")

with aba2:
    st.subheader(f"Top 10 Palavras Mais Fáceis e Mais Difíceis (mínimo de {freq_minima} aparições)")
    
    palavras = df_filtrado.groupby(["palavra_limpa", "learning_language"]).agg(
        total_vezes=("p_recall", "count"),
        media_acerto=("p_recall", "mean")
    ).reset_index()

    palavras_freq = palavras[palavras["total_vezes"] >= freq_minima]

    if len(palavras_freq) >= 20:
        dificeis = palavras_freq.sort_values(by="media_acerto", ascending=True).head(10)
        faceis = palavras_freq.sort_values(by="media_acerto", ascending=False).head(10).sort_values(by="media_acerto", ascending=True)

        col_d, col_f = st.columns(2)

        with col_d:
            st.markdown("##### Mais Difíceis")
            fig_d, ax_d = plt.subplots(figsize=(6, 4))
            sns.barplot(data=dificeis, y="palavra_limpa", x="media_acerto", color=VERMELHO_DUO, ax=ax_d)
            ax_d.set_xlim(0.65, 1.0)
            ax_d.set_xlabel("Taxa Média de Acerto")
            ax_d.set_ylabel("Palavra")
            ax_d.grid(axis="x", linestyle="--", alpha=0.4)
            st.pyplot(fig_d)

        with col_f:
            st.markdown("##### Mais Fáceis")
            fig_f, ax_f = plt.subplots(figsize=(6, 4))
            sns.barplot(data=faceis, y="palavra_limpa", x="media_acerto", color=VERDE_DUO, ax=ax_f)
            ax_f.set_xlim(0.65, 1.0)
            ax_f.set_xlabel("Taxa Média de Acerto")
            ax_f.set_ylabel("Palavra")
            ax_f.grid(axis="x", linestyle="--", alpha=0.4)
            st.pyplot(fig_f)
    else:
        st.warning(f"Poucas palavras com pelo menos {freq_minima} aparições para este filtro. Experimente diminuir a frequência na barra lateral.")

with aba3:
    st.subheader("Distribuição de Engajamento por Aluno")

    usuarios = df_filtrado.groupby("user_id").agg(
        total_licoes=("p_recall", "count")
    ).reset_index()

    col_h, col_s = st.columns([3, 2])

    with col_h:
        fig_u, ax_u = plt.subplots(figsize=(8, 4.5))
        sns.histplot(usuarios["total_licoes"], bins=60, kde=True, color=VERDE_ESCURO, ax=ax_u)
        ax_u.set_xlabel("Total de Exercícios por Usuário")
        ax_u.set_ylabel("Número de Usuários")
        ax_u.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig_u)

    with col_s:
        st.markdown("**Resumo Descritivo:**")
        stats = usuarios["total_licoes"].describe()
        df_resumo = pd.DataFrame({
            "Métrica": ["Usuários", "Média", "Mínimo", "25% (Q1)", "50% (Mediana)", "75% (Q3)", "Máximo"],
            "Valor": [
                f"{stats['count']:.0f}",
                f"{stats['mean']:.1f}",
                f"{stats['min']:.0f}",
                f"{stats['25%']:.0f}",
                f"{stats['50%']:.0f}",
                f"{stats['75%']:.0f}",
                f"{stats['max']:.0f}"
            ]
        })
        st.dataframe(df_resumo, hide_index=True, width="stretch")
