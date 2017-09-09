import collections
from invInd import lemmatize

def process_query(query, index):
    query = query.replace('(', '( ')
    query = query.replace(')', ' )')
    query = query.split(' ')
    postfix_queue = collections.deque(lemmatize(shunting_yard(query)))
    tokens = []
    while postfix_queue:
        token = postfix_queue.popleft()
        if token != 'AND' and token != 'OR':
            tokens.append(list(index[token]))
        elif token == 'AND':
            second = tokens.pop()
            first = tokens.pop()
            res = list(set(first) & set(second))
            tokens.append(res)
        elif token == 'OR':
            right = tokens.pop()
            left = tokens.pop()
            in_first = set(right)
            in_second = set(left)
            in_second_but_not_in_first = in_second - in_first
            res = right + list(in_second_but_not_in_first)
            tokens.append(res)
    return tokens

def get_doc_by_name(name):
    if name == None:
        return name
    ints = list(name)
    year = ints[0] + ints[1]
    month = ints[2] + ints[3]
    path = "./Corpus/"
    if int(year) >= 90 and int(year) <= 94:
        path += "Part 1/"
        path += "awards_19" + year + "/"
        path += "awd_19" + year + "_" + month + "/"
        path += "a" + name + ".txt"
    elif int(year) >= 95 and int(year) <= 99:
        path += "Part 2/"
        path += "awards_19" + year + "/"
        path += "awd_19" + year + "_" + month + "/"
        path += "a" + name + ".txt"
    elif year == '00' or year == '01' or year == '02' or year == '03':
        path += "Part 3/"
        path += "awards_20" + year + "/"
        path += "awd_20" + year + "_" + month + "/"
        path += "a" + name + ".txt"

    try:
        return open(path)
    except FileNotFoundError:
        return None

def shunting_yard(infix_tokens):
    precedence = {}
    precedence['AND'] = 2
    precedence['OR'] = 1
    precedence['('] = 0
    precedence[')'] = 0

    output = []
    operator_stack = []

    for token in infix_tokens:
        if (token == '('):
            operator_stack.append(token)
        elif (token == ')'):
            operator = operator_stack.pop()
            while operator != '(':
                output.append(operator)
                operator = operator_stack.pop()
        elif (token in precedence):
            if (operator_stack):
                current_operator = operator_stack[-1]
                while (operator_stack and precedence[current_operator] > precedence[token]):
                    output.append(operator_stack.pop())
                    if (operator_stack):
                        current_operator = operator_stack[-1]
            operator_stack.append(token)
        else:
            output.append(token.lower())

    while (operator_stack):
        output.append(operator_stack.pop())
    return output