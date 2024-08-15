import unittest
from timeit import default_timer as timer

import chip8_compiler as cc

# bytecodes = cc.parse_file(file_path="./hello_world_test.chip8")
#
# with open("parsed_test.ch8", "wb") as f:
#     for code in bytecodes:
#         f.write(code)


class TestInstructions(unittest.TestCase):

    def test_all_instructions(self):
        compiled_bytecodes = cc.parse_file(file_path="./instruction_test_input.chip8")

        with open("./instruction_test_expected.ch8", "rb") as f:
            expected_bytecodes = f.read()

        self.assertEqual(compiled_bytecodes, expected_bytecodes, "Byte codes not equal")

    def test_special_token(self):
        compiled_bytecodes = cc.parse_file(file_path="./special_token_test.chip8")

        with open("./special_token_test_expected.ch8", "rb") as f:
            expected_bytecodes = f.read()

        self.assertEqual(compiled_bytecodes, expected_bytecodes, "Byte codes not equal")

    def test_time_1k(self):
        # We want to have a time under 0.01 seconds
        start = timer()
        compiled_bytecodes = cc.parse_file(file_path="./time_1k_test.chip8")
        end = timer()
        print("TIME TAKEN (1k):", end - start, "SECONDS")

        self.assertLess(end - start, 0.012, "Time is greater than 0.01 seconds")

    def test_time_10k(self):
        # We want to have a time under 0.01 seconds
        start = timer()
        compiled_bytecodes = cc.parse_file(file_path="./time_10k_test.chip8")
        end = timer()
        print("TIME TAKEN (10k):", end - start, "SECONDS")

        self.assertLess(end - start, 0.12, "Time is greater than 0.01 seconds")


if __name__ == "__main__":
    unittest.main()
