import pytest
from src.calculation_exceptions import ExpresionException

from src.calculate import calculate


def test_number_tokenization():
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
