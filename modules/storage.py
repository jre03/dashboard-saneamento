"""
Módulo de Persistência de Dados em GitHub e Session State.

Funcionalidades:
- Upload de arquivos para GitHub (com commit automático)
- Listagem de versões de um tipo de projeto
- Leitura e escrita de histórico (history.json) - imutável após criação
- Leitura e escrita de metadados (metadata.json)
- Gerenciamento de session_state local

Estrutura do repositório GitHub:
  data/
  ├── captacoes/
  │   └── YYYYMMDD - Plano-de-Acao_Captacoes.xlsx
  ├── etas/
  │   └── YYYYMMDD - Plano-de-Acao_ETAs.xlsx
  └── etes/
      └── YYYYMMDD - Plano-de-Acao_ETEs.xlsx
  history.json    (feed de histórico acumulado, imutável)
  metadata.json   (índice de arquivos com tipos e datas)

Autenticação:
- Leitura: API pública GitHub (sem token)
- Escrita: GITHUB_TOKEN em st.secrets
- Verificação: ADMIN_PASSWORD em st.secrets
"""

import os
import certifi
os.environ["SSL_CERT_FILE"]      = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

import streamlit as st
import json
import hashlib
import logging
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime
from github import Github, Auth
from github.GithubException import GithubException
import pandas as pd
import io

logger = logging.getLogger(__name__)

# Configuração — lida de st.secrets em runtime
DATA_FOLDER = "data"
HISTORY_FILE = "history.json"
METADATA_FILE = "metadata.json"
CONFIG_FILE = "config.json"

# Mapeamento de tipo para pasta no GitHub
TIPO_PASTA = {
    "ETA": "etas",
    "Captação": "captacoes",
    "ETE": "etes",
}


def _get_github_client() -> Optional[Github]:
    """Retorna cliente GitHub autenticado com SSL via certifi."""
    try:
        token = st.secrets.get("GITHUB_TOKEN")
        if not token:
            logger.warning("GITHUB_TOKEN não configurado em st.secrets")
            return None

        auth = Auth.Token(token)
        return Github(auth=auth)
    except Exception as e:
        logger.error(f"Erro ao criar cliente GitHub: {e}")
        return None


def _get_repo(g: Github) -> Optional[Any]:
    """Obtém repositório GitHub a partir de st.secrets."""
    try:
        owner = st.secrets.get("GITHUB_OWNER", "")
        repo  = st.secrets.get("GITHUB_REPO", "dashboard-saneamento")
        if not owner:
            logger.warning("GITHUB_OWNER não configurado em st.secrets")
            return None
        repo_completo = f"{owner}/{repo}"
        return g.get_repo(repo_completo)
    except GithubException as e:
        logger.error(f"Repositório não encontrado: {e}")
        return None


def _sha256(texto: str) -> str:
    return hashlib.sha256(texto.encode()).hexdigest()


def _carregar_config() -> Optional[Dict[str, Any]]:
    """Lê data/config.json do GitHub. Retorna None se não existir."""
    try:
        g = _get_github_client()
        if not g:
            return None
        repo = _get_repo(g)
        if not repo:
            return None
        contents = repo.get_contents(f"{DATA_FOLDER}/{CONFIG_FILE}")
        return json.loads(contents.decoded_content.decode())
    except GithubException as e:
        if e.status == 404:
            return None
        logger.error(f"Erro ao carregar config: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro ao carregar config: {e}")
        return None


def _salvar_config(config: Dict[str, Any]) -> Tuple[bool, str]:
    """Grava data/config.json no GitHub via commit."""
    try:
        g = _get_github_client()
        if not g:
            return False, "Token GitHub ausente"
        repo = _get_repo(g)
        if not repo:
            return False, "Repositório não encontrado"

        conteudo = json.dumps(config, ensure_ascii=False, indent=2)
        caminho = f"{DATA_FOLDER}/{CONFIG_FILE}"

        try:
            contents = repo.get_contents(caminho)
            repo.update_file(
                path=caminho,
                message="Atualizar config (senha admin)",
                content=conteudo,
                sha=contents.sha,
                branch="main",
            )
        except GithubException as e:
            if e.status == 404:
                repo.create_file(
                    path=caminho,
                    message="Criar config inicial",
                    content=conteudo,
                    branch="main",
                )
            else:
                raise

        return True, "Config salvo"
    except Exception as e:
        logger.error(f"Erro ao salvar config: {e}")
        return False, str(e)


