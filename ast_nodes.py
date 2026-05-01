class AST:
    pass

class Program(AST):
    def __init__(self, func_decls, stmts):
        self.func_decls = func_decls  # List[FuncDecl]
        self.stmts = stmts            # List[Stmt]

    def __repr__(self):
        return f"Program(Decls={len(self.func_decls)}, Stmts={len(self.stmts)})"

# Statements
class FuncDecl(AST):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params  # List[str]
        self.body = body      # Expr Node

class Stmt(AST):
    pass

class Assign(Stmt):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Read(Stmt):
    def __init__(self, name):
        self.name = name

class Write(Stmt):
    def __init__(self, expr):
        self.expr = expr

class Deriv(Stmt):
    def __init__(self, func_name, args, wrt):
        self.func_name = func_name
        self.args = args      # List[Expr]
        self.wrt = wrt        # str (variable name)

# Expressions
class Expr(AST):
    pass

class BinOp(Expr):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op          # Token
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.op.type} {self.right})"

class FuncCall(Expr):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Var(Expr):
    def __init__(self, token):
        self.name = token.value
    def __repr__(self):
        return f"Var({self.name})"

class Num(Expr):
    def __init__(self, token):
        self.value = token.value
    def __repr__(self):
        return f"{self.value}"