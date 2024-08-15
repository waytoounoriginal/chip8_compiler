import chip8_compiler as cc

compiled_bytecodes: bytes = cc.parse_file(file_path="./hello_world_test.chip8")
with open("hello_world_program.ch8", "wb") as f:
    f.write(compiled_bytecodes)