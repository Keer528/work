import sys

class PredictiveParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first = {}
        self.follow = {}
        self.predictive_table = {}

    def compute_first(self, symbol):
        first_set = set()
        if symbol not in self.grammar:
            return {symbol}
        productions = self.grammar[symbol]
        for production in productions:
            if production[0] not in self.grammar.keys():  # Terminal symbol
                first_set.add(production[0])
            elif production[0] == symbol:  # Recursive production
                continue
            else:
                first_set = first_set.union(self.compute_first(production[0]))
        return first_set

    def compute_follow(self, symbol):
        follow_set = set()
        for key in self.grammar.keys():
            for production in self.grammar[key]:
                if symbol in production:
                    idx = production.index(symbol)
                    if idx == len(production) - 1:
                        if key != symbol:
                            follow_set = follow_set.union(self.compute_follow(key))
                    else:
                        next_symbol = production[idx + 1]
                        if next_symbol not in self.grammar.keys():
                            follow_set.add(next_symbol)
                        else:
                            first_next = self.compute_first(next_symbol)
                            if "ɛ" in first_next:
                                follow_set = follow_set.union(first_next.difference({"ɛ"}))
                                follow_set = follow_set.union(self.compute_follow(key))
                            else:
                                follow_set = follow_set.union(first_next)
        return follow_set

    def build_first_set(self):
        for key in self.grammar.keys():
            self.first[key] = self.compute_first(key)

    def build_follow_set(self):
        for key in self.grammar.keys():
            self.follow[key] = set()

        start_symbol = list(self.grammar.keys())[0]
        self.follow[start_symbol] = {"$"}

        for key in self.grammar.keys():
            self.follow[key] = self.compute_follow(key)
            self.follow[key].add("$")

    def build_predictive_table(self):
        self.build_first_set()
        self.build_follow_set()
        for non_terminal, productions in self.grammar.items():
            for production in productions:
                first_of_production = self.compute_first(production[0])
                if 'ɛ' in first_of_production:
                    first_of_production.remove('ɛ')
                    for terminal in self.follow[non_terminal]:
                        self.predictive_table[(non_terminal, terminal)] = production
                for terminal in first_of_production:
                    self.predictive_table[(non_terminal, terminal)] = production
                if 'ɛ' in first_of_production or len(first_of_production) == 0:
                    for terminal in self.follow[non_terminal]:
                        self.predictive_table[(non_terminal, terminal)] = production
            for terminal in self.follow[non_terminal]:
                if (non_terminal, terminal) not in self.predictive_table:
                    self.predictive_table[(non_terminal, terminal)] = 'error'

    def parse(self, input_string):
        stack = ['$']
        input_string += ' $'
        stack.append(list(self.grammar.keys())[0])  # Starting symbol
        parsing_steps = []
        while len(stack) > 0:
            top_stack = stack[-1]
            current_input = input_string[0]
            if top_stack == current_input == '$':
                parsing_steps.append((stack[-1], current_input))
                return True, parsing_steps
            elif top_stack == current_input:
                parsing_steps.append((stack[-1], current_input))
                stack.pop()
                input_string = input_string[1:]
            elif top_stack in self.grammar.keys():
                if (top_stack, current_input) in self.predictive_table:
                    if self.predictive_table[(top_stack, current_input)] == 'error':
                        parsing_steps.append((stack[-1], current_input))
                        return False, parsing_steps
                    stack.pop()
                    production = self.predictive_table[(top_stack, current_input)]
                    if production != 'ɛ':
                        production = production[::-1]
                        stack.extend(production)
                    parsing_steps.append((top_stack, production))
                else:
                    return False, parsing_steps
            else:
                return False, parsing_steps
        return False, parsing_steps


grammar = {
    'E': ['TQ'],
    'Q': ['+TQ', '-TQ', 'ɛ'],
    'T': ['FR'],
    'R': ['*FR', '/FR', 'ɛ'],
    'F': ['(E)', 'a']
}

predictive_parser = PredictiveParser(grammar)
predictive_parser.build_predictive_table()

print("FIRST集:")
for key, value in predictive_parser.first.items():
    print(f"FIRST({key}): {value}")

print("\nFOLLOW集:")
for key, value in predictive_parser.follow.items():
    print(f"FOLLOW({key}): {value}")

predictive_parser.build_predictive_table()
print("\n预测分析表:")
for key, value in predictive_parser.predictive_table.items():
    if value != 'error':
        print(f"Parsing Table[{key[0]}, {key[1]}]: {value}")

# 测试字符串
test_strings = [
    "(a+a)$",
    "(a+a)e"
]

print("\n字符串分析结果:")
for test_str in test_strings:
    result, parsing_steps = predictive_parser.parse(test_str)
    print(f"'{test_str}': {'String is accepted/ valid' if result else 'String is not accepted/ In valid'}")


for test_str in test_strings:
    stack = ['$']
    test_str += ' $'
    stack.append(list(grammar.keys())[0])  # Starting symbol
    step = 0
    while len(stack) > 0:
        top_stack = stack[-1]
        current_input = test_str[0]
        if top_stack == current_input == '$':
            if len(stack) == 1:
                break
            print(f"Stack: {stack}")
            stack.pop()
            break
        elif top_stack == current_input:
            stack.pop()
            test_str = test_str[1:]
        elif top_stack in grammar.keys():
            if (top_stack, current_input) in predictive_parser.predictive_table:
                if predictive_parser.predictive_table[(top_stack, current_input)] == 'error':
                    break
                stack.pop()
                production = predictive_parser.predictive_table[(top_stack, current_input)]
                if production != 'ɛ':
                    production = production[::-1]
                    stack.extend(production)
            else:
                break
        step += 1
print(f"Stack: {stack}")





            

