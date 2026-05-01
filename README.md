# 📐 AutoDiff-Lang: Forward Mode Automatic Differentiation Interpreter
A custom-built interpreted language designed to perform Forward Mode Automatic Differentiation (AD) using Dual Numbers. This project implements a complete pipeline, from a hand-written Lexer and Recursive Descent Parser to a specialized Interpreter that evaluates derivatives as a first-class operation.

# 🚀 Features
⚡ Automatic Differentiation: Evaluate exact derivatives using the deriv keyword, no finite difference approximations needed.  

🔢 Dual Number Arithmetic: Core engine implements Dual objects where every number carries its own derivative bit.  

🌳 Custom AST: Hand-built Abstract Syntax Tree with nodes for variable assignment, function declarations, and mathematical expressions.  

🔧 Hand-Written Lexer & Parser: A robust Scanner and Parser implementation supporting operator precedence and function scoping.


# 🛠️ Core Components
### The Dual Number Engine (dual.py):
At the heart of the interpreter is the Dual class. It overrides standard Python arithmetic operators to propagate derivatives using the chain rule:
Addition/Subtraction: $(f + g)' = f' + g'$  
Multiplication: $(f \cdot g)' = f \cdot g' + f' \cdot g$  
Division: $(f / g)' = (f' \cdot g - f \cdot g') / g^2$  
Power: $(x^n)' = n \cdot x^{n-1} \cdot x'$  2. 

### The Interpreter (interpreter.py):
The interpreter uses the Visitor Pattern to walk the AST. When the deriv command is encountered, it "seeds" the target variable with a derivative of 1.0 and all other variables with 0.0, then evaluates the function body to extract the exact derivative.

# 📝 Language Syntax:
The language supports function declarations, standard variable operations, and the derivative statement. 
```
#1. Define a function
func f(x) := x^3 + 2*x 

#2. Variable operations
read y
z := y + 10
write z

#3. Calculate derivative: f'(6) with respect to x 
deriv f(6) wrt x
```

# 💻 Technical Implementation Details
### Lexer (lexer.py)
A standard Scanner that converts raw text into tokens like TT_ID, TT_NUM, and keywords such as func or deriv.  

### Parser (parser.py)
A Recursive Descent Parser that handles mathematical precedence:  

Expressions/Terms: Handles + and -.  

Factors: Handles * and /.  

Exponents: Handles ^ (Note: Exponents must be number literals).  

### AST Nodes (ast_nodes.py)
Defines the structure of the program, separating Statements (Assign, Read, Write, Deriv) from Expressions (BinOp, FuncCall, Var, Num).


# 🏃 Getting Started:
To run the interpreter, simply execute the main.py file. It will process the hardcoded source_code or can be modified to read from a file. 
```python main.py```
##### Example Execution Flow
- Scan: Raw text becomes a token stream.  
- Parse: Tokens are structured into a Program AST.  
- Visit: The Interpreter visits nodes, using Dual objects for all calculations to maintain derivative data. 