def verificar_autenticacao(senha: str) -> bool:
    """
    Verifica senha de admin com SHA-256.

    Ordem de verificação:
    1. data/config.json no GitHub (password_hash)
    2. Fallback: SHA-256(st.secrets["ADMIN_PASSWORD"])
    """
    try:
        hash_fornecido = _sha256(senha)

        config = _carregar_config()
        if config and "password_hash" in config:
            return hash_fornecido == config["password_hash"]

        # Fallback: secrets
        admin_password = st.secrets.get("ADMIN_PASSWORD", "")
        if not admin_password:
            logger.error("ADMIN_PASSWORD não configurado")
            return False
        return hash_fornecido == _sha256(admin_password)

    except Exception as e:
        logger.error(f"Erro ao verificar autenticação: {e}")
        return False


def alterar_senha(senha_atual: str, nova_senha: str) -> Tuple[bool, str]:
    """
    Valida senha_atual e grava SHA-256(nova_senha) em data/config.json.

    Returns:
        Tupla (sucesso, mensagem)
    """
    if not verificar_autenticacao(senha_atual):
        return False, "Senha atual incorreta"

    if len(nova_senha) < 6:
        return False, "Nova senha deve ter pelo menos 6 caracteres"

    config = _carregar_config() or {}
    config["password_hash"] = _sha256(nova_senha)

    return _salvar_config(config)


def carregar_planilha(url: str) -> Optional[bytes]:
    """
    Baixa bytes de um arquivo do GitHub pela URL de download.

    Args:
        url: download_url retornado por listar_versoes()

    Returns:
        bytes do arquivo ou None em caso de erro
    """
    try:
        import urllib.request
        with urllib.request.urlopen(url) as resp:
            return resp.read()
    except Exception as e:
        logger.error(f"Erro ao carregar planilha: {e}")
        return None


def listar_versoes(tipo: str) -> List[Tuple[str, Optional[datetime], str]]:
    """
    Lista todas as versões de um tipo de projeto no GitHub.

    Args:
        tipo: "ETA" | "Captação" | "ETE"

    Returns:
        Lista de (nome_arquivo, data_extraida, url_download) ordenada por data decrescente
    """
    try:
        g = _get_github_client()
        if not g:
            logger.warning("Cliente GitHub não disponível")
            return []

        repo = _get_repo(g)
        if not repo:
            return []

        pasta = TIPO_PASTA.get(tipo)
        if not pasta:
            logger.error(f"Tipo desconhecido: {tipo}")
            return []

        # Listar arquivos na pasta
        versoes = []
        try:
            contents = repo.get_contents(f"{DATA_FOLDER}/{pasta}")
            for content in contents:
                if content.name.endswith(".xlsx"):
                    # Extrair data do nome
                    import re
                    match = re.search(r"(\d{8})", content.name)
                    data = None
                    if match:
                        try:
                            data = datetime.strptime(match.group(1), "%Y%m%d")
                        except:
                            pass

                    versoes.append((content.name, data, content.download_url))

            # Ordenar por data decrescente
            versoes.sort(key=lambda x: x[1] if x[1] else datetime.min, reverse=True)

            logger.info(f"Encontradas {len(versoes)} versões de {tipo}")
            return versoes

        except GithubException as e:
            if e.status == 404:
                logger.info(f"Pasta {DATA_FOLDER}/{pasta} não existe ainda")
                return []
            raise

    except Exception as e:
        logger.error(f"Erro ao listar versões de {tipo}: {e}")
        return []


