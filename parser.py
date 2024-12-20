class Parser:
    def __init__(self):
        self.rules = {}  # Dictionary to store grammar rules
        self.input_string = []  # Input string to check
        self.success = False  # Parsing success flag

    def input_grammar(self):
        """Method to input grammar rules dynamically."""
        self.rules.clear()
        print("\n\U0001F449 Grammars \U0001F448")
        for non_terminal in ['S', 'B']:  # Two non-terminals: S and B
            print(f"Enter rule number 1 for non-terminal '{non_terminal}': ", end="")
            rule1 = input().strip()
            print(f"Enter rule number 2 for non-terminal '{non_terminal}': ", end="")
            rule2 = input().strip()
            self.rules[non_terminal] = [rule1, rule2]
        print("\nGrammar stored successfully!\n")
        
        # Check if the grammar is simple after input
        self.check_grammar_simple()

    def check_nullable(self):
        """Check for nullable rules (rules that can produce the empty string)."""
        nullable = set()
        for non_terminal, productions in self.rules.items():
            for production in productions:
                if production == 'ε':  # If production can generate an empty string
                    nullable.add(non_terminal)
        return nullable

    def check_terminal_first(self):
        """Check if the grammar follows the 'A → a alpha' rule (right-hand side starts with terminal)."""
        for non_terminal, productions in self.rules.items():
            for production in productions:
                if not production[0].islower():  # If the first symbol isn't terminal
                    print(f"Production '{non_terminal} → {production}' doesn't start with a terminal.")
                    return False
        return True

    def check_disjoint(self):
        """Check for disjoint sets in the grammar (no two rules start with the same terminal)."""
        for non_terminal, productions in self.rules.items():
            seen_terminals = set()
            for production in productions:
                if production:  # Ensure the production isn't empty
                    first_symbol = production[0]
                    if first_symbol in seen_terminals:
                        print(f"Disjoint violation: Two rules for '{non_terminal}' start with '{first_symbol}'")
                        return False
                    seen_terminals.add(first_symbol)
        return True

    def is_simple_grammar(self):
        """Check if the grammar is simple based on the provided conditions."""
        nullable = self.check_nullable()
        if nullable:
            print("The grammar is not simple (contains nullable rules).")
            return False
        
        if not self.check_terminal_first():
            print("The grammar is not simple (does not follow 'A → a alpha' form).")
            return False
        
        if not self.check_disjoint():
            print("The grammar is not simple (contains disjoint violations).")
            return False

        print("The grammar is simple.")
        return True

    def check_grammar_simple(self):
        """Check and display if the grammar is simple or not."""
        if not self.is_simple_grammar():
            print("The grammar is not simple.")
        else:
            print("The grammar is simple.")

    def parse_string(self, stack, index):
        """Recursive function for parsing with backtracking."""
        if not stack:  # If stack is empty
            return index == len(self.input_string)  # Check if input is fully consumed

        top = stack.pop()
        print(f"Stack after checking: {stack}")
        print(f"The rest of unchecked string: {self.input_string[index:]}")

        # Terminal match
        if top.islower():
            if index < len(self.input_string) and top == self.input_string[index]:
                print(f"Matched terminal: '{top}'")
                return self.parse_string(stack[:], index + 1)  # Move input pointer
            else:
                return False  # Terminal mismatch

        # Non-terminal expansion with backtracking
        elif top in self.rules:
            for production in self.rules[top]:  # Try each rule for the non-terminal
                print(f"Expanding '{top}' -> {production}")
                new_stack = stack[:]  # Copy current stack
                for symbol in reversed(production):  # Push production in reverse
                    new_stack.append(symbol)

                if self.parse_string(new_stack, index):  # Recursive call
                    return True  # If successful, return True
            return False  # All productions failed
        else:
            return False  # Invalid symbol

    def run(self):
        """Main loop to run the parser interactively."""
        while True:
            print("============================================")
            print("1-Another Grammar.")
            print("2-Another String.")
            print("3-Exit")
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                self.input_grammar()
            elif choice == '2':
                if not self.rules:
                    print("Please input the grammar first!")
                    continue
                print("Enter the string you want to be checked: ", end="")
                self.input_string = list(input().strip())
                print(f"The input String: {self.input_string}")
                self.success = self.parse_string(['S'], 0)  # Start with 'S' on the stack
                if self.success:
                    print("The string is accepted by the grammar.")
                else:
                    print("The string is not accepted by the grammar.")
            elif choice == '3':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice! Try again.")

if __name__ == "__main__":
    parser = Parser()
    parser.run()
