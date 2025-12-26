import os
import shutil

SAFE_MODE = True  # MODO DE SEGURANÇA - NÃO MOVE ARQUIVOS

def set_safe_mode(value: bool):
    global SAFE_MODE
    SAFE_MODE = value


def get_safe_mode():
    return SAFE_MODE


def is_critical_path(path):
    path = os.path.abspath(path).lower()

    # raiz do disco (c:\, d:\ etc)
    if len(path) == 3 and path[1:] == ":\\":  
        return True

    blocked_exact = [
        "c:\\windows",
        "c:\\program files",
        "c:\\program files (x86)",
        "c:\\system volume information"
    ]

    for blocked in blocked_exact:
        if path == blocked or path.startswith(blocked + "\\"):
            return True

    if path == "c:\\users":
        return True

    return False



def organize_folder(path):
    if SAFE_MODE:
        raise RuntimeError(
            "SAFE_MODE ativo. Nenhum arquivo foi movido. "
            "Use apenas para testes."
        )

    arquivos_movidos = 0
    pastas_criadas = set()

    for nome_arquivo in os.listdir(path):
        caminho_completo = os.path.join(path, nome_arquivo)

        if not os.path.isfile(caminho_completo):
            continue

        _, extensao = os.path.splitext(nome_arquivo)

        if extensao == "":
            nome_pasta = "OUTROS"
        else:
            nome_pasta = extensao.replace(".", "").upper()

        pasta_destino = os.path.join(path, nome_pasta)
        os.makedirs(pasta_destino, exist_ok=True)

        destino_final = os.path.join(pasta_destino, nome_arquivo)

        contador = 1
        while os.path.exists(destino_final):
            nome_base, ext = os.path.splitext(nome_arquivo)
            destino_final = os.path.join(
                pasta_destino,
                f"{nome_base}_{contador}{ext}"
            )
            contador += 1

        shutil.move(caminho_completo, destino_final)

        arquivos_movidos += 1
        pastas_criadas.add(nome_pasta)

    return arquivos_movidos, len(pastas_criadas)