def upload_arquivo(
    arquivo_bytes: bytes,
    nome_arquivo: str,
    tipo: str,
    mensagem_commit: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Faz upload de arquivo para GitHub com commit automático.

    Args:
        arquivo_bytes: Conteúdo do arquivo em bytes
        nome_arquivo: Nome do arquivo
        tipo: "ETA" | "Captação" | "ETE"
        mensagem_commit: Mensagem do commit (opcional)

    Returns:
        Tupla (sucesso, mensagem)
    """
    try:
        g = _get_github_client()
        if not g:
            return False, "Autenticação GitHub falhou"

        repo = _get_repo(g)
        if not repo:
            return False, f"Repositório {OWNER}/{REPO} não encontrado"

        pasta = TIPO_PASTA.get(tipo)
        if not pasta:
            return False, f"Tipo desconhecido: {tipo}"

        caminho = f"{DATA_FOLDER}/{pasta}/{nome_arquivo}"

        # Mensagem padrão do commit
        if not mensagem_commit:
            mensagem_commit = f"Upload {tipo}: {nome_arquivo}"

        # Fazer upload
        repo.create_file(
            path=caminho,
            message=mensagem_commit,
            content=arquivo_bytes,
            branch="main"
        )

        logger.info(f"Arquivo enviado: {caminho}")
        return True, f"Arquivo {nome_arquivo} enviado com sucesso para {tipo}"

    except GithubException as e:
        if e.status == 422:
            # Arquivo já existe, atualizar
            try:
                contents = repo.get_contents(caminho)
                repo.update_file(
                    path=caminho,
                    message=mensagem_commit,
                    content=arquivo_bytes,
                    sha=contents.sha,
                    branch="main"
                )
                logger.info(f"Arquivo atualizado: {caminho}")
                return True, f"Arquivo {nome_arquivo} atualizado com sucesso"
            except Exception as e2:
                logger.error(f"Erro ao atualizar arquivo: {e2}")
                return False, f"Erro ao atualizar arquivo: {e2}"
        else:
            logger.error(f"Erro GitHub ao fazer upload: {e}")
            return False, f"Erro ao fazer upload: {e}"

    except Exception as e:
        logger.error(f"Erro ao fazer upload de arquivo: {e}")
        return False, f"Erro ao fazer upload: {e}"


def excluir_arquivo(nome_arquivo: str, tipo: str) -> Tuple[bool, str]:
    """
    Remove arquivo do GitHub.

    Nota: O histórico NÃO é removido (é imutável).

    Args:
        nome_arquivo: Nome do arquivo
        tipo: "ETA" | "Captação" | "ETE"

    Returns:
        Tupla (sucesso, mensagem)
    """
    try:
        g = _get_github_client()
        if not g:
            return False, "Autenticação GitHub falhou"

        repo = _get_repo(g)
        if not repo:
            return False, f"Repositório {OWNER}/{REPO} não encontrado"

        pasta = TIPO_PASTA.get(tipo)
        if not pasta:
            return False, f"Tipo desconhecido: {tipo}"

        caminho = f"{DATA_FOLDER}/{pasta}/{nome_arquivo}"

        try:
            contents = repo.get_contents(caminho)
            repo.delete_file(
                path=caminho,
                message=f"Exclusao {tipo}: {nome_arquivo}",
                sha=contents.sha,
                branch="main"
            )

            logger.info(f"Arquivo deletado: {caminho}")
            return True, f"Arquivo {nome_arquivo} removido com sucesso"

        except GithubException as e:
            if e.status == 404:
                return False, f"Arquivo não encontrado: {nome_arquivo}"
            raise

    except Exception as e:
        logger.error(f"Erro ao deletar arquivo: {e}")
        return False, f"Erro ao deletar arquivo: {e}"


def carregar_historico() -> List[Dict[str, Any]]:
    """
    Carrega history.json do GitHub.

    Returns:
        Lista de entradas de histórico (vazia se arquivo não existe)
    """
    try:
        g = _get_github_client()
        if not g:
            logger.warning("Cliente GitHub não disponível")
            return []

        repo = _get_repo(g)
        if not repo:
            return []

        try:
            contents = repo.get_contents(HISTORY_FILE)
            historico = json.loads(contents.decoded_content.decode())
            logger.info(f"Histórico carregado: {len(historico)} entradas")
            return historico

        except GithubException as e:
            if e.status == 404:
                logger.info(f"Arquivo {HISTORY_FILE} não existe ainda")
                return []
            raise

    except Exception as e:
        logger.error(f"Erro ao carregar histórico: {e}")
        return []


def salvar_historico(novas_entradas: List[Dict[str, Any]]) -> Tuple[bool, str]:
    """
    Appenda novas entradas em history.json e commita no GitHub.

    Args:
        novas_entradas: Lista de dicts com histórico

    Returns:
        Tupla (sucesso, mensagem)
    """
    try:
        g = _get_github_client()
        if not g:
            return False, "Autenticação GitHub falhou"

        repo = _get_repo(g)
        if not repo:
            return False, f"Repositório {OWNER}/{REPO} não encontrado"

        # Carregar histórico existente
        historico = carregar_historico()

        # Adicionar novas entradas
        historico.extend(novas_entradas)

        # Converter datas para string (JSON serializable)
        historico_json = []
        for entrada in historico:
            entrada_copy = entrada.copy()
            if isinstance(entrada_copy.get("data_upload"), datetime):
                entrada_copy["data_upload"] = entrada_copy["data_upload"].isoformat()
            historico_json.append(entrada_copy)

        # Escrever arquivo
        conteudo = json.dumps(historico_json, ensure_ascii=False, indent=2)

        try:
            contents = repo.get_contents(HISTORY_FILE)
            # Arquivo existe, atualizar
            repo.update_file(
                path=HISTORY_FILE,
                message=f"Atualizar histórico: {len(novas_entradas)} novas entradas",
                content=conteudo,
                sha=contents.sha,
                branch="main"
            )
        except GithubException as e:
            if e.status == 404:
                # Arquivo não existe, criar
                repo.create_file(
                    path=HISTORY_FILE,
                    message="Criar histórico inicial",
                    content=conteudo,
                    branch="main"
                )
            else:
                raise

        logger.info(f"Histórico salvo: {len(novas_entradas)} novas entradas")
        return True, f"Histórico atualizado com {len(novas_entradas)} entradas"

    except Exception as e:
        logger.error(f"Erro ao salvar histórico: {e}")
        return False, f"Erro ao salvar histórico: {e}"


def carregar_metadata() -> Dict[str, Any]:
    """
    Carrega metadata.json do GitHub.

    Returns:
        Dict com metadados (vazio se arquivo não existe)
    """
    try:
        g = _get_github_client()
        if not g:
            return {}

        repo = _get_repo(g)
        if not repo:
            return {}

        try:
            contents = repo.get_contents(METADATA_FILE)
            metadata = json.loads(contents.decoded_content.decode())
            logger.info(f"Metadados carregados")
            return metadata

        except GithubException as e:
            if e.status == 404:
                logger.info(f"Arquivo {METADATA_FILE} não existe ainda")
                return {}
            raise

    except Exception as e:
        logger.error(f"Erro ao carregar metadados: {e}")
        return {}


def salvar_metadata(metadata: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Salva metadata.json no GitHub.

    Args:
        metadata: Dicionário com metadados

    Returns:
        Tupla (sucesso, mensagem)
    """
    try:
        g = _get_github_client()
        if not g:
            return False, "Autenticação GitHub falhou"

        repo = _get_repo(g)
        if not repo:
            return False, f"Repositório {OWNER}/{REPO} não encontrado"

        conteudo = json.dumps(metadata, ensure_ascii=False, indent=2)

        try:
            contents = repo.get_contents(METADATA_FILE)
            repo.update_file(
                path=METADATA_FILE,
                message="Atualizar metadados",
                content=conteudo,
                sha=contents.sha,
                branch="main"
            )
        except GithubException as e:
            if e.status == 404:
                repo.create_file(
                    path=METADATA_FILE,
                    message="Criar metadados iniciais",
                    content=conteudo,
                    branch="main"
                )
            else:
                raise

        logger.info(f"Metadados salvos")
        return True, "Metadados atualizados"

    except Exception as e:
        logger.error(f"Erro ao salvar metadados: {e}")
        return False, f"Erro ao salvar metadados: {e}"


def inicializar_session_state():
    """
    Inicializa st.session_state com estrutura padrão.

    Estrutura:
    - arquivos: {tipo: [(nome, data, url), ...]}
    - historico: [entradas...]
    - autenticado: bool
    - dados_atuais: {tipo: DataFrame}
    """
    if "arquivos" not in st.session_state:
        st.session_state.arquivos = {
            "ETA": [],
            "Captação": [],
            "ETE": [],
        }

    if "historico" not in st.session_state:
        st.session_state.historico = []

    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if "dados_atuais" not in st.session_state:
        st.session_state.dados_atuais = {}

    if "timestamp_ultimo_refresh" not in st.session_state:
        st.session_state.timestamp_ultimo_refresh = None

    if "filtros_ativos" not in st.session_state:
        st.session_state.filtros_ativos = {}

    if "modo_comparacao" not in st.session_state:
        st.session_state.modo_comparacao = False

    if "versao_a" not in st.session_state:
        st.session_state.versao_a = None

    if "versao_b" not in st.session_state:
        st.session_state.versao_b = None

    if "historico_carregado" not in st.session_state:
        st.session_state.historico_carregado = []

    logger.info("Session state inicializado")


def recarregar_versoes():
    """Recarrega lista de versões do GitHub para session_state."""
    try:
        for tipo in ["ETA", "Captação", "ETE"]:
            versoes = listar_versoes(tipo)
            st.session_state.arquivos[tipo] = versoes

        # Recarregar histórico
        st.session_state.historico = carregar_historico()

        st.session_state.timestamp_ultimo_refresh = datetime.now()
        logger.info("Versões recarregadas do GitHub")
        return True, "Dados recarregados com sucesso"

    except Exception as e:
        logger.error(f"Erro ao recarregar versões: {e}")
        return False, f"Erro ao recarregar: {e}"
