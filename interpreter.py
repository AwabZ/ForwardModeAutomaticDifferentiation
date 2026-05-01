from lexer import TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_POW
from ast_nodes import *
from dual import *

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.functions = {}  # Store function definitions (FuncDecl nodes)
        self.globals = {}    # Store global variables (Dual objects)

    def visit(self, node, scope=None):
        """
        This function looks at the type of the node
        and calls the appropriate specific visit method.
        """
        if scope is None:
            scope = self.globals

        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, scope)

    def generic_visit(self, node, scope):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    # *** 1. Program & Declaration ***

    def visit_Program(self, node, scope):
        # Register all functions first
        for decl in node.func_decls:
            self.visit(decl, scope)
        
        # Execute all statements
        for stmt in node.stmts:
            self.visit(stmt, scope)

    def visit_FuncDecl(self, node, scope):
        # (node) is a FuncDecl Node (name, params, body)
        # Store the function node in the registry
        self.functions[node.name] = node

    # *** 2. Statements ***

    def visit_Assign(self, node, scope):
        #(node) is an assignment node (name, expr)
        value = self.visit(node.expr, scope) #(node.expr) is an expression node
        scope[node.name] = value  # Save to symbol table

    def visit_Read(self, node, scope):
        # Runtime input. (node) is a Read node (name).
        val_str = input(f"Enter value for {node.name}: ")
        try:
            val = float(val_str)
            scope[node.name] = Dual(val, 0.0) # Constants have 0 derivative
        except ValueError:
            print(f"Error: '{val_str}' is not a valid number.")

    def visit_Write(self, node, scope):
        # Print to console. (node) is a write node (expr).
        value = self.visit(node.expr, scope) #(node.expr) is an expression node.
        print(f"Output: {value.real}") # Print the real value
        

    def visit_Deriv(self, node, scope):
        # This is the Forward Mode AD logic
        
        # Look up function
        func_def = self.functions.get(node.func_name)
        if not func_def:
            raise Exception(f"Function '{node.func_name}' not defined.")

        if len(node.args) != len(func_def.params):
            raise Exception(f"Function '{node.func_name}' expects {len(func_def.params)} args, got {len(node.args)}.")

        # Prepare the local scope for the function execution
        local_scope = {}
        
        # Evaluate arguments and seed the Dual numbers
        # node.wrt is the name of the variable we are differentiating with respect to.
        
        for param_name, arg_expr in zip(func_def.params, node.args): 
            # Evaluate the argument expression  # In case the argument is an expression and not a constant 
            arg_val = self.visit(arg_expr, scope)  #Zip each FuncDef.params = [x,y,..] with FuncCall.args = [1.5, 2,...] = [(x, 1.5), (y, 2)]
            
            # Check if this parameter is the 'wrt' target
            if param_name == node.wrt:
                # SEED: value=arg, derivative=1.0
                local_scope[param_name] = Dual(arg_val.real, 1.0)
            else:
                # CONSTANT: value=arg, derivative=0.0
                local_scope[param_name] = Dual(arg_val.real, 0.0)

        # Execute the function body in the LOCAL scope
        result = self.visit(func_def.body, local_scope)

        # Output the result (The Derivative is the Dual part)
        print(f"Derivative of {node.func_name} w.r.t {node.wrt} at point {node.args} is: {result.dual}")

    # *** 3. Expressions ***

    def visit_BinOp(self, node, scope):
        # (node) is a BinOp node (left, op, right)
        # Either of node.left or node.right could be any sort of expression (Num, Var, FuncCall, BinOp)
        left = self.visit(node.left, scope)  # Both will keep recursing until they both just contain Dual Objects.
        right = self.visit(node.right, scope)
        # Since these (left) and (Right) will be Dual objects, the operators are defined based on Dual operations of Dual Class. 
        if node.op.type == TT_PLUS:
            return left + right
        elif node.op.type == TT_MINUS:
            return left - right
        elif node.op.type == TT_MUL:
            return left * right
        elif node.op.type == TT_DIV:
            return left / right
        elif node.op.type == TT_POW:
            return left ** right.real

    def visit_Num(self, node, scope):
        # (node) is a NUM node (value)
        # Wrap in a Dual object and return
        return Dual(node.value, 0.0) # (node.value) is a number.

    def visit_Var(self, node, scope):
        # (node) is a VAR node (name)
        val = scope.get(node.name) #(node.name) 
        if val is None:
            raise Exception(f"Variable '{node.name}' not defined.")
        return val

    def visit_FuncCall(self, node, scope):
        # Standard function call (not a derivative)
        # (node) is a FuncCall node (name, args)
        func_def = self.functions.get(node.name) #get that FuncDef node
        if not func_def:    #If DNE, error.
            raise Exception(f"Function '{node.name}' not defined.") 

        local_scope = {}    #Define a local scope for evaluation to avoid global scope pollution (accidental overriding/utilization of incorrect values).
        for param_name, arg_expr in zip(func_def.params, node.args): #Zip each FuncDef.params = [x,y,..] with FuncCall.args = [1.5, 2,...] = [(x, 1.5), (y, 2)]
            arg_val = self.visit(arg_expr, scope) # In case the argument is an expression and not a constant 
            local_scope[param_name] = arg_val   # Save all (param:value) pairs to local scope.

        return self.visit(func_def.body, local_scope) # visit some expression function because (func_def.body) is an expression that could be anything (Use local scope parameters).





        