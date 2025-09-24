import pytest
from src.calculation_exceptions import ExpresionException

from src.calculate import calculate


def test_number_tokenization():
    """
    Проверяет токенизирования числа
    :return: Данная функция ничего не возвращает
    """
    calculate("0")
    calculate("1234567890")
    calculate("1234.56789")
    calculate("1,5")
    calculate(".1")

    with pytest.raises(ExpresionException):
        calculate("01")
    with pytest.raises(ExpresionException):
        calculate("001")
    with pytest.raises(ExpresionException):
        calculate(".")
    with pytest.raises(ExpresionException):
        calculate("1.0.0")


def test_expresion_syntax():
    """
    Проверяет синтаксес вырожения
    :return: Данная функция ничего не возвращает
    """

    with pytest.raises(ExpresionException):
        calculate("Hello world!")

    with pytest.raises(ExpresionException):
        calculate("")
    with pytest.raises(ExpresionException):
        calculate("(")
    with pytest.raises(ExpresionException):
        calculate(")")
    with pytest.raises(ExpresionException):
        calculate("()")
    with pytest.raises(ExpresionException):
        calculate("*")
    with pytest.raises(ExpresionException):
        calculate("+")

    with pytest.raises(ExpresionException):
        calculate("1*")
    with pytest.raises(ExpresionException):
        calculate("*1")
    with pytest.raises(ExpresionException):
        calculate("++")
    with pytest.raises(ExpresionException):
        calculate("++")

    with pytest.raises(ExpresionException):
        calculate("1)")
    with pytest.raises(ExpresionException):
        calculate(")1")
    with pytest.raises(ExpresionException):
        calculate("1(")
    with pytest.raises(ExpresionException):
        calculate("(1")

    with pytest.raises(ExpresionException):
        calculate("(1+1")
    with pytest.raises(ExpresionException):
        calculate("1+1)")
    with pytest.raises(ExpresionException):
        calculate("(-1)+((1+(2*3))+(-1)")
    with pytest.raises(ExpresionException):
        calculate("(-1)+(1+(2*3)))+(-1)")
