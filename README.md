# MyYAPL Interpreter

MyYAPL (My Yet Another Programming Language) is a simple programming language interpreter implemented in Python. It supports basic data types, arithmetic operations, control structures, and user-defined structures (structs). The interpreter is built using the ply (Python Lex-Yacc) library, which provides lexical analysis and parsing capabilities.

# Features
**Basic Data Types:** int, double, string, bool, char

**Arithmetic Operations:** addition, subtraction, multiplication, division, modulus, exponentiation

**Comparison Operators:** <, >, <=, >=, ==, !=

**Logical Operators:** AND, OR, NOT

**Control Structures:** DO-WHILE loop

**User-Defined Structures:** Ability to define and use custom structs

**Print Statement:** Print values to the console

# Getting Started
To use the MyYAPL interpreter, follow these steps:

- Clone the repository or download the source code.
- Make sure you have Python 3.x installed on your system.
- Navigate to the project directory.
- Run the interpreter with your MyYAPL code file as an argument:
```python interpreter.py your_code_file.myy```
- Replace your_code_file.myy with the name of your MyYAPL code file.
- The interpreter will execute the code and print the output to the console.

# Project Structure
- interpreter.py: The main interpreter file that handles code execution and variable management.
- lexer.py: Defines the lexical rules and tokens for the MyYAPL language.
- parser.py: Defines the grammar rules and constructs the abstract syntax tree (AST) for the input code.
- test_cases/: Directory containing test cases for the interpreter.

# Example
Here's a simple MyYAPL program that calculates the sum of two numbers:
```
INT a;
INT b;
INT c;
a = 10;
b = 20;
c = a + b;
PRINT(c);
```
This program will output 30 to the console.
