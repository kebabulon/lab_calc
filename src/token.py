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


class TokenData():
    def __init__(self,
                 string: str,
                 operator: bool,
                 args: int = -1,
                 priority: int = -1,
                 right_to_left: bool = False,
                 ):
        self.string = string
        self.operator = operator
        self.args = args
        self.priority = priority
        self.right_to_left = right_to_left


TOKEN_DATA: dict[TokenName, TokenData] = {
    TokenName.ADD: TokenData(
        string='+',
        operator=True,
        args=2,
        priority=1,
    ),
    TokenName.SUBTRACT: TokenData(
        string='-',
        operator=True,
        args=2,
        priority=1,
    ),
    TokenName.MULTIPLY: TokenData(
        string='*',
        operator=True,
        args=2,
        priority=2,
    ),
    TokenName.DIVIDE: TokenData(
        string='/',
        operator=True,
        args=2,
        priority=2,
    ),
    TokenName.DIVIDE_AND_FLOOR: TokenData(
        string='//',
        operator=True,
        args=2,
        priority=2,
    ),
    TokenName.MOD: TokenData(
        string='%',
        operator=True,
        args=2,
        priority=2,
    ),
    TokenName.UNARY_PLUS: TokenData(
        string='+',
        operator=True,
        args=1,
        priority=3,
        right_to_left=True
    ),
    TokenName.UNARY_MINUS: TokenData(
        string='-',
        operator=True,
        args=1,
        priority=3,
        right_to_left=True
    ),
    TokenName.POW: TokenData(
        string='**',
        operator=True,
        args=2,
        priority=4,
        right_to_left=True
    ),

    TokenName.LEFT_BRACKET: TokenData(
        string='(',
        operator=False,
    ),
    TokenName.RIGHT_BRACKET: TokenData(
        string=')',
        operator=False,
    ),
    TokenName.NUMBER: TokenData(
        string='N',
        operator=False,
    ),

    TokenName.EMPTY: TokenData(
        string='',
        operator=False,
    ),
}

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


class Token():
    def __init__(self, name: TokenName, value: int | float | None = None):
        self.name = name
        self.value = value

        self.data: TokenData = TOKEN_DATA[name]

    # TODO: implement docstring
    def equals(self, token_name: TokenName) -> bool:
        return self.name == token_name

    def is_number(self) -> bool:
        """
        Проверяет если токен является числом
        :return: Возвращает bool
        """
        return self.equals(TokenName.NUMBER)

    def is_operator(self) -> bool:
        """
        Проверяет если токен является оператором
        :return: Возвращает bool
        """
        return self.data.operator

    def get_priority(self) -> int:
        """
        Приоритет токена (оператора)
        :return: Возвращает приоритет
        """
        return self.data.priority

    def is_right_to_left(self) -> bool:
        """
        Проверяет если токен является право-ассициативным
        :return: Возвращает bool
        """
        return self.data.right_to_left

    def __str__(self):
        if self.is_number():
            return str(self.value)
        else:
            return self.data.string

    def __repr__(self):
        return f"<{self.__str__()}>"
