import argparse

import chip8_compiler as cc


def is_chip8_file(file_path: str) -> str:
    if not file_path.endswith('.chip8'):
        raise argparse.ArgumentTypeError("Input file must have a '.chip8' extension")
    return file_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Allows assembly of '.chip8' files.")
    parser.add_argument(
        "-i", "--input",
        help="The path to the input file.",
        required=True,
        type=is_chip8_file
    )
    parser.add_argument(
        "-o", "--output",
        help="The path to the output file.",
        default="./tmp.ch8",
        nargs=1
    )

    args = parser.parse_args()
    compiled_bytecode: bytes = cc.parse_file(file_path=args.input)

    # Write to the file
    with open(args.output, "wb") as f:
        f.write(compiled_bytecode)
