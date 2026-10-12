# ============================================================
# Project: criptografia
# Module: encriptador.py
# Author: 0xander
# Watermark: created by 0xander | all rights reserved by the author
# Description: Professional encryption utilities based on ASCII
# and standard cryptography primitives (Fernet) for everyday use.
# ============================================================

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken 

if __package__ in (None, ""):
    ROOT = Path(__file__).resolve().parent.parent
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from criptografia.cifra_de_cesar.criptografar.encriptar_cifra import encriptar_cifra_de_cesar
    from criptografia.cifra_de_cesar.descriptografar.decriptar_crifra import decriptar_cifra_de_cesar
else:
    from .cifra_de_cesar.criptografar.encriptar_cifra import encriptar_cifra_de_cesar
    from .cifra_de_cesar.descriptografar.decriptar_crifra import decriptar_cifra_de_cesar

ASCII_MIN = 32
ASCII_MAX = 126
ASCII_RANGE = ASCII_MAX - ASCII_MIN + 1


def ascii_criptografar(texto: str, chave: int) -> str:
    """Encrypts a string using a printable ASCII rotation cipher."""
    if not isinstance(texto, str):
        raise TypeError("O texto deve ser uma string.")

    chave = int(chave) % ASCII_RANGE
    texto_criptografado: list[str] = []

    for caractere in texto:
        codigo = ord(caractere)
        if ASCII_MIN <= codigo <= ASCII_MAX:
            codigo_criptografado = ((codigo - ASCII_MIN + chave) % ASCII_RANGE) + ASCII_MIN
            texto_criptografado.append(chr(codigo_criptografado))
        else:
            texto_criptografado.append(caractere)

    return "".join(texto_criptografado)


def ascii_descriptografar(texto_criptografado: str, chave: int) -> str:
    """Decrypts ASCII rotation cipher output."""
    if not isinstance(texto_criptografado, str):
        raise TypeError("O texto criptografado deve ser uma string.")

    chave = int(chave) % ASCII_RANGE
    texto_original: list[str] = []

    for caractere in texto_criptografado:
        codigo = ord(caractere)
        if ASCII_MIN <= codigo <= ASCII_MAX:
            codigo_original = ((codigo - ASCII_MIN - chave) % ASCII_RANGE) + ASCII_MIN
            texto_original.append(chr(codigo_original))
        else:
            texto_original.append(caractere)

    return "".join(texto_original)


def encriptar_ascii(texto: str, chave: int) -> str:
    """Alias em português para a função principal de cifra ASCII."""
    return ascii_criptografar(texto, chave)


def descriptografar_ascii(texto_criptografado: str, chave: int) -> str:
    """Alias em português para descriptografia ASCII."""
    return ascii_descriptografar(texto_criptografado, chave)


def gerar_chave_fernet(caminho_chave: str | Path | None = None) -> bytes:
    """Generates a Fernet key and optionally stores it to disk."""
    chave = Fernet.generate_key()

    if caminho_chave is not None:
        caminho = Path(caminho_chave)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_bytes(chave)

    return chave


def carregar_chave_fernet(caminho_chave: str | Path) -> Fernet:
    """Loads a Fernet key from a file and returns a Fernet instance."""
    chave = Path(caminho_chave).read_bytes()
    return Fernet(chave)


def criptografar_arquivo(
    caminho_arquivo: str | Path,
    caminho_chave: str | Path,
    sobrescrever: bool = True,
) -> Path:
    """Encrypts a file using Fernet and writes the result beside the original file."""
    arquivo = Path(caminho_arquivo)
    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")

    chave = Path(caminho_chave)
    if not chave.exists():
        chave.write_bytes(Fernet.generate_key())

    fernet = carregar_chave_fernet(chave)
    dados = arquivo.read_bytes()
    dados_criptografados = fernet.encrypt(dados)

    arquivo_saida = arquivo.with_name(f"{arquivo.name}.enc")
    if arquivo_saida.exists() and not sobrescrever:
        raise FileExistsError(f"Arquivo de saída já existe: {arquivo_saida}")

    arquivo_saida.write_bytes(dados_criptografados)
    return arquivo_saida


def descriptografar_arquivo(
    caminho_arquivo_criptografado: str | Path,
    caminho_chave: str | Path,
    sobrescrever: bool = True,
) -> Path:
    """Decrypts a file encrypted with Fernet."""
    arquivo = Path(caminho_arquivo_criptografado)
    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo criptografado não encontrado: {arquivo}")

    fernet = carregar_chave_fernet(caminho_chave)
    dados_criptografados = arquivo.read_bytes()

    try:
        dados_originais = fernet.decrypt(dados_criptografados)
    except InvalidToken as exc:
        raise ValueError("Chave inválida ou arquivo corrompido.") from exc

    nome_saida = arquivo.name.removesuffix(".enc")
    arquivo_saida = arquivo.with_name(nome_saida)
    if arquivo_saida.exists() and not sobrescrever:
        raise FileExistsError(f"Arquivo de saída já existe: {arquivo_saida}")

    arquivo_saida.write_bytes(dados_originais)
    return arquivo_saida


def encriptar_arquivo(
    caminho_arquivo: str | Path,
    caminho_chave: str | Path,
    sobrescrever: bool = True,
) -> Path:
    """Alias em português em um único nome para o fluxo de criptografia de arquivos."""
    return criptografar_arquivo(caminho_arquivo, caminho_chave, sobrescrever=sobrescrever)


def descriptografar_arquivo_com_chave(
    caminho_arquivo_criptografado: str | Path,
    caminho_chave: str | Path,
    sobrescrever: bool = True,
) -> Path:
    """Alias para descriptografar arquivos com chave Fernet."""
    return descriptografar_arquivo(caminho_arquivo_criptografado, caminho_chave, sobrescrever=sobrescrever)


def banner_ascii() -> str:
    """Returns a professional ASCII-art banner for the cryptography tool."""
    return """
  ██████╗██████╗ ██╗██████╗ ███████╗██████╗ ███████╗██████╗ ██╗██╗   ██╗
 ██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗██╔════╝██╔══██╗██║██║   ██║
 ██║     ██████╔╝██║██████╔╝█████╗  ██████╔╝█████╗  ██████╔╝██║██║   ██║
 ██║     ██╔══██╗██║██╔═══╝ ██╔══╝  ██╔══██╗██╔══╝  ██╔══██╗██║██║   ██║
 ╚██████╗██║  ██║██║██║     ███████╗██║  ██║███████╗██║  ██║██║╚██████╔╝
  ╚═════╝╚═╝  ╚═╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝

                    0xander Security Tools
                    ASCII • César • Fernet
""".strip()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Criptografia profissional com ASCII, César e Fernet.")
    parser.add_argument("--texto", type=str, help="Texto em claro para criptografar ou descriptografar.")
    parser.add_argument("--chave", type=int, default=7, help="Chave numérica para a cifra ASCII.")
    parser.add_argument("--arquivo", type=str, help="Caminho do arquivo para criptografar/descriptografar.")
    parser.add_argument("--chave-arquivo", type=str, default="chave_simetrica.key", help="Arquivo da chave Fernet.")
    parser.add_argument("--acao", choices=["encrypt", "decrypt"], default="encrypt", help="Ação desejada.")
    return parser.parse_args()


def menu_interativo() -> None:
    """Menu terminal para escolher o método de criptografia e digitar a mensagem."""
    print("\n" + banner_ascii())
    print("============================================================")
    print("1. ASCII")
    print("2. César")
    print("3. Criptografar arquivo")
    print("4. Descriptografar arquivo")
    print("0. Sair")
    print("============================================================")

    escolha = input("Escolha uma opção: ").strip()

    if escolha == "0":
        print("Saindo...")
        return

    if escolha not in {"1", "2", "3", "4"}:
        print("Opção inválida.")
        return

    if escolha in {"3", "4"}:
        caminho_arquivo = input("Digite o caminho do arquivo: ").strip()
        caminho_chave = input("Digite o caminho da chave: ").strip() or "chave_simetrica.key"

        try:
            if escolha == "3":
                print("Arquivo gerado:", criptografar_arquivo(caminho_arquivo, caminho_chave))
            else:
                print("Arquivo restaurado:", descriptografar_arquivo(caminho_arquivo, caminho_chave))
        except Exception as exc:
            print(f"Erro: {exc}")
        return

    mensagem = input("Digite a mensagem: ")

    if escolha == "1":
        chave = int(input("Digite a chave ASCII (número): "))
        acao = input("Deseja criptografar ou descriptografar? [enc/dec]: ").strip().lower()
        if acao == "enc":
            print("Resultado:", ascii_criptografar(mensagem, chave))
        elif acao == "dec":
            print("Resultado:", ascii_descriptografar(mensagem, chave))
        else:
            print("Ação inválida. Use enc ou dec.")
        return

    if escolha == "2":
        chave = int(input("Digite a chave da Cifra de César: "))
        acao = input("Deseja criptografar ou descriptografar? [enc/dec]: ").strip().lower()
        if acao == "enc":
            print("Resultado:", encriptar_cifra_de_cesar(mensagem, chave))
        elif acao == "dec":
            print("Resultado:", decriptar_cifra_de_cesar(mensagem, chave))
        else:
            print("Ação inválida. Use enc ou dec.")
        return


if __name__ == "__main__":
    args = _parse_args()

    if args.texto is not None:
        if args.acao == "encrypt":
            resultado = ascii_criptografar(args.texto, args.chave)
        else:
            resultado = ascii_descriptografar(args.texto, args.chave)
        print(resultado)
    elif args.arquivo is not None:
        if args.acao == "encrypt":
            arquivo_saida = criptografar_arquivo(args.arquivo, args.chave_arquivo)
        else:
            arquivo_saida = descriptografar_arquivo(args.arquivo, args.chave_arquivo)
        print(f"Operação concluída: {arquivo_saida}")
    else:
        menu_interativo()


__all__ = [
    "ASCII_MIN",
    "ASCII_MAX",
    "ASCII_RANGE",
    "ascii_criptografar",
    "ascii_descriptografar",
    "encriptar_ascii",
    "descriptografar_ascii",
    "gerar_chave_fernet",
    "carregar_chave_fernet",
    "criptografar_arquivo",
    "descriptografar_arquivo",
    "encriptar_arquivo",
    "descriptografar_arquivo_com_chave",
]
