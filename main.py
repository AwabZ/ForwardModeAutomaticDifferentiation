from lexer import Scanner
from parser import Parser
from interpreter import Interpreter


source_code = """
func f(x) := x^3 +/ 2*x 
         
read y
z := y + 10
write z

deriv f(6) wrt x
"""

def main():
    print("*** RAW SOURCE CODE ***")
    print(source_code)
    print("***********************")

    try:
        # Scan
        scanner = Scanner(source_code)
        
        # Parse
        parser = Parser(scanner)
        ast = parser.program()

        # Interpret
        print("*** EXECUTION ***")
        interpreter = Interpreter(parser)
        interpreter.visit(ast)

    except Exception as e:
        print(f"CRASH: {e}")

if __name__ == "__main__":
    main()

