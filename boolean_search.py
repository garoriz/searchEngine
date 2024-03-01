AND = "AND"
OR = "OR"
NOT = 'NOT'

Operators = {'AND', 'OR', 'NOT', '(', ')'}

Priority = {'OR': 1, 'AND': 2, 'NOT': 3}

all_doc_ids = {str(doc_id) for doc_id in range(0, 155)}


def infix_to_postfix(tokens):
    stack = []
    output = []

    for token in tokens:
        if token not in Operators:
            output.append(token)
        elif token == '(':
            stack.append('(')
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and Priority[token] <= Priority[stack[-1]]:
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())
    return output


def open_inverted_index(request_token):
    with open('inverted_index.txt', 'r', encoding='utf-8') as file:
        iterate_lines(file, request_token)


def get_result(request_token, split_read_line):
    global results
    if request_token == split_read_line[0]:
        split_read_line.pop(0)
        split_read_line = set(split_read_line)
        results.append(split_read_line)


def iterate_lines(file, request_token):
    read_line = file.readline()
    while read_line:
        split_read_line = read_line.split(' ')
        last_index = len(split_read_line) - 1
        split_read_line.pop(last_index)
        if request_token == split_read_line[0]:
            split_read_line.pop(0)
            split_read_line = set(split_read_line)
            results.append(split_read_line)
            return
        read_line = file.readline()

    results.append(set())


def processing_request(expression):
    def is_operator(character):
        return character in ['AND', 'OR', 'NOT', '(', ')']

    tokens = []
    current_token = ''
    for char in expression:
        if char == ' ':
            if current_token:
                tokens.append(current_token)
                current_token = ''
        elif is_operator(char):
            if current_token:
                tokens.append(current_token)
                current_token = ''
            tokens.append(char)
        else:
            current_token += char
    if current_token:
        tokens.append(current_token)

    tokens = infix_to_postfix(tokens)
    tokens.reverse()

    while len(tokens) > 0:
        token = tokens.pop()
        if token not in Operators:
            open_inverted_index(token)
        elif token == AND:
            result1 = results.pop()
            result2 = results.pop()
            results.append(result1.intersection(result2))
        elif token == OR:
            result1 = results.pop()
            result2 = results.pop()
            results.append(result1.union(result2))
        elif token == NOT:
            result1 = results.pop()
            results.append(all_doc_ids.difference(result1))

    return results.pop()


if __name__ == '__main__':
    results = []
    request = input()
    print("Результат:", sorted(processing_request(request)))
