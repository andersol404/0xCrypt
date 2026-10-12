"""Pacote de utilitários de criptografia do projeto 0xander."""

__all__ = [
    "ASCII_MIN",
    "ASCII_MAX",
    "ASCII_RANGE",
    "ascii_criptografar",
    "ascii_descriptografar",
    "encriptar_ascii",
    "descriptografar_ascii",
    "gerar_chave_fernet",
    "criptografar_arquivo",
    "descriptografar_arquivo",
    "encriptar_arquivo",
]


def __getattr__(name):
    if name in __all__:
        from .encriptador import (
            ASCII_MAX,
            ASCII_MIN,
            ASCII_RANGE,
            ascii_criptografar,
            ascii_descriptografar,
            criptografar_arquivo,
            descriptografar_arquivo,
            descriptografar_ascii,
            encriptar_ascii,
            encriptar_arquivo,
            gerar_chave_fernet,
        )

        mapping = {
            "ASCII_MIN": ASCII_MIN,
            "ASCII_MAX": ASCII_MAX,
            "ASCII_RANGE": ASCII_RANGE,
            "ascii_criptografar": ascii_criptografar,
            "ascii_descriptografar": ascii_descriptografar,
            "encriptar_ascii": encriptar_ascii,
            "descriptografar_ascii": descriptografar_ascii,
            "gerar_chave_fernet": gerar_chave_fernet,
            "criptografar_arquivo": criptografar_arquivo,
            "descriptografar_arquivo": descriptografar_arquivo,
            "encriptar_arquivo": encriptar_arquivo,
        }
        return mapping[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
