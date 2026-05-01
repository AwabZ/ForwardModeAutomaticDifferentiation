TT_ID     = 'ID'
TT_NUM    = 'NUM'
TT_PLUS   = 'PLUS'
TT_MINUS  = 'MINUS'
TT_MUL    = 'MUL'
TT_DIV    = 'DIV'
TT_POW    = 'POW'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_COMMA  = 'COMMA'
TT_ASSIGN = 'ASSIGN'  
TT_EOF    = 'EOF'

# Keywords
KEYWORDS = {
    'func': 'FUNC',
    'read': 'READ',
    'write': 'WRITE',
    'deriv': 'DERIV',
    'wrt': 'WRT'
}

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

class Scanner:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception(f"Invalid character '{self.current_char}' at position {self.pos}")

    def advance(self):
        """Move the 'pointer' one position forward"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # EOF
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        """Look one character ahead without moving the pointer"""
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """Parse integers and floats"""
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        
        if '.' in result:
            return Token(TT_NUM, float(result))
        return Token(TT_NUM, int(result))

    def _id(self):
        """Parse identifiers and check if they are keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
            
        # Check if it's a keyword (like 'func' or 'deriv')
        token_type = KEYWORDS.get(result, TT_ID)
        return Token(token_type, result)

    def get_next_token(self):
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == ':':
                # Check for Assignment :=
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TT_ASSIGN)
                else:
                    self.error()

            if self.current_char == '+':
                self.advance()
                return Token(TT_PLUS)

            if self.current_char == '-':
                self.advance()
                return Token(TT_MINUS)

            if self.current_char == '*':
                self.advance()
                return Token(TT_MUL)

            if self.current_char == '/':
                self.advance()
                return Token(TT_DIV)
            
            if self.current_char == '^':
                self.advance()
                return Token(TT_POW)

            if self.current_char == '(':
                self.advance()
                return Token(TT_LPAREN)

            if self.current_char == ')':
                self.advance()
                return Token(TT_RPAREN)
            
            if self.current_char == ',':
                self.advance()
                return Token(TT_COMMA)


        return Token(TT_EOF)
    




