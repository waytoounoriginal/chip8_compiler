chip8_compiler
--------------------------
A probably over-engineered compiler/assembler for the chip8 language.
Uses '.chip8' files.

To install the package use: : `pip install .`

To use simply do:
```python
import chip8_compiler as cc

... # your code

bytes = cc.parse_file(<your file>)
```

For cli usage you can do:
```
chip8_compiler [-h] -i INPUT [-o OUTPUT]
```

TODO:
* Add a preprocessor
* Tidy up the code
* Maybe go a bit in-depth over the whole process