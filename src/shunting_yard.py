from src.calculation_exceptions import ExpresionException
from src.token import Token, TokenName


# TODO: implement
def shunting_yard(tokenized_expr: list[Token]) -> list[Token]:
    """
    Имплементация шунтирующего дворa со скобками
    :param tokenized_expr: Список токенов в инфиксной нотации
    :return: Возвращает список токенов в обратной польской нотации (RPN)
    """

    result: list[Token] = []
    operator_stack: list[Token] = []

    for token in tokenized_expr:
        if token.is_number():
            result.append(token)

        elif token.is_operator():
            token_priority = token.get_priority()
            token_right_to_left = token.is_right_to_left()
            while (
                operator_stack and
                operator_stack[-1].is_operator() and
                (
                    token_right_to_left and operator_stack[-1].get_priority() > token_priority
                    or not token_right_to_left and operator_stack[-1].get_priority() >= token_priority
                )
            ):
                result.append(operator_stack.pop())

            operator_stack.append(token)

        elif token.equals(TokenName.LEFT_BRACKET):
            operator_stack.append(token)

        elif token.equals(TokenName.RIGHT_BRACKET):
            while operator_stack and not operator_stack[-1].equals(TokenName.LEFT_BRACKET):
                result.append(operator_stack.pop())
            if operator_stack:
                operator_stack.pop()
            else:
                raise ExpresionException("Существует скобка без пары")

    while operator_stack:
        popped_operator = operator_stack.pop()
        if popped_operator.equals(TokenName.LEFT_BRACKET):
            raise ExpresionException("Существует скобка без пары")
        result.append(popped_operator)

    print(result)

    return result
