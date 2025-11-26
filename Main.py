import sys
from antlr4 import *
from DLangLexer import DLangLexer
from DLangParser import DLangParser
from EvalVisitor import EvalVisitor


def run_code(code, visitor):
    input_stream = InputStream(code)
    lexer = DLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = DLangParser(stream)
    tree = parser.program()
    visitor.visit(tree)


def main():
    visitor = EvalVisitor()

    if len(sys.argv) > 1:
        # Ejecutar archivo .dl
        filename = sys.argv[1]
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
        run_code(code, visitor)
    else:
        # REPL simple
        print("DLang (lenguaje para operaciones matematicas, matrices y graficas).")
        print("Escribe 'exit' para salir.")
        while True:
            try:
                line = input(">>> ")
            except EOFError:
                break

            if line.strip() in ("exit", "quit"):
                break
            if not line.strip():
                continue

            run_code(line, visitor)


if __name__ == "__main__":
    main()
