# MyFile.py
# Diccionario global que actúa como "sistema de archivos"
FS = {}

def write_text(path, content):
    """
    Escribe (o crea) un archivo en el FS simulado.
    """
    FS[path] = str(content)

def append_text(path, content):
    """
    Agrega contenido al final del archivo simulado.
    """
    if path not in FS:
        FS[path] = ""
    FS[path] += str(content)

def read_text(path):
    """
    Devuelve el contenido completo del archivo simulado.
    """
    if path not in FS:
        raise ValueError(f"Archivo no encontrado: {path}")
    return FS[path]

def read_lines(path):
    """
    Lee el archivo y devuelte una lista de líneas (sin \n).
    """
    if path not in FS:
        raise ValueError(f"Archivo no encontrado: {path}")
    return FS[path].split("\n")
