from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {key_to_insert[0]}; '
        'Длительность: {key_to_insert[1]:.3f} ч.; '
        'Дистанция: {key_to_insert[2]:.3f} км; '
        'Ср. скорость: {key_to_insert[3]:.3f} км/ч; '
        'Потрачено ккал: {key_to_insert[4]:.3f}.'
    )

    def get_message(self):
        """Выводит на экран информацию о тренировке."""
        message_data = (
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories
        )
        return self.MESSAGE.format(key_to_insert=message_data)


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    M_IN_KM = 1000  # Коэффициент для перевода метров в километры.
    LEN_STEP = 0.65  # Длина шага в метрах.

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # Средняя скорость движения в километрах в час.
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        # Создаём объект класса InfoMessage
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    # Коэффициент для перевода часов в минуты.
    HOURS_TO_MINUTES = 60
    # Коэффициент, учитавыемый для средней скорости
    # в функции для расчета каллорий.
    СOEFF_CALORIE_SPEED_1 = 18
    # Коэффициент, учитавыемый для вычитания из средней скорости
    # в функции для расчета каллорий.
    СOEFF_CALORIE_SPEED_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_minutes = self.duration * self.HOURS_TO_MINUTES
        return ((self.СOEFF_CALORIE_SPEED_1
                * self.get_mean_speed()
                - self.СOEFF_CALORIE_SPEED_2)
                * self.weight / self.M_IN_KM
                * duration_minutes)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float  # Добавили параметр "рост" в сантиметрах.

    # Коэффициент для перевода часов в минуты.
    HOURS_TO_MINUTES = 60
    # Коэффициент, учитавыемый для веса в первой части формулы
    # в функции для расчета каллорий.
    СOEFF_CALORIE_WEIGHT_1 = 0.035
    # Коэффициент, учитавыемый для веса во второй части формулы
    # в функции для расчета каллорий.
    СOEFF_CALORIE_WEIGHT_2 = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Переводим полученные часы в минуты.
        duration_minutes = self.duration * self.HOURS_TO_MINUTES
        return ((self.СOEFF_CALORIE_WEIGHT_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.СOEFF_CALORIE_WEIGHT_2 * self.weight)
                * duration_minutes)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float  # Добавляем параметр "длина бассейна" в метрах.
    count_pool: float  # Добавили количество переплываний бассейна.

    LEN_STEP = 1.38  # Дистанция, проходимая плавцом за один гребок.
    СOEFF_CALORIE_SPEED = 1.1  # Коэффициент, учитавыемый для средней скорости
    # в функции для расчета каллорий.
    СOEFF_CALORIE_WEIGHT = 2  # Коэффициент, учитавыемый для веса
    # в функции для расчета каллорий.

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # Средняя скорость движения в километрах в час.
        return (((self.length_pool * self.count_pool) / self.M_IN_KM)
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.СOEFF_CALORIE_SPEED)
                * self.СOEFF_CALORIE_WEIGHT * self.weight)


TRAINING_TYPE = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        return TRAINING_TYPE[workout_type](*data)
    except KeyError:
        raise KeyError('Недопустимый тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
