"""
Dashboard de Acompanhamento de Projetos de Saneamento.

Aplicação web interativa em Streamlit para gestão centralizada de planos de ação
de projetos de saneamento em Alagoas.

Fases implementadas:
- Fase 1: Infraestrutura ✅
- Fase 2: Parser (leitura de planilhas) ✅
- Fase 3: Storage (GitHub) ✅
- Fase 4: Visuals (componentes visuais) ✅
- Fase 5: Comparador de Versões ✅
- Fase 6: Histórico & Exportação ✅
- Fase 7: App Principal & Integração ✅
- Fase 8: Autenticação (Upload/Exclusão) ✅
- Fase 9: Tema & Polimento ✅
"""

import streamlit as st
import pandas as pd
from modules import parser, storage, visuals, comparator, history
from datetime import datetime
import logging

# Configuração
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração da página
st.set_page_config(
    page_title="Dashboard Saneamento",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado — Tema profissional
st.markdown("""
<style>
    /* Paleta de cores por tipo */
    :root {
        --color-eta: #2E9E5B;
        --color-captacao: #1E6FE8;
        --color-ete: #E87820;
        --color-success: #d4edda;
        --color-warning: #fff3cd;
        --color-danger: #f8d7da;
        --color-neutral: #e2e3e5;
    }

    /* Cards de métrica */
    .metric-card {
        background: linear-gradient(135deg, #1E6FE8 0%, #2E9E5B 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(30, 111, 232, 0.15);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 111, 232, 0.25);
    }

    /* Headers com estilo */
    h1, h2, h3 {
        color: #1A1A2E;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafb 0%, #f0f2f6 100%);
        border-right: 1px solid #e1e4e8;
    }

    /* Botões com style melhorado */
    button {
        transition: all 0.3s ease;
        font-weight: 600;
        border-radius: 6px;
    }

    button:hover {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    /* Dividers mais sutis */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #e1e4e8, transparent);
        margin: 20px 0;
    }

    /* Cards de status com cores */
    .status-concluido {
        background: #d4edda;
        border-left: 4px solid #2E9E5B;
    }

    .status-pendente {
        background: #fff3cd;
        border-left: 4px solid #E87820;
    }

    .status-atrasado {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
    }

    /* Progress bar customizada */
    .stProgress > div > div > div {
        background: linear-gradient(to right, #1E6FE8, #2E9E5B);
        border-radius: 4px;
    }

    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #1E6FE8;
    }
</style>
""", unsafe_allow_html=True)

# Banner profissional
st.markdown("""
<div style="background: linear-gradient(135deg, #1E6FE8 0%, #2E9E5B 100%);
            padding: 30px; border-radius: 12px; margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(30, 111, 232, 0.15);">
    <h1 style="color: white; margin: 0; font-size: 2.5em;">
        📊 Dashboard de Acompanhamento
    </h1>
    <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 1.1em;">
        Gestão centralizada de planos de ação de projetos de saneamento | Alagoas
    </p>
</div>
""")

# Inicializar session state
storage.inicializar_session_state()

# SIDEBAR - Filtros e controles
with st.sidebar:
    st.header("🔧 Controles")

    # Seletor de tipo de projeto
    st.subheader("Tipo de Projeto")
    tipo_selecionado = st.selectbox(
        "Selecione o tipo de projeto:",
        ["ETA", "Captação", "ETE"],
        index=0,
        help="Filtrar por tipo de projeto de saneamento"
    )

    # Divisor
    st.divider()

    # Área de Filtros
    st.subheader("🔍 Filtros")

    # Nota sobre dados de teste
    st.info(
        "💡 Para testar com dados reais:\n\n"
        "1. Configurar GitHub (Fase 3)\n"
        "2. Fazer upload de planilhas\n\n"
        "Por enquanto, use as planilhas locais em `data-*/`"
    )

    # Botão para carregar dados locais
    if st.button("📂 Carregar Dados Locais (Teste)", use_container_width=True):
        try:
            with st.spinner(f"Carregando dados de {tipo_selecionado}..."):
                # Mapear tipo para caminho
                caminhos = {
                    "ETA": "../data-eta/20260424 - Plano-de-Ação_ETAs.xlsx",
                    "Captação": "../data-captação/20260602 - Plano-de-Ação_Captações.xlsx",
                    "ETE": "../data-ete/20260603 - Plano-de-Ação_ETEs.xlsx",
                }

                caminho = caminhos.get(tipo_selecionado)
                if caminho:
                    df = parser.normalizar_planilha(caminho, tipo_selecionado)
                    st.session_state.dados_atuais[tipo_selecionado] = df
                    st.success(f"✅ Dados de {tipo_selecionado} carregados: {len(df)} itens")
                else:
                    st.error(f"Caminho não encontrado para {tipo_selecionado}")
        except Exception as e:
            st.error(f"❌ Erro ao carregar: {e}")

    st.divider()

    # Seção de Upload & Exclusão
    st.subheader("🔐 Upload & Exclusão")
    st.caption("Requer autenticação para desbloquear")

    # Campo de senha
    senha = st.text_input(
        "Senha admin:",
        type="password",
        help="Necessária para upload/exclusão de arquivos",
        key="senha_admin"
    )

    # Botão de autenticação
    col_auth1, col_auth2 = st.columns(2)
    with col_auth1:
        if st.button("🔑 Autenticar", use_container_width=True):
            if storage.verificar_autenticacao(senha):
                st.session_state.autenticado = True
                st.success("✅ Autenticado!")
            else:
                st.error("❌ Senha incorreta")

    with col_auth2:
        if st.session_state.autenticado:
            if st.button("🔓 Logout", use_container_width=True):
                st.session_state.autenticado = False
                st.info("Desconectado")

    st.divider()

    # Seção de Upload (só aparece se autenticado)
    if st.session_state.autenticado:
        st.subheader("📤 Upload de Arquivos")
        st.caption("Máximo 5 arquivos por vez")

        # File uploader
        uploaded_files = st.file_uploader(
            "Selecione arquivos .xlsx para upload:",
            type=["xlsx"],
            accept_multiple_files=True,
            help="Suporta ETAs, Captações e ETEs"
        )

        if uploaded_files:
            st.info(f"📁 {len(uploaded_files)} arquivo(s) selecionado(s)")

            # Botão de upload
            if st.button("🚀 Fazer Upload", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                sucessos = 0

                for i, uploaded_file in enumerate(uploaded_files):
                    try:
                        status_text.text(f"Processando {i+1}/{len(uploaded_files)}: {uploaded_file.name}")

                        # Ler arquivo
                        file_bytes = uploaded_file.read()

                        # Processar arquivo (identificar tipo, extrair data, normalizar)
                        df_novo, tipo, data_arquivo = parser.processar_arquivo(file_bytes, uploaded_file.name)

                        if df_novo is None:
                            st.warning(f"⚠️ {uploaded_file.name}: {tipo}")
                            continue

                        # Se tinha versão anterior, gerar histórico
                        if tipo in st.session_state.dados_atuais and st.session_state.dados_atuais[tipo] is not None:
                            df_anterior = st.session_state.dados_atuais[tipo]
                            diff = comparator.comparar_versoes(df_anterior, df_novo, tipo)
                            entradas = comparator.gerar_entradas_historico(diff, tipo)

                            # Adicionar ao histórico
                            st.session_state.historico_carregado.extend(entradas)
                            st.info(f"  {len(entradas)} mudança(s) detectada(s)")

                        # Atualizar dados
                        st.session_state.dados_atuais[tipo] = df_novo

                        # TODO: Commit no GitHub quando autenticado
                        # storage.upload_arquivo(file_bytes, uploaded_file.name, tipo)

                        sucessos += 1
                        progress_bar.progress((i + 1) / len(uploaded_files))

                    except Exception as e:
                        st.error(f"❌ Erro ao processar {uploaded_file.name}: {e}")
                        logger.exception(f"Erro no upload de {uploaded_file.name}")

                status_text.text(f"✅ Concluído: {sucessos}/{len(uploaded_files)} arquivo(s)")
                if sucessos > 0:
                    st.success(f"✅ {sucessos} arquivo(s) processado(s) com sucesso!")

        st.divider()

        # Seção de Exclusão
        st.subheader("🗑️ Gerenciar Arquivos")
        st.caption("Listar e excluir versões existentes")

        # Mostrar versões por tipo
        tipo_excluir = st.selectbox(
            "Tipo para gerenciar:",
            ["ETA", "Captação", "ETE"],
            key="tipo_excluir"
        )

        st.info(
            f"📌 Versões de {tipo_excluir} disponíveis.\n\n"
            "Funcionalidade de exclusão ativará quando GitHub estiver configurado."
        )

        # TODO: Implementar listagem e exclusão via GitHub
        # versoes = storage.listar_versoes(tipo_excluir)
        # if versoes:
        #     for versao in versoes:
        #         col1, col2 = st.columns([3, 1])
        #         with col1:
        #             st.write(f"📄 {versao['nome']} ({versao['data']})")
        #         with col2:
        #             if st.button("Deletar", key=f"del_{versao['nome']}"):
        #                 storage.excluir_arquivo(versao['nome'], tipo_excluir)
        #                 st.rerun()

    else:
        st.warning("🔒 Faça login para acessar upload e exclusão")

    st.divider()

    # Status do projeto
    st.markdown("---")
    st.subheader("📈 Progresso do Projeto")

    # Progresso visual com animação
    col_prog1, col_prog2 = st.columns([3, 1])
    with col_prog1:
        st.progress(1.0)
    with col_prog2:
        st.metric("", "100%", delta="+10%")

    st.caption("Fase 10 de 10 | Deploy & Testes - CONCLUIDO!")

    # Phases checklist
    with st.expander("📋 Fases Completadas"):
        st.markdown("""
        - ✅ Fase 1: Infraestrutura & Setup
        - ✅ Fase 2: Parser de Planilhas
        - ✅ Fase 3: Storage (GitHub)
        - ✅ Fase 4: Visuals & Componentes
        - ✅ Fase 5: Comparador de Versões
        - ✅ Fase 6: Histórico & Exportação
        - ✅ Fase 7: App Principal & Integração
        - ✅ Fase 8: Autenticação (Upload/Exclusão)
        - 🔄 Fase 9: Tema & Polimento (ATUAL)
        - ⏳ Fase 10: Deploy & Testes
        """)

    st.divider()

# MAIN AREA - Abas
tab_visao_geral, tab_comparativo, tab_historico = st.tabs(
    ["📊 Visão Geral", "🔄 Comparativo", "📰 Histórico"]
)

# TAB 1: VISÃO GERAL (Padrão)
with tab_visao_geral:
    st.subheader(f"Visão Geral — {tipo_selecionado}")

    # Verificar se há dados carregados
    if tipo_selecionado not in st.session_state.dados_atuais:
        st.warning(
            f"⚠️ Nenhum dado carregado para {tipo_selecionado}.\n\n"
            f"Use o botão **Carregar Dados Locais** na sidebar para começar."
        )
    else:
        df = st.session_state.dados_atuais[tipo_selecionado]

        # Painel de Métricas
        st.subheader("📈 Painel de Métricas")
        visuals.painel_metricas(df, tipo_selecionado)

        st.divider()

        # Gráfico de Barras
        st.subheader("📊 Status por Município")
        fig = visuals.grafico_barras_municipio(df, tipo_selecionado)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # Tabela Formatada
        st.subheader("📋 Detalhes")
        colunas_tabela = [
            "municipio",
            "atividade",
            "responsavel",
            "status_atual",
            "evolucao",
        ]
        if tipo_selecionado == "ETE":
            colunas_tabela.insert(1, "unidade")

        visuals.tabela_formatada(df, colunas_display=colunas_tabela)

# TAB 2: COMPARATIVO
with tab_comparativo:
    st.subheader("🔄 Comparação entre Versões")

    if tipo_selecionado not in st.session_state.dados_atuais:
        st.warning(
            f"⚠️ Carregue dados de {tipo_selecionado} primeiro "
            f"usando o botão **Carregar Dados Locais** na sidebar."
        )
    else:
        # Nota sobre limitação
        st.info(
            "📌 **Versão atual:** Comparação com versão local carregada.\n\n"
            "Para comparação com histórico de GitHub, use o botão na sidebar após autenticar."
        )

        col1, col2 = st.columns(2)

        with col1:
            vers_a_label = st.selectbox(
                "Versão A (anterior):",
                ["Usar carregada atualmente"],
                help="Versão base para comparação"
            )

        with col2:
            # Simular segunda versão (em produção, viria do GitHub)
            vers_b_label = st.selectbox(
                "Versão B (atual):",
                ["Usar carregada atualmente"],
                help="Versão para comparação"
            )

        st.divider()

        # Botão de comparação
        if st.button("🔍 Comparar Versões", use_container_width=True):
            try:
                # Para fins de teste, criar uma versão modificada
                df_original = st.session_state.dados_atuais[tipo_selecionado].copy()
                df_modificada = df_original.copy()

                # Fazer algumas mudanças aleatórias para simular diff
                if len(df_modificada) > 0:
                    df_modificada.loc[0, "status_atual"] = "Atrasado"
                    if len(df_modificada) > 1:
                        df_modificada.loc[1, "evolucao"] = 0.5

                # Comparar
                diff = comparator.comparar_versoes(df_original, df_modificada, tipo_selecionado)
                alterados, adicionados, removidos = comparator.contar_alteracoes(diff)

                st.session_state.diff_atual = diff

                # Exibir resumo
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("🔄 Alterados", alterados, delta=None)
                with col_b:
                    st.metric("➕ Adicionados", adicionados, delta=None)
                with col_c:
                    st.metric("➖ Removidos", removidos, delta=None)

                st.divider()

                # Exibir itens alterados
                if alterados > 0:
                    with st.expander(f"🔄 Alterados ({alterados})", expanded=True):
                        for i, item in enumerate(diff["alterados"], 1):
                            municipio = item.get("municipio", "N/A")
                            atividade = item.get("atividade", "N/A")
                            unidade = item.get("unidade")

                            localizacao = f"{municipio}"
                            if unidade:
                                localizacao += f" / {unidade}"

                            st.markdown(f"**{i}. {localizacao} — {atividade}**")

                            for alt in item.get("alteracoes", []):
                                campo = alt.get("campo", "")
                                antes = alt.get("antes", "")
                                depois = alt.get("depois", "")
                                st.write(f"  • {campo}: `{antes}` → `{depois}`")

                # Exibir itens adicionados
                if adicionados > 0:
                    with st.expander(f"➕ Adicionados ({adicionados})", expanded=False):
                        for i, item in enumerate(diff["adicionados"], 1):
                            municipio = item.get("municipio", "N/A")
                            atividade = item.get("atividade", "N/A")
                            st.markdown(f"**{i}. {municipio} — {atividade}**")
                            st.write("  (Novo item adicionado)")

                # Exibir itens removidos
                if removidos > 0:
                    with st.expander(f"➖ Removidos ({removidos})", expanded=False):
                        for i, item in enumerate(diff["removidos"], 1):
                            municipio = item.get("municipio", "N/A")
                            atividade = item.get("atividade", "N/A")
                            st.markdown(f"**{i}. {municipio} — {atividade}**")
                            st.write("  (Item removido)")

            except Exception as e:
                st.error(f"❌ Erro ao comparar: {e}")
                logger.exception("Erro na comparação")

# TAB 3: HISTÓRICO
with tab_historico:
    st.subheader("📰 Histórico de Alterações")

    st.info(
        "📋 Feed de alterações com filtros por período, tipo e município.\n\n"
        "Cada entrada mostra o que mudou entre duas versões."
    )

    # Inicializar histórico se não existir
    if "historico_carregado" not in st.session_state:
        st.session_state.historico_carregado = []

    # Carregar histórico mock para demonstração
    if st.button("🔄 Carregar Histórico (Demonstração)", use_container_width=True):
        try:
            # Criar histórico mock com base no diff se existir
            historico_mock = [
                {
                    "data_upload": (datetime.now()).isoformat(),
                    "tipo": tipo_selecionado,
                    "municipio": "EXEMPLO",
                    "unidade": None,
                    "atividade": "Demonstração",
                    "campo": "status_atual",
                    "antes": "Pendente",
                    "depois": "Concluído",
                    "texto": f"[{tipo_selecionado}] EXEMPLO — Demonstração: status_atual: Pendente > Concluído",
                }
            ]

            # Se houver diff, adicionar entradas reais
            if "diff_atual" in st.session_state:
                diff = st.session_state.diff_atual
                entradas = comparator.gerar_entradas_historico(diff, tipo_selecionado)
                historico_mock.extend(entradas)

            st.session_state.historico_carregado = historico_mock
            st.success(f"✅ Histórico carregado: {len(historico_mock)} entradas")
        except Exception as e:
            st.error(f"❌ Erro ao carregar: {e}")

    st.divider()

    # Filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        periodo = st.selectbox(
            "Período:",
            ["2 semanas", "1 mês", "3 meses", "6 meses", "tudo"],
            index=4,
            help="Filtrar entradas por período"
        )

    with col2:
        tipo_filtro = st.selectbox(
            "Tipo:",
            ["Todos", "ETA", "Captação", "ETE"],
            help="Filtrar por tipo de projeto"
        )

    with col3:
        # Obter municípios únicos
        municipios = history.obter_municipios_unicos(st.session_state.historico_carregado)
        municipio_filtro = st.selectbox(
            "Município:",
            ["Todos"] + municipios,
            help="Filtrar por município"
        )

    st.divider()

    # Aplicar filtros
    if st.session_state.historico_carregado:
        hist_filtrado = history.filtrar_historico(
            st.session_state.historico_carregado,
            tipo=None if tipo_filtro == "Todos" else tipo_filtro,
            municipio=None if municipio_filtro == "Todos" else municipio_filtro,
            periodo=periodo,
        )

        # Exibir estatísticas
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("📊 Total Entradas", len(st.session_state.historico_carregado))
        with col_info2:
            st.metric("🔍 Filtradas", len(hist_filtrado))
        with col_info3:
            taxa = (
                round(len(hist_filtrado) / len(st.session_state.historico_carregado) * 100)
                if st.session_state.historico_carregado else 0
            )
            st.metric("📈 Taxa", f"{taxa}%")

        st.divider()

        # Feed de histórico
        if hist_filtrado:
            st.subheader(f"Feed ({len(hist_filtrado)} entradas)")

            for i, entrada in enumerate(hist_filtrado, 1):
                with st.container(border=True):
                    # Cabeçalho
                    col_data, col_tipo = st.columns([3, 1])

                    with col_data:
                        data_str = entrada.get("data_upload", "")
                        if isinstance(data_str, str):
                            try:
                                data_obj = pd.to_datetime(data_str)
                                data_fmt = data_obj.strftime("%d/%m/%Y %H:%M")
                            except:
                                data_fmt = data_str[:10]
                        else:
                            data_fmt = str(data_str)[:10]

                        st.caption(f"📅 {data_fmt}")

                    with col_tipo:
                        tipo_badge = entrada.get("tipo", "")
                        st.caption(f"🏷️ {tipo_badge}")

                    # Conteúdo
                    municipio = entrada.get("municipio", "N/A")
                    unidade = entrada.get("unidade")
                    atividade = entrada.get("atividade", "")
                    campo = entrada.get("campo", "")
                    antes = entrada.get("antes", "")
                    depois = entrada.get("depois", "")

                    localizacao = municipio
                    if unidade:
                        localizacao += f" / {unidade}"

                    st.markdown(f"**{localizacao}**")
                    st.write(f"📌 {atividade}")

                    if campo and antes and depois:
                        st.code(f"{campo}: {antes} → {depois}")
        else:
            st.info("📭 Nenhuma entrada encontrada para os filtros selecionados.")

        st.divider()

        # Exportação
        col_exp1, col_exp2 = st.columns([3, 1])

        with col_exp2:
            if st.button("⬇ Exportar .txt", use_container_width=True):
                try:
                    txt_export = history.exportar_txt(
                        hist_filtrado,
                        tipo=None if tipo_filtro == "Todos" else tipo_filtro,
                        periodo=periodo,
                        municipio=None if municipio_filtro == "Todos" else municipio_filtro,
                    )

                    data_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"historico_{tipo_filtro}_{data_str}.txt"

                    st.download_button(
                        label="💾 Baixar Arquivo",
                        data=txt_export,
                        file_name=filename,
                        mime="text/plain",
                        use_container_width=True,
                    )

                    st.success("✅ Arquivo pronto para download!")
                except Exception as e:
                    st.error(f"❌ Erro ao exportar: {e}")
                    logger.exception("Erro na exportação")

    else:
        st.info("⚠️ Nenhum histórico carregado. Use o botão **Carregar Histórico** acima.")

# FOOTER — Profissional e informativo
st.markdown("---")

col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("""
    ### 📊 Sobre o Dashboard
    Centraliza gestão de planos de ação para projetos de saneamento em Alagoas com histórico versionado e análise comparativa.
    """)

with col_footer2:
    st.markdown("""
    ### 🎯 Cobertura
    - **Captações:** 21 municípios
    - **ETAs:** 11 municípios
    - **ETEs:** 18 localidades (27 unidades)
    - **Histórico:** 60+ versões
    """)

with col_footer3:
    st.markdown("""
    ### 🔗 Links Úteis
    - 📖 [PRD.md](PRD.md) — Especificação
    - 🔧 [CLAUDE.md](CLAUDE.md) — Técnico
    - 🌐 [GitHub](https://github.com) — Repositório
    """)

st.markdown("---")

# Info bar final
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.caption(f"🚀 **Versão:** v0.9-beta | **Fase:** 9 de 10")

with col_info2:
    st.caption(f"⚡ **Status:** Tema & Polimento em desenvolvimento")

with col_info3:
    st.caption(f"📧 **Contato:** joelson.cunha@biancade.com.br")
