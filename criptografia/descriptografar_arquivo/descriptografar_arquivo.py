# ============================================================
# Project: criptografia / descriptografar_arquivo
# Author: 0xander
# Watermark: created by 0xander | all rights reserved by the author
# Description: Decrypts a Fernet-encrypted file using the stored key.
# ============================================================

from __future__ import annotations

import argparse
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken


def carregar_chave(caminho_chave: str | Path) -> bytes:
    """Reads the Fernet key from disk."""
    return Path(caminho_chave).read_bytes()


def descriptografar_arquivo(caminho_arquivo_criptografado: str | Path, caminho_chave: str | Path) -> Path:
    """Decrypts a .enc file and writes the original data back to disk."""
    arquivo = Path(caminho_arquivo_criptografado)
    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo criptografado não encontrado: {arquivo}")

    chave = carregar_chave(caminho_chave)
    fernet = Fernet(chave)

    try:
        dados_descriptografados = fernet.decrypt(arquivo.read_bytes())
    except InvalidToken as exc:
        raise ValueError("Chave inválida ou arquivo corrompido.") from exc

    nome_original = arquivo.name.removesuffix(".enc")
    arquivo_saida = arquivo.with_name(nome_original)
    arquivo_saida.write_bytes(dados_descriptografados)
    return arquivo_saida


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Descriptografa um arquivo usando Fernet.")
    parser.add_argument("arquivo", help="Caminho do arquivo criptografado")
    parser.add_argument("--chave", default="chave_simetrica.txt", help="Arquivo da chave simétrica")
    args = parser.parse_args()

    arquivo_saida = descriptografar_arquivo(args.arquivo, args.chave)
    print(f"Arquivo descriptografado salvo em: {arquivo_saida}")
