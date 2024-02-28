AND = "AND"
IS_AND = False
OR = "OR"
IS_OR = False
NOT = 'NOT'

Operators = {'AND', 'OR', 'NOT', '(', ')'}

Priority = {'OR': 1, 'AND': 2, 'NOT': 3}

all_doc_ids = {doc_id for doc_id in range(0, 155)}


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


def validate_the_request(request_token):
    global IS_AND, IS_OR
    if len(token_stack) == 0 or token_stack[len(token_stack) - 1] == AND or token_stack[len(token_stack) - 1] == "OR":
        token_stack.append(request_token)
        open_inverted_index(request_token)
    elif request_token == AND:
        IS_AND = True
        token_stack.append(request_token)
    elif request_token == OR:
        IS_OR = True
        token_stack.append(request_token)
    elif token_stack[len(token_stack) - 1] != AND:
        print("Некорректный запрос!")
        exit()


def split_the_request_by_or(request_token):
    split_request = request_token.split(" OR ")
    for request_token in split_request:
        open_inverted_index(request_token)


def iterate_split_request(split_request):
    for request_token in split_request:
        # validate_the_request(request_token)
        split_the_request_by_or(request_token)


def split_the_request_by_and():
    split_request = request.split(" AND ")
    for request_token in split_request:
        # validate_the_request(request_token)
        split_the_request_by_or(request_token)


def get_result(request_token, split_read_line):
    global results
    if request_token == split_read_line[0]:
        split_read_line.pop(0)
        split_read_line = set(split_read_line)
        results.append(split_read_line)
        #if len(result) == 0:
        #    for elem in split_read_line:
        #        result.add(elem)
        #else:
        #    result = result.union(split_read_line)
    # global IS_AND
    # if request_token == split_read_line[0]:
    #    split_read_line.pop(0)
    #    if IS_AND:
    #        result.intersection_update(split_read_line)
    #        IS_AND = False
    #    if IS_OR:
    #        result.intersection_update(split_read_line)
    #        IS_AND = False
    #    else:
    #        for elem in split_read_line:
    #            result.add(elem)


def iterate_lines(file, request_token):
    read_line = file.readline()
    while read_line:
        split_read_line = read_line.split(' ')
        last_index = len(split_read_line) - 1
        split_read_line.pop(last_index)
        get_result(request_token, split_read_line)
        read_line = file.readline()


def evaluate_expression(expression):
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
    # request = input()
    # token_stack = []
    results = []
    # split_the_request_by_and()
    # print(result)
    expression = "орор"
    print("Результат выражения:", evaluate_expression(expression))
