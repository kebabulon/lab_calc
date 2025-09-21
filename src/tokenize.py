from enum import Enum, auto
from src.calculation_exceptions import ExpresionException


class TokenName(Enum):
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    DIVIDE_AND_FLOOR = auto()
    MOD = auto()
    POW = auto()
    UNARY_PLUS = auto()
    UNARY_MINUS = auto()

    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()

    NUMBER = auto()

    EMPTY = auto()


OPERATORS: list[TokenName] = [
    TokenName.ADD,
    TokenName.SUBTRACT,
    TokenName.MULTIPLY,
    TokenName.DIVIDE,
    TokenName.DIVIDE_AND_FLOOR,
    TokenName.MOD,
    TokenName.POW,
    TokenName.UNARY_PLUS,
    TokenName.UNARY_MINUS,
]

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

TOKEN_NAME_TO_STR: dict[TokenName, str] = {
    TokenName.ADD: '+',
    TokenName.SUBTRACT: '-',
    TokenName.MULTIPLY: '*',
    TokenName.DIVIDE: '/',
    TokenName.DIVIDE_AND_FLOOR: '//',
    TokenName.MOD: '%',
    TokenName.POW: '**',
    TokenName.UNARY_PLUS: '+',
    TokenName.UNARY_MINUS: '-',

    TokenName.LEFT_BRACKET: '(',
    TokenName.RIGHT_BRACKET: ')',

    TokenName.EMPTY: '',
}


class Token():
    def __init__(self, name: TokenName, value: int | float | None = None):
        self.name = name
        self.value = value

    # TODO: implement docstring
    def equals(self, token_name: TokenName) -> bool:
        return self.name == token_name

    def is_number(self) -> bool:
        """
        Проверяет если токен является числом
        :return: Возвращает bool
        """
        return self.name == TokenName.NUMBER

    def is_operator(self) -> bool:
        """
        Проверяет если токен является оператором
        :return: Возвращает bool
        """
        return self.name in OPERATORS

    def __str__(self):
        if self.name == TokenName.NUMBER:
            return str(self.value)
        else:
            return TOKEN_NAME_TO_STR[self.name]

    def __repr__(self):
        return f"<{self.__str__()}>"


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

        # covert +|- to unary +|-
        if last_token.name in [TokenName.EMPTY, TokenName.LEFT_BRACKET]:
            if tokens[i].equals(TokenName.ADD):
                tokens[i].name = TokenName.UNARY_PLUS
            if tokens[i].equals(TokenName.SUBTRACT):
                tokens[i].name = TokenName.UNARY_MINUS

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

    print(tokenized_expr)

    return tokenized_expr
