from src.calculation_exceptions import ExpresionException
from src.constants import OPERATORS


def is_number(tok: str | int | float) -> bool:
    """
    Проверяет если токен является числом
    :param expr: Токен
    :return: Возвращает bool
    """
    return (tok is int) or (tok is float)


def is_operator(tok: str | int | float) -> bool:
    """
    Проверяет если токен является оператором
    :param expr: Токен
    :return: Возвращает bool
    """
    return tok in OPERATORS


def string_to_tokens(expr: str) -> list[str | int | float]:
    """
    Токенизирует математическое выражение
    :param expr: Выражение
    :return: Возвращает необработаный список токенов
    """

    expr = expr.replace(' ', '')
    expr = expr.replace(',', '.')
    expr += " "  # 1 char buffer for checking ahead

    tokenized_expr: list[str | int | float] = []
    index = 0

    while index < len(expr)-1:
        # numbers
        if expr[index].isdigit() or expr[index] == '.':
            number_str = expr[index]

            while expr[index+1].isdigit() or expr[index+1] == '.':
                index += 1
                number_str += expr[index]

            if number_str == '.':
                raise ExpresionException("'.' не является числом")
            if number_str[:2] == '00':
                raise ExpresionException(f"Присуствуют ведущие нули ({number_str})")

            floating_point = False

            for i in number_str:
                if i == '.':
                    if floating_point:
                        raise ExpresionException(f"Присуствует несколько запятых в числе ({number_str})")
                    floating_point = True

            if floating_point:
                number = float(number_str)
            else:
                number = int(number_str)
            tokenized_expr.append(number)
            index += 1

        # operators
        elif is_operator(expr[index:index+2]):
            tokenized_expr.append(expr[index:index+2])
            index += 2

        elif is_operator(expr[index]) or expr[index] in ['(', ')']:
            tokenized_expr.append(expr[index])
            index += 1

        else:
            raise ExpresionException(f"Неизвестный символ ({expr[index]})")

    return tokenized_expr


def tokens_preprocessing(tokens: list[str | int | float]) -> list[str | int | float]:
    """
    Проверка и окончательное изменение токенов
    :param tokens: Необработаный список токенов
    :return: Возвращает обработаный список токенов
    """

    last_token: str | int | float = ''

    for i in range(len(tokens)):
        # operator exceptions
        if is_operator(last_token) and is_operator(tokens[i]):
            raise ExpresionException(f"Два оператора идущих подрят ({last_token} {tokens[i]})")

        if last_token == ')' and tokens[i] == '(':
            raise ExpresionException("Нету оператора между скобок")

        if (
                last_token == ')' and is_number(tokens[i]) or
                is_number(last_token) and tokens[i] == '('
        ):
            raise ExpresionException(f"Нету оператора между скобкой и числом ({last_token} {tokens[i]})")

        if is_number(last_token) and is_number(tokens[i]):
            raise ExpresionException(f"Нету оператора между числами ({last_token} {tokens[i]})")

        # covert +|- to unary +|-
        if last_token in ['', '('] and tokens[i] in ['+', '-']:
            tokens[i] = f'u{tokens[i]}'

        last_token = tokens[i]

    if is_operator(tokens[0]) and tokens[0] not in ['u+', 'u-']:
        raise ExpresionException(f"Оператор не может быть первым токеном ({tokens[0]})")

    if is_operator(tokens[-1]):
        raise ExpresionException(f"Оператор не может быть последним токеном ({tokens[-1]})")

    return tokens


def tokenize(expr: str) -> list[str | int | float]:
    """
    Токенизирует математическое выражение
    :param expr: Выражение
    :return: Возвращает список токенов
    """

    raw_tokenized_expr = string_to_tokens(expr=expr)
    tokenized_expr = tokens_preprocessing(tokens=raw_tokenized_expr)

    return tokenized_expr
