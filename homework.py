class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Выводит на экран информацию о тренировке."""
        show_message = [
            f'Тип тренировки: {self.training_type};',
            f'Длительность: {self.duration:.3f} ч.;',
            f'Дистанция: {self.distance:.3f} км;',
            f'Ср. скорость: {self.speed:.3f} км/ч;',
            f'Потрачено ккал: {self.calories:.3f}.'
        ]
        return (' '.join(show_message))


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    M_IN_KM = 1000  # Коэффициент для перевода метров в километры.
    LEN_STEP = 0.65  # Длина шага в метрах.

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        # Пройденная дистанция в километрах.
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
        hided_message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        # Вызываем метод show_training_info() класса InfoMessage
        return hided_message


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Переводим полученные часы в минуты.
        duration_minutes = self.duration * 60
        coeff_calorie_1 = 18  # Коэффициент для расчета каллорий №1.
        coeff_calorie_2 = 20  # Коэффициент для расчета каллорий №2.
        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
                * self.weight / self.M_IN_KM * duration_minutes)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # Добавили параметр "рост" в сантиметрах.

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Переводим полученные часы в минуты.
        duration_minutes = self.duration * 60
        coeff_calorie_1 = 0.035  # Коэффициент для расчета каллорий №1.
        coeff_calorie_2 = 0.029  # Коэффициент для расчета каллорий №2.
        return ((coeff_calorie_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * coeff_calorie_2 * self.weight) * duration_minutes)


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        # Добавляем параметр "длина бассейна" в метрах.
        self.length_pool = length_pool
        # Добавили количество переплываний бассейна.
        self.count_pool = count_pool

    LEN_STEP = 1.38

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # Средняя скорость движения в километрах в час.
        return (((self.length_pool * self.count_pool) / self.M_IN_KM)
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 1.1  # Коэффициент для расчета каллорий №1.
        coeff_calorie_2 = 2  # Коэффициент для расчета каллорий №2.
        return ((self.get_mean_speed() + coeff_calorie_1)
                * coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    database = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    # Проверяем, к какому типу относится тренировка.
    if workout_type == 'RUN':
        return database['RUN'](*data)
    elif workout_type == 'WLK':
        return database['WLK'](*data)
    else:
        return database['SWM'](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
