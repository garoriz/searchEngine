AND = "AND"
IS_AND = False


def open_inverted_index(request_token):
    with open('inverted_index.txt', 'r', encoding='utf-8') as file:
        iterate_lines(file, request_token)


def validate_the_request(request_token):
    global IS_AND
    if len(token_stack) == 0 or token_stack[len(token_stack) - 1] == AND:
        token_stack.append(request_token)
        open_inverted_index(request_token)
    elif request_token == AND:
        IS_AND = True
        token_stack.append(request_token)
    elif token_stack[len(token_stack) - 1] != AND:
        print("Некорректный запрос!")
        exit()


def iterate_split_request(split_request):
    for request_token in split_request:
        validate_the_request(request_token)


def split_the_request():
    split_request = request.split()
    iterate_split_request(split_request)


def get_result(request_token, split_read_line):
    if request_token == split_read_line[0]:
        split_read_line.pop(0)
        if IS_AND:
            result.intersection_update(split_read_line)
        else:
            for elem in split_read_line:
                result.add(elem)


def iterate_lines(file, request_token):
    read_line = file.readline()
    while read_line:
        split_read_line = read_line.split(' ')
        last_index = len(split_read_line) - 1
        split_read_line.pop(last_index)
        get_result(request_token, split_read_line)
        read_line = file.readline()


if __name__ == '__main__':
    request = input()
    token_stack = []
    result = set()
    split_the_request()
    print(result)
