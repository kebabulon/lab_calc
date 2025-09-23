import pytest
from src.calculation_exceptions import ExpresionException

from src.calculate import calculate


def test_number_tokenization():
    with pytest.raises(ExpresionException):
        calculate("01")
    with pytest.raises(ExpresionException):
        calculate("001")
    with pytest.raises(ExpresionException):
        calculate(".")
    with pytest.raises(ExpresionException):
        calculate("1.0.0")
