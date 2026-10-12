# ============================================================
# Repository: criptografia / cifra_de_cesar / criptografar
# Script: encriptar_cifra.py
# Author: 0xander
# Watermark: created by 0xander | all rights reserved by the author
# Description: Professional Caesar cipher implementation with
#            ASCII-safe handling and readability improvements.
# ============================================================


def encriptar_cifra_de_cesar(cifra: str, chave: int) -> str:
    """Encrypts text using the Caesar cipher over the A-Z alphabet."""
    alfabeto: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cifra_encriptada: list[str] = []

    for letra in cifra:
        if letra.isalpha():
            original = letra.upper()
            index_alfabeto = alfabeto.index(original)
            index_letra_encriptada = (index_alfabeto + chave) % len(alfabeto)
            letra_encriptada = alfabeto[index_letra_encriptada]

            if letra.islower():
                letra_encriptada = letra_encriptada.lower()

            cifra_encriptada.append(letra_encriptada)
        else:
            cifra_encriptada.append(letra)

    return "".join(cifra_encriptada)


if __name__ == "__main__":
    mensagem = "O governo nos observa!"
    print(encriptar_cifra_de_cesar(mensagem, 10))
    # Output esperado: "Yvk Wgxly!"
