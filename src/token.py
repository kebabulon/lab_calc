from enum import Enum, auto


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

OPERATOR_PRIORITY: dict[TokenName, int] = {
    TokenName.ADD: 1,
    TokenName.SUBTRACT: 1,
    TokenName.MULTIPLY: 2,
    TokenName.DIVIDE: 2,
    TokenName.DIVIDE_AND_FLOOR: 2,
    TokenName.MOD: 2,
    TokenName.UNARY_MINUS: 3,
    TokenName.UNARY_PLUS: 3,
    TokenName.POW: 4,
}

RIGHT_TO_LEFT_OPERATORS: list[TokenName] = [
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

    def get_priority(self) -> int:
        """
        Приоритет токена (оператора)
        :return: Возвращает приоритет
        """
        return OPERATOR_PRIORITY.get(self.name, -1)

    def is_right_to_left(self) -> bool:
        """
        Проверяет если токен является право-ассициативным
        :return: Возвращает bool
        """
        return self.name in RIGHT_TO_LEFT_OPERATORS

    def __str__(self):
        if self.name == TokenName.NUMBER:
            return str(self.value)
        else:
            return TOKEN_NAME_TO_STR[self.name]

    def __repr__(self):
        return f"<{self.__str__()}>"
