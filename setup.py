from setuptools import setup

setup(
    name="chip8_compiler",
    version="0.1",
    description="A probably over-engineered compiler/assembler for the chip8 language.",
    author="waytoounoriginal",
    author_email="mihai.tira@yahoo.ro",
    py_modules=["chip8_compiler"],
    entry_points={
        'console_scripts': ['chip8_compiler=chip8_compiler.chip8_cli:main']
    }
)
