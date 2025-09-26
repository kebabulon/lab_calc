import pytest

from src.calculation_exceptions import ExpresionException
from src.calculation_exceptions import CalculationException

from src.calculate import calculate


def test_number_tokenization():
    """
    Проверяет токенизирования числа
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
    Проверяет синтаксес выражения
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

    with pytest.raises(ExpresionException):
        calculate("(1)(1)")


def test_calculation():
    """
    Проверяет выполнение выражения
    """

    assert calculate("1") == 1
    assert calculate("1+1") == 2
    assert calculate("1+0.5") == 1.5
    assert calculate("-(9+2-1)*(8/(40//10))*(1%10)*((+2)**2)*1.5") == -120.0

    with pytest.raises(CalculationException):
        calculate("1/0")
    with pytest.raises(CalculationException):
        calculate("1//0")

    with pytest.raises(CalculationException):
        calculate("1.5//1")
    with pytest.raises(CalculationException):
        calculate("1//1.5")
    with pytest.raises(CalculationException):
        calculate("1.5//1.5")

    with pytest.raises(CalculationException):
        calculate("10.1%10")
    with pytest.raises(CalculationException):
        calculate("20%10.5")
    with pytest.raises(CalculationException):
        calculate("1.5%10.5")

    with pytest.raises(CalculationException):
        calculate("0**(-1)")
    with pytest.raises(CalculationException):
        calculate("(-1)**0.5")
