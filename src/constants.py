OPERATORS: list[str] = ['+', '-', '*', '/', '//', '%', '**', 'u+', 'u-']
OPERATOR_PRIORITY: dict[str, int] = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '//': 2,
    '%': 2,
    'u+': 3,
    'u-': 3,
    '**': 4,
}
RIGHT_TO_LEFT_OPERATORS: dict[str, bool] = {
    '**': True,
    'u+': True,
    'u-': True,
}
