"""
Dashboard de Acompanhamento de Projetos de Saneamento — Biancade.
Página única, sem abas, com filtros transversais (cartões + tabela + feed).
"""

import streamlit as st
import pandas as pd

import logging
from datetime import datetime
from modules import parser, storage, visuals, comparator, history

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Saneamento — Biancade",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS — paleta Biancade
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #F5F2EE;
        border-right: 1px solid #E0D9CF;
    }
    h1, h2, h3 { color: #000000; font-weight: 700; }
    hr { border: none; height: 1px; background: #E0D9CF; margin: 16px 0; }
    div[data-testid="stDataFrame"] thead th {
        background-color: #423725 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
storage.inicializar_session_state()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

TIPO_PASTA = {"ETA": "etas", "Captação": "captacoes", "ETE": "etes"}


def _label_versao(nome: str, data: datetime | None) -> str:
    d = data.strftime("%d/%m/%Y") if data else "—"
    return f"{d} — {nome}"


# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        "<div style='padding:12px 0 4px 0;'>"
        "<span style='font-size:1.3em;font-weight:700;color:#423725;'>"
        "Dashboard Saneamento</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    # ---- Tipo de projeto ----
    tipo_selecionado = st.selectbox(
        "Tipo de projeto",
        ["ETA", "Captação", "ETE"],
        key="tipo_selecionado",
    )

    # ---- Listar versões do GitHub ----
    versoes = st.session_state.arquivos.get(tipo_selecionado, [])

    if not versoes:
        with st.spinner("Carregando versões…"):
            versoes = storage.listar_versoes(tipo_selecionado)
            st.session_state.arquivos[tipo_selecionado] = versoes

    if versoes:
        labels = [_label_versao(n, d) for n, d, _ in versoes]

        idx_a = st.selectbox(
            "Versão ativa ★",
            range(len(labels)),
            format_func=lambda i: labels[i],
            index=0,
            key="idx_versao_a",
        )
        st.session_state.versao_a = versoes[idx_a]

        # ---- Modo comparação ----
        if not st.session_state.modo_comparacao:
            if st.button("🔄 Comparar versões", use_container_width=True):
                st.session_state.modo_comparacao = True
                st.rerun()
        else:
            idx_b_default = min(idx_a + 1, len(versoes) - 1)
            idx_b = st.selectbox(
                "Comparar com",
                range(len(labels)),
                format_func=lambda i: labels[i],
                index=idx_b_default,
                key="idx_versao_b",
            )
            st.session_state.versao_b = versoes[idx_b]
            if st.button("✕ Cancelar comparação", use_container_width=True):
                st.session_state.modo_comparacao = False
                st.rerun()
    else:
        st.info("Nenhuma versão no GitHub. Faça upload para começar.")

    # ---- Filtros ativos (lista + limpar) ----
    filtros = st.session_state.filtros_ativos
    if filtros:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("**Filtros ativos:**")
        for k, v in filtros.items():
            st.caption(f"• {k}: {v}")
        if st.button("✕ Limpar filtros", use_container_width=True):
            st.session_state.filtros_ativos = {}
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ---- Upload (expander, colapsado) ----
    with st.expander("📤 Upload / Administração", expanded=False):
        senha_input = st.text_input("Senha admin", type="password", key="senha_admin")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Entrar", use_container_width=True):
                if storage.verificar_autenticacao(senha_input):
                    st.session_state.autenticado = True
                    st.success("Autenticado")
                else:
                    st.error("Senha incorreta")
        with col_b:
            if st.session_state.autenticado:
                if st.button("Sair", use_container_width=True):
                    st.session_state.autenticado = False
                    st.rerun()

        if st.session_state.autenticado:
            st.markdown("---")
            # --- Upload ---
            uploaded = st.file_uploader(
                "Selecione .xlsx para upload",
                type=["xlsx"],
                accept_multiple_files=True,
                key="uploader_files",
            )
            if uploaded and st.button("🚀 Enviar para GitHub", use_container_width=True):
                for f in uploaded:
                    with st.spinner(f"Enviando {f.name}…"):
                        try:
                            fbytes = f.read()
                            tipo_detectado = parser.identificar_tipo(fbytes)
                            if tipo_detectado is None:
                                st.warning(f"⚠️ {f.name}: arquivo incompatível (Gantt ou desconhecido).")
                                continue
                            ok, msg = storage.upload_arquivo(fbytes, f.name, tipo_detectado)
                            if ok:
                                # Gerar histórico se já existe versão anterior
                                df_novo = parser.normalizar_planilha(fbytes, tipo_detectado)
                                versoes_tipo = storage.listar_versoes(tipo_detectado)
                                if len(versoes_tipo) >= 2:
                                    _, _, url_ant = versoes_tipo[1]
                                    bytes_ant = storage.carregar_planilha(url_ant)
                                    if bytes_ant:
                                        df_ant = parser.normalizar_planilha(bytes_ant, tipo_detectado)
                                        diff = comparator.comparar_versoes(df_ant, df_novo, tipo_detectado)
                                        entradas = comparator.gerar_entradas_historico(diff, tipo_detectado)
                                        if entradas:
                                            storage.salvar_historico(entradas)
                                # Limpar cache de versões
                                st.session_state.arquivos[tipo_detectado] = []
                                st.success(f"✅ {f.name} enviado.")
                            else:
                                st.error(f"❌ {f.name}: {msg}")
                        except Exception as e:
                            st.error(f"❌ {f.name}: {e}")

            st.markdown("---")
            # --- Exclusão ---
            st.markdown("**Excluir versão**")
            tipo_excluir = st.selectbox("Tipo", ["ETA", "Captação", "ETE"], key="tipo_excluir")
            versoes_excl = storage.listar_versoes(tipo_excluir)
            if versoes_excl:
                nomes_excl = [n for n, _, _ in versoes_excl]
                arquivo_excluir = st.selectbox("Arquivo", nomes_excl, key="arquivo_excluir")
                if st.button("🗑️ Excluir", use_container_width=True):
                    with st.spinner("Excluindo…"):
                        ok, msg = storage.excluir_arquivo(arquivo_excluir, tipo_excluir)
                        if ok:
                            st.session_state.arquivos[tipo_excluir] = []
                            st.success(msg)
                        else:
                            st.error(msg)
            else:
                st.caption("Nenhum arquivo encontrado.")

            st.markdown("---")
            # --- Troca de senha ---
            with st.expander("🔑 Trocar senha"):
                senha_atual  = st.text_input("Senha atual",  type="password", key="troca_atual")
                nova_senha   = st.text_input("Nova senha",   type="password", key="troca_nova")
                nova_senha2  = st.text_input("Confirmar",    type="password", key="troca_conf")
                if st.button("Salvar nova senha", use_container_width=True):
                    if nova_senha != nova_senha2:
                        st.error("Senhas não coincidem.")
                    else:
                        with st.spinner("Salvando…"):
                            ok, msg = storage.alterar_senha(senha_atual, nova_senha)
                            st.success(msg) if ok else st.error(msg)

# ---------------------------------------------------------------------------
# CONTEÚDO PRINCIPAL
# ---------------------------------------------------------------------------

# Banner Biancade
st.markdown("""
<div style="background:#423725;padding:20px 28px;border-radius:8px;margin-bottom:20px;">
    <div style="color:#FFFFFF;font-size:1.6em;font-weight:700;">
        Dashboard de Projetos de Saneamento
    </div>
    <div style="color:#E0D9CF;font-size:0.9em;margin-top:4px;">
        Gestão centralizada de planos de ação — Biancade Engenharia
    </div>
</div>
""", unsafe_allow_html=True)

# --- Carregar dados da versão ativa ---
df_ativo = None
data_versao_a = None

if st.session_state.versao_a:
    nome_a, data_a, url_a = st.session_state.versao_a
    data_versao_a = data_a
    cache_key = f"df_{url_a}"

    if cache_key not in st.session_state:
        with st.spinner(f"Carregando {nome_a}…"):
            try:
                fbytes = storage.carregar_planilha(url_a)
                if fbytes:
                    st.session_state[cache_key] = parser.normalizar_planilha(fbytes, tipo_selecionado)
                else:
                    st.error("Não foi possível baixar o arquivo do GitHub.")
            except Exception as e:
                st.error(f"Erro ao carregar planilha: {e}")

    df_ativo = st.session_state.get(cache_key)

if df_ativo is None:
    st.info(
        "Nenhum dado carregado. Faça upload de uma planilha para começar.\n\n"
        "Use o expander **📤 Upload / Administração** na sidebar."
    )
    st.stop()

# --- Aplicar filtros transversais ao DataFrame ---
df_filtrado = df_ativo.copy()
filtros = st.session_state.filtros_ativos
if filtros.get("municipio"):
    df_filtrado = df_filtrado[df_filtrado["municipio"].fillna("").str.contains(filtros["municipio"], case=False)]
if filtros.get("atividade"):
    df_filtrado = df_filtrado[df_filtrado["atividade"].fillna("").str.contains(filtros["atividade"], case=False)]
if filtros.get("responsavel"):
    df_filtrado = df_filtrado[df_filtrado["responsavel"].fillna("").str.contains(filtros["responsavel"], case=False)]
if filtros.get("plano"):
    df_filtrado = df_filtrado[df_filtrado["plano_de_acao"].fillna("").str.contains(filtros["plano"], case=False)]
if filtros.get("status"):
    df_filtrado = df_filtrado[df_filtrado["status_atual"] == filtros["status"]]

# ---------------------------------------------------------------------------
# 1 — CARTÕES DE MÉTRICAS (sobre dados filtrados)
# ---------------------------------------------------------------------------
visuals.cartoes_metricas(df_filtrado)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 2 — TABELA COM FILTROS INLINE
# ---------------------------------------------------------------------------
st.markdown(f"**Plano de Ação — {tipo_selecionado}**", unsafe_allow_html=False)
df_filtrado = visuals.tabela_com_filtros(df_filtrado, chave_estado=f"tbl_{tipo_selecionado}")

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 3 — FEED DINÂMICO
# ---------------------------------------------------------------------------
st.markdown("**Feed de Atualizações**")

# Carregar histórico do GitHub (cache de sessão)
if not st.session_state.historico_carregado:
    with st.spinner("Carregando histórico…"):
        st.session_state.historico_carregado = storage.carregar_historico()

# Resumo (versão única ou comparação)
if st.session_state.modo_comparacao and st.session_state.versao_b:
    nome_b, data_b, url_b = st.session_state.versao_b
    cache_key_b = f"df_{url_b}"
    if cache_key_b not in st.session_state:
        with st.spinner(f"Carregando {nome_b} para comparação…"):
            try:
                fbytes_b = storage.carregar_planilha(url_b)
                if fbytes_b:
                    st.session_state[cache_key_b] = parser.normalizar_planilha(
                        fbytes_b, tipo_selecionado
                    )
            except Exception as e:
                st.error(f"Erro ao carregar versão B: {e}")

    df_b = st.session_state.get(cache_key_b)
    if df_b is not None:
        diff = comparator.comparar_versoes(df_b, df_ativo, tipo_selecionado)
        resumo_txt = comparator.gerar_resumo_comparacao(
            diff, tipo_selecionado, data_b, data_versao_a
        )
        visuals.resumo_feed("comparacao", {"texto": resumo_txt})

        # Entradas do diff como feed
        entradas_feed = comparator.gerar_entradas_historico(diff, tipo_selecionado)
    else:
        entradas_feed = []
else:
    resumo_txt = history.gerar_resumo_versao(df_filtrado, tipo_selecionado, data_versao_a)
    visuals.resumo_feed("versao", {"texto": resumo_txt})
    entradas_feed = st.session_state.historico_carregado

# Filtros do feed
col_p1, col_p2, col_p3 = st.columns([2, 2, 1])
periodo_feed = col_p1.selectbox(
    "Período", ["2 semanas", "1 mês", "3 meses", "6 meses", "tudo"],
    index=4, key="periodo_feed",
)
tipo_feed = col_p2.selectbox(
    "Tipo", ["Todos", "ETA", "Captação", "ETE"], key="tipo_feed"
)

# Filtrar o feed pelos filtros ativos da tabela (municipio_filtro)
municipio_feed = filtros.get("municipio") if filtros else None

entradas_filtradas = history.filtrar_historico(
    entradas_feed,
    tipo=None if tipo_feed == "Todos" else tipo_feed,
    municipio=municipio_feed,
    periodo=periodo_feed,
)

# Exportação
with col_p3:
    if st.button("⬇ .txt", use_container_width=True, key="btn_export"):
        txt = history.exportar_txt(
            entradas_filtradas,
            tipo=None if tipo_feed == "Todos" else tipo_feed,
            periodo=periodo_feed,
            municipio=municipio_feed,
        )
        st.download_button(
            "💾 Baixar",
            data=txt,
            file_name=f"feed_{tipo_selecionado}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

# Exibir entradas do feed
if entradas_filtradas:
    st.caption(f"{len(entradas_filtradas)} entrada(s) no feed")
    for entrada in entradas_filtradas[:100]:
        visuals.linha_feed(entrada)
else:
    st.caption("Nenhuma entrada no feed para os filtros selecionados.")
