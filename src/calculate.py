from src.tokenize import tokenize
from src.shunting_yard import shunting_yard
from src.rpn import solve_rpn


def calculate(expr: str) -> float:
    """
    Вычисляет математическое выражение
    :param expr: Выражение
    :return: Возвращает число, результат выполнения выражения
    """

    tokenized_expr = tokenize(expr=expr)
    rpn_expr = shunting_yard(tokenized_expr=tokenized_expr)
    result = solve_rpn(rpn_expr=rpn_expr)

    return result
