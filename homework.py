from dataclasses import asdict, dataclass, fields


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self):
        """Выводит на экран информацию о тренировке."""
        return self.MESSAGE.format(**asdict(self))


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
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    HOURS_TO_MINUTES = 60
    MULTIPLYING_MEAN_SPEED = 18
    DECREASING_MEAN_SPEED = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_minutes = self.duration * self.HOURS_TO_MINUTES
        return (
            (
                self.MULTIPLYING_MEAN_SPEED * self.get_mean_speed()
                - self.DECREASING_MEAN_SPEED
            )
            * self.weight / self.M_IN_KM
            * duration_minutes
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float  # Добавили параметр "рост" в сантиметрах.

    HOURS_TO_MINUTES = 60
    MULTIPLYING_WEIGHT = 0.035
    MULTIPLYING_MEAN_SPEED = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Переводим полученные часы в минуты.
        duration_minutes = self.duration * self.HOURS_TO_MINUTES
        return (
            (
                self.MULTIPLYING_WEIGHT
                * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.MULTIPLYING_MEAN_SPEED
                * self.weight
            )
            * duration_minutes
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float  # Добавляем параметр "длина бассейна" в метрах.
    count_pool: int  # Добавили количество переплываний бассейна.

    LEN_STEP = 1.38  # Дистанция, проходимая плавцом за один гребок.
    INCREASING_MEAN_SPEED = 1.1
    MULTIPLYING_MEAN_SPEED = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return (((self.length_pool * self.count_pool) / self.M_IN_KM)
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.get_mean_speed() + self.INCREASING_MEAN_SPEED
            )
            * self.MULTIPLYING_MEAN_SPEED * self.weight
        )


TRAINING_TYPES = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming
}


ERROR_MESSAGE = 'Неожиданное значение параметра'


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAINING_TYPES:
        raise ValueError(f'{ERROR_MESSAGE} {workout_type}')
    training_types_values = TRAINING_TYPES[workout_type]
    if len(data) != len(fields(training_types_values)):
        raise ValueError(f'{ERROR_MESSAGE} для {workout_type}')
    return training_types_values(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
