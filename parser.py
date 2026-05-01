from lexer import TT_ID, TT_NUM, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_POW, TT_LPAREN, TT_RPAREN, TT_COMMA, TT_ASSIGN, TT_EOF
from lexer import Token
from ast_nodes import *
from lexer import Scanner

class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = self.scanner.get_next_token()

    def error(self, message):
        raise Exception(f"Parser Error: {message} -> Current Token: {self.current_token}")

    def consume(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.scanner.get_next_token()
        else:
            self.error(f"Expected {token_type} but got {self.current_token.type}")

    # *** 1. Program Structure ***
    
    def program(self):
        # program -> decl_list stmt_list $$
        decls = self.decl_list()
        stmts = self.stmt_list()

        if self.current_token.type not in ['EOF', 'TT_EOF']:
            self.error(f"Parsing finished early! Unexpected token '{self.current_token.value}' found. \n"
                       f"Rule: Function Declarations must appear at the VERY TOP of the file.")
            
        return Program(decls, stmts)

    def decl_list(self):
        # decl_list -> decl decl_list | epsilon
        if self.current_token.type == 'FUNC':
            decl = self.func_decl()
            rest = self.decl_list()
            return [decl] + rest
        else:
            return []

    def func_decl(self):
        # func_decl -> 'func' id '(' param_list ')' ':=' expr
        self.consume('FUNC')
        name = self.current_token.value
        self.consume(TT_ID)
        self.consume(TT_LPAREN)
        params = self.param_list()
        self.consume(TT_RPAREN)
        self.consume(TT_ASSIGN)
        body = self.expr()
        return FuncDecl(name, params, body)

    def param_list(self):
        # param_list -> id param_tail | epsilon
        if self.current_token.type == TT_ID:
            param = self.current_token.value
            self.consume(TT_ID)
            rest = self.param_tail()
            return [param] + rest
        return []

    def param_tail(self):
        # param_tail -> ',' id param_tail | epsilon
        if self.current_token.type == TT_COMMA:
            self.consume(TT_COMMA)
            param = self.current_token.value
            self.consume(TT_ID)
            rest = self.param_tail()
            return [param] + rest
        return []

    def stmt_list(self):
        # stmt_list -> stmt stmt_list | epsilon
        # Check FIRST(stmt) to see if we should parse a statement
        if self.current_token.type in [TT_ID, 'READ', 'WRITE', 'DERIV']:
            stmt = self.stmt()
            rest = self.stmt_list()
            return [stmt] + rest
        return []

    def stmt(self):
        if self.current_token.type == TT_ID:
            # id ':=' expr
            name = self.current_token.value
            self.consume(TT_ID)
            self.consume(TT_ASSIGN)
            val = self.expr()
            return Assign(name, val)
        
        elif self.current_token.type == 'READ':
            self.consume('READ')
            name = self.current_token.value
            self.consume(TT_ID)
            return Read(name)
        
        elif self.current_token.type == 'WRITE':
            self.consume('WRITE')
            val = self.expr()
            return Write(val)
        
        elif self.current_token.type == 'DERIV':
            return self.derivative_stmt()
        
        else:
            self.error("Invalid statement")

    def derivative_stmt(self):
        # 'deriv' id '(' arg_list ')' 'wrt' id
        self.consume('DERIV')
        func_name = self.current_token.value
        self.consume(TT_ID)
        self.consume(TT_LPAREN)
        args = self.arg_list()
        self.consume(TT_RPAREN)
        self.consume('WRT')
        wrt_var = self.current_token.value
        self.consume(TT_ID)
        return Deriv(func_name, args, wrt_var)

    def arg_list(self):
        # arg_list -> expr arg_tail | epsilon
        # FIRST(expr) includes ID, NUM, LPAREN
        if self.current_token.type in [TT_ID, TT_NUM, TT_LPAREN]:
            arg = self.expr()
            rest = self.arg_tail()
            return [arg] + rest
        return []

    def arg_tail(self):
        if self.current_token.type == TT_COMMA:
            self.consume(TT_COMMA)
            arg = self.expr()
            rest = self.arg_tail()
            return [arg] + rest
        return []

    # *** 2. Math Expressions (The Recursive Logic) ***

    def expr(self):
        # expr -> term term_tail
        left = self.term()
        return self.term_tail(left)

    def term_tail(self, left_node):
        # term_tail -> add_op term term_tail | epsilon
        if self.current_token.type in [TT_PLUS, TT_MINUS]:
            op = self.current_token
            self.consume(op.type)
            right = self.term()
            # CRconsumeE NODE IMMEDIATELY (Left Associativity)
            new_left = BinOp(left_node, op, right)
            # RECURSE passing the new node as the 'left' for the next step
            return self.term_tail(new_left)
        return left_node

    def term(self):
        # term -> expo fact_tail
        left = self.expo()
        return self.fact_tail(left)

    def fact_tail(self, left_node):
        # fact_tail -> mult_op expo fact_tail | epsilon
        if self.current_token.type in [TT_MUL, TT_DIV]:
            op = self.current_token
            self.consume(op.type)
            right = self.expo()
            new_left = BinOp(left_node, op, right)
            return self.fact_tail(new_left)
        return left_node

    def expo(self):
        # expo -> factor expo_tail
        base = self.factor()
        return self.expo_tail(base)

    def expo_tail(self, base_node):
        # expo_tail -> '^' number | epsilon
        if self.current_token.type == TT_POW:
            op = self.current_token
            self.consume(TT_POW)
            
            # STRICT CHECK: The next token MUST be a number
            if self.current_token.type == TT_NUM:
                num_token = self.current_token
                self.consume(TT_NUM)
                right_side = Num(num_token)
                return BinOp(base_node, op, right_side)
            else:
                self.error("Exponent must be a number literal")
                
        return base_node

    def factor(self):
        # factor -> '(' expr ')' | number | id factor_tail
        token = self.current_token
        
        if token.type == TT_LPAREN:
            self.consume(TT_LPAREN)
            node = self.expr()
            self.consume(TT_RPAREN)
            return node
        
        elif token.type == TT_NUM:
            self.consume(TT_NUM)
            return Num(token)
        
        elif token.type == TT_ID:
            name = token.value
            self.consume(TT_ID)
            return self.factor_tail(name)
        
        else:
            self.error("Unexpected token in factor")

    def factor_tail(self, name):
        # factor_tail -> '(' arg_list ')' | epsilon
        if self.current_token.type == TT_LPAREN:
            # It's a Function Call
            self.consume(TT_LPAREN)
            args = self.arg_list()
            self.consume(TT_RPAREN)
            return FuncCall(name, args)
        else:
            # It's just a Variable
            return Var(Token(TT_ID, name))