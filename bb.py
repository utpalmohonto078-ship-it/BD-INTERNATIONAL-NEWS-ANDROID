import sys
from pathlib import Path
from compiler.lexer import tokenize
from compiler.parser import parse
from compiler.semantic import analyze
from compiler.ir import generate
from compiler.bytecode import compile_ir
from runtime.vm import VirtualMachine

def compile_source(source):
    ast = parse(tokenize(source))
    analyze(ast)
    return compile_ir(generate(ast))

def run_source(source, input_fn=None):
    return VirtualMachine(input_fn=input_fn).run(compile_source(source))

MAX_SOURCE_BYTES = 1024 * 1024


def read_source_file(path):
    path = Path(path)
    with path.open("rb") as source_file:
        data = source_file.read(MAX_SOURCE_BYTES + 1)

    if len(data) > MAX_SOURCE_BYTES:
        raise ValueError(
            f"Source file exceeds the {MAX_SOURCE_BYTES}-byte limit"
        )

    return data.decode("utf-8")


def main():
    if len(sys.argv) != 2:
        print("Usage: python bb.py FILE.bb")
        raise SystemExit(2)

    path = Path(sys.argv[1])

    try:
        source = read_source_file(path)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)

    for result in run_source(source):
        print(result)

if __name__ == "__main__":
    main()
