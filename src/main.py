from src.calculate import calculate
from src.calculation_exceptions import CalculationException
from src.calculation_exceptions import ExpresionException


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    while expr := input("Введите выражение: "):
        try:
            result = calculate(expr=expr)
            print(result)

        except ExpresionException as e:
            print("Ошибка ввода:", str(e))
        except CalculationException as e:
            print("Ошибка выполнения:", str(e))


if __name__ == "__main__":
    main()
