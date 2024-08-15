import cProfile

import chip8_compiler as cc

if __name__ == "__main__":
    cProfile.run("cc.parse_file(file_path='../time_10k_test.chip8')")