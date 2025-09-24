from src.calculation_exceptions import ExpresionException
from src.token import Token, TokenName
from src.constants import DEBUG_PRINT


STR_TO_TOKEN_NAME: dict[str, TokenName] = {
    '+': TokenName.ADD,
    '-': TokenName.SUBTRACT,
    '*': TokenName.MULTIPLY,
    '/': TokenName.DIVIDE,
    '//': TokenName.DIVIDE_AND_FLOOR,
    '%': TokenName.MOD,
    '**': TokenName.POW,

    '(': TokenName.LEFT_BRACKET,
    ')': TokenName.RIGHT_BRACKET,
}


def string_to_tokens(expr: str) -> list[Token]:
    """
    Токенизирует математическое выражение
    :param expr: Выражение
    :return: Возвращает необработаный список токенов
    """

    expr = expr.replace(' ', '')
    expr = expr.replace(',', '.')
    expr += " "  # 1 char buffer for checking ahead

    tokenized_expr: list[Token] = []
    index = 0

    while index < len(expr) - 1:
        # numbers
        if expr[index].isdigit() or expr[index] == '.':
            number_str = expr[index]

            while expr[index + 1].isdigit() or expr[index + 1] == '.':
                index += 1
                number_str += expr[index]

            if number_str == '.':
                raise ExpresionException("'.' не является числом")
            if number_str[:2] == '00':
                raise ExpresionException(f"Присуствуют ведущие нули ({number_str})")
            if len(number_str) >= 2 and number_str[0] == '0' and number_str[1].isdigit():
                raise ExpresionException(f"Присуствует ведущий ноль ({number_str})")

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
            tokenized_expr.append(Token(name=TokenName.NUMBER, value=number))
            index += 1

        # operators
        elif expr[index:index + 2] in STR_TO_TOKEN_NAME:
            tokenized_expr.append(Token(name=STR_TO_TOKEN_NAME[expr[index:index + 2]]))
            index += 2

        elif expr[index] in STR_TO_TOKEN_NAME:
            tokenized_expr.append(Token(name=STR_TO_TOKEN_NAME[expr[index]]))
            index += 1

        else:
            raise ExpresionException(f"Неизвестный символ ('{expr[index]}')")

    return tokenized_expr


def tokens_preprocessing(tokens: list[Token]) -> list[Token]:
    """
    Проверка и окончательное изменение токенов
    :param tokens: Необработаный список токенов
    :return: Возвращает обработаный список токенов
    """

    last_token: Token = Token(name=TokenName.EMPTY)

    for i in range(len(tokens)):
        # covert +|- to unary +|-
        if last_token.name in [TokenName.EMPTY, TokenName.LEFT_BRACKET]:
            if tokens[i].equals(TokenName.ADD):
                tokens[i] = Token(name=TokenName.UNARY_PLUS)
            if tokens[i].equals(TokenName.SUBTRACT):
                tokens[i] = Token(name=TokenName.UNARY_MINUS)

        # operator exceptions
        if last_token.is_operator() and tokens[i].is_operator():
            raise ExpresionException(f"Два оператора идущих подрят ('{last_token}' '{tokens[i]}')")

        if last_token.equals(TokenName.RIGHT_BRACKET) and tokens[i].equals(TokenName.LEFT_BRACKET):
            raise ExpresionException("Нету оператора между скобок")

        if (
                last_token.equals(TokenName.RIGHT_BRACKET) and tokens[i].is_number()
                or last_token.is_number() and tokens[i].equals(TokenName.LEFT_BRACKET)
        ):
            raise ExpresionException(f"Нету оператора между скобкой и числом ('{last_token}' '{tokens[i]}')")

        if last_token.is_number() and tokens[i].is_number():
            raise ExpresionException(f"Нету оператора между числами ('{last_token}' '{tokens[i]}')")

        if (
                last_token.equals(TokenName.LEFT_BRACKET) and tokens[i].is_operator()
                and tokens[i].name not in [TokenName.UNARY_MINUS, TokenName.UNARY_PLUS]

                or last_token.is_operator() and tokens[i].equals(TokenName.RIGHT_BRACKET)
        ):
            raise ExpresionException(f"Нету числа между скобкой и оператором ('{last_token}' '{tokens[i]}')")

        if last_token.equals(TokenName.LEFT_BRACKET) and tokens[i].equals(TokenName.RIGHT_BRACKET):
            raise ExpresionException("Пустая скобка")

        last_token = tokens[i]

    if tokens[0].is_operator() and tokens[0].name not in [TokenName.UNARY_MINUS, TokenName.UNARY_PLUS]:
        raise ExpresionException(f"Оператор не может быть первым токеном ('{tokens[0]}')")

    if tokens[-1].is_operator():
        raise ExpresionException(f"Оператор не может быть последним токеном ('{tokens[-1]}')")

    return tokens


def tokenize(expr: str) -> list[Token]:
    """
    Токенизирует математическое выражение
    :param expr: Выражение
    :return: Возвращает список токенов
    """

    raw_tokenized_expr = string_to_tokens(expr=expr)
    tokenized_expr = tokens_preprocessing(tokens=raw_tokenized_expr)

    if DEBUG_PRINT:
        print(tokenized_expr)

    return tokenized_expr
