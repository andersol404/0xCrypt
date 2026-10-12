from pathlib import Path
import argparse

from cryptography.fernet import Fernet


def gerar_chave(caminho_chave: str | Path) -> bytes:
    caminho = Path(caminho_chave)

    if caminho.exists():
        return caminho.read_bytes()

    chave = Fernet.generate_key()
    caminho.write_bytes(chave)
    return chave


def criptografar_arquivo(caminho_arquivo: str | Path, caminho_chave: str | Path) -> Path:
    arquivo = Path(caminho_arquivo)
    chave = gerar_chave(caminho_chave)

    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")

    dados = arquivo.read_bytes()
    fernet = Fernet(chave)
    dados_criptografados = fernet.encrypt(dados)

    arquivo_criptografado = arquivo.with_name(f"{arquivo.name}.enc")
    arquivo_criptografado.write_bytes(dados_criptografados)
    return arquivo_criptografado


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Criptografa um arquivo usando Fernet.")
    parser.add_argument("arquivo", help="Caminho do arquivo a ser criptografado")
    parser.add_argument(
        "--chave",
        default="chave_simetrica.txt",
        help="Caminho do arquivo da chave simétrica (padrão: chave_simetrica.txt)",
    )
    args = parser.parse_args()

    arquivo_saida = criptografar_arquivo(args.arquivo, args.chave)
    print(f"Arquivo criptografado salvo em: {arquivo_saida}")
