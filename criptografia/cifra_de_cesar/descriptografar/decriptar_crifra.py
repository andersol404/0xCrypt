# ============================================================
# Repository: criptografia / cifra_de_cesar / descriptografar
# Script: decriptar_crifra.py
# Author: 0xander
# Watermark: created by 0xander | all rights reserved by the author
# Description: Decrypts Caesar cipher text using a clean and
#              professional modulo-based implementation.
# ============================================================


def decriptar_cifra_de_cesar(cifra: str, chave: int) -> str:
    """Decrypts text encrypted by the Caesar cipher."""
    alfabeto: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cifra_decriptada: list[str] = []

    for letra in cifra:
        if letra.isalpha():
            original = letra.upper()
            index_alfabeto = alfabeto.index(original)
            index_letra_decriptada = (index_alfabeto - chave) % len(alfabeto)
            letra_decriptada = alfabeto[index_letra_decriptada]

            if letra.islower():
                letra_decriptada = letra_decriptada.lower()

            cifra_decriptada.append(letra_decriptada)
        else:
            cifra_decriptada.append(letra)

    return "".join(cifra_decriptada)


if __name__ == "__main__":
    print(decriptar_cifra_de_cesar("Yvk Wgxly!", 10))
    # Output esperado: "Ola Mundo!"
