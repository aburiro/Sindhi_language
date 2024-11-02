import re

# Keywords dictionary for Sindhi keywords
KEYWORDS = {
    "جيڪڏهن": "IF",
    "ٻيو": "ELSE",
    "ڇپائي": "PRINT"
}

# Token regex patterns with Sindhi keywords and operators
TOKEN_REGEX = [
    (r'\s+', None),  # Ignore whitespace
    (r'جيڪڏهن', 'IF'),  # Sindhi 'if'
    (r'ٻيو', 'ELSE'),  # Sindhi 'else'
    (r'ڇپائي', 'PRINT'),  # Sindhi 'print'
    (r'\(', 'LPAREN'),  # (
    (r'\)', 'RPAREN'),  # )
    (r'\{', 'LBRACE'),  # {
    (r'\}', 'RBRACE'),  # }
    (r'[><=!]=?', 'COMPARE_OP'),  # Comparison operators
    (r'\d+', 'NUMBER'),  # Numbers
    (r'"[^"]*"', 'STRING')  # String literals
]

def tokenize(code):
    tokens = []
    while code:
        match = None
        for pattern, token_type in TOKEN_REGEX:
            regex = re.compile(pattern, re.UNICODE)  # Ensure Unicode pattern
            match = regex.match(code)
            if match:
                if token_type:
                    tokens.append((token_type, match.group(0)))
                code = code[match.end():]  # Move to the next part of the code
                break
        if not match:
            raise SyntaxError(f"غيرقانوني اکر: '{code[0]}'")  # Error in Sindhi for unrecognized characters
    return tokens

# IfNode represents an 'if' statement in the parse tree
class IfNode:
    def __init__(self, condition, if_statements, else_statements):
        self.condition = condition
        self.if_statements = if_statements
        self.else_statements = else_statements

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = tokens[self.current_token_index]

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]

    def expect_token(self, token_type):
        if self.current_token[0] == token_type:
            value = self.current_token[1]
            self.advance()
            return value
        else:
            raise SyntaxError(f"توقع آهي '{token_type}', پر مليو '{self.current_token[1]}'")

    def parse_if_statement(self):
        # Expect 'جيڪڏهن' (IF)
        self.expect_token('IF')

        # Expect '(' after 'جيڪڏهن'
        self.expect_token('LPAREN')

        # Parse the condition (e.g., `2 > 6`)
        condition = self.parse_expression()

        # Expect ')' after the condition
        self.expect_token('RPAREN')

        # Expect '{' to start the block
        self.expect_token('LBRACE')

        # Parse the statements inside the if block
        if_statements = self.parse_statements()

        # Expect '}' to end the if block
        self.expect_token('RBRACE')

        # Check for 'ٻيو' (else)
        else_statements = None
        if self.current_token[0] == 'ELSE':
            self.advance()  # Move past 'ELSE'

            # Expect '{' for the else block
            self.expect_token('LBRACE')

            # Parse the statements inside the else block
            else_statements = self.parse_statements()

            # Expect '}' to end the else block
            self.expect_token('RBRACE')

        return IfNode(condition, if_statements, else_statements)

    def parse_expression(self):
        # Parse a simple comparison expression like `2 > 6`
        left = self.expect_token('NUMBER')  # Expect a number on the left side, like `2`
        op = self.expect_token('COMPARE_OP')  # Expect a comparison operator (e.g., `>`)
        right = self.expect_token('NUMBER')  # Expect another number on the right side, like `6`
        return (left, op, right)  # Return the parsed condition as a tuple

    def parse_statements(self):
        # Check if the next statement is a print statement
        if self.current_token[0] == 'PRINT':
            self.expect_token('PRINT')
            self.expect_token('LPAREN')
            string_literal = self.expect_token('STRING')
            self.expect_token('RPAREN')
            return f"Print statement: {string_literal}"
        return None

def main():
    # Test code in Sindhi directly
    code = """
جيڪڏهن (2 < 6) {
    ڇپائي("خوش آمديد سنڌي زبان")
} ٻيو {
    ڇپائي("خوش آمديد سنڌي زبان")
}
"""

    try:
        # Tokenize the input code
        tokens = tokenize(code)
        
        # Initialize the parser with tokens
        parser = Parser(tokens)
        
        # Parse the code
        parsed_result = parser.parse_if_statement()

        # Output the parsed structure
        print("Parsing successful!")
        print("Condition:", parsed_result.condition)
        print("If statements:", parsed_result.if_statements)
       # if parsed_result.else_statements:
      #      print("Else statements:", parsed_result.else_statements)

    except SyntaxError as e:
        print("Syntax Error:", e)

if __name__ == "__main__":
    main()
