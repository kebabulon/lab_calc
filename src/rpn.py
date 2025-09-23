from src.calculation_exceptions import ExpresionException
from src.calculation_exceptions import CalculationException
from src.token import Token, TokenName


def solve_rpn(rpn_expr: list[Token]) -> int | float:
    """
    Вычисляет математическое выражение в обратной польской нотации (RPN)
    :param rpn_expr: Список токенов в обратной польской нотации
    :return: Возвращает результат выполнения вырожения
    """

    stack: list[int | float] = []

    for token in rpn_expr:
        if token.is_number():
            assert token.value is not None
            stack.append(token.value)

        elif token.is_operator():
            if token.get_arg_count() == 1:
                n = stack.pop()  # number

                match token.name:
                    case TokenName.UNARY_PLUS:
                        result = +n

                    case TokenName.UNARY_MINUS:
                        result = -n

                    case _:
                        raise ExpresionException(f"Неизвестная операция ('{token}')")

            elif token.get_arg_count() == 2:
                n2 = stack.pop()  # number 2
                n1 = stack.pop()  # number 1

                match token.name:
                    case TokenName.ADD:
                        result = n1 + n2

                    case TokenName.SUBTRACT:
                        result = n1 - n2

                    case TokenName.MULTIPLY:
                        result = n1 * n2

                    case TokenName.DIVIDE:
                        if n2 == 0:
                            raise CalculationException(f"Нельзя делить на ноль ({n1} / {n2})")
                        result = n1 / n2

                    case TokenName.DIVIDE_AND_FLOOR:
                        if n2 == 0:
                            raise CalculationException(f"Нельзя делить на ноль ({n1} // {n2})")
                        if (type(n1) is not int) or (type(n2) is not int):
                            raise CalculationException(f"Делить с окргулением можно только целые числа ({n1} // {n2})")
                        result = n1 // n2

                    case TokenName.MOD:
                        if n2 == 0:
                            raise CalculationException(f"Нельзя брать остаток числа от нуля ({n1} % {n2})")
                        if (type(n1) is not int) or (type(n2) is not int):
                            raise CalculationException(f"Брать остаток можно только с целыми числами ({n1} % {n2})")
                        result = n1 % n2

                    case TokenName.POW:
                        result = n1 ** n2

                    case _:
                        raise ExpresionException(f"Неизвестная операция ('{token}')")

            else:
                raise ExpresionException(f"Неизвестная операция ('{token}')")

            stack.append(result)

    final_result = stack.pop()
    if stack:
        raise ExpresionException("Ошибка синтаксиса математического вырожения")

    return final_result
