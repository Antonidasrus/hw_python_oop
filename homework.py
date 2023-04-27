from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return ('Тип тренировки: {}; '
                'Длительность: {:.3f} ч.; '
                'Дистанция: {:.3f} км; '
                'Ср. скорость: {:.3f} км/ч; '
                'Потрачено ккал: {:.3f}.').format(*asdict(self).values())

    def __str__(self) -> str:
        return self.get_message()


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65    # Длина шага при ходьбе/беге
    M_IN_KM: float = 1000     # Коэффициент для перевода [км] -> [м]
    CM_IN_M: float = 100      # Коэффициент для перевода [м] -> [см]
    MIN_IN_H: float = 60      # Коэффициент для перевода [час] -> [мин]

    def __init__(self, action: int, duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите метод get_spent_calories'
                                  f'в {self.__class__.__name__}')

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=type(self).__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    """Коэффициенты для формулы подсчета калорий при БЕГЕ"""
    RUN_speed_multiplier: float = 18    # Константа № 1 (для бега)
    RUN_speed_shift: float = 1.79       # Константа № 2 (для бега)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.RUN_speed_multiplier * self.get_mean_speed()
                + self.RUN_speed_shift) * self.weight
                * self.duration * self.MIN_IN_H
                / self.M_IN_KM)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    """Коэффициенты для формулы подсчета калорий при ХОДЬБЕ"""
    WLK_weight_multiplier: float = 0.035    # Константа № 1 (для ходьбы)
    WLK_speed_multiplier: float = 0.029     # Константа № 2 (для ходьбы)
    WLK_speed_converter: float = 0.278      # Для перевода [км/ч] -> [м/с]
    WLK_power: int = 2                      # Показатель возведения в степень
    CM_IN_M: int = 100                      # Для перевода [м] -> [см]

    def __init__(self, action: int, duration: float,
                 weight: int, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        duration_in_min = self.duration * self.MIN_IN_H    # Время в [мин]
        speed = self.get_mean_speed() * self.WLK_speed_converter
        self.height /= self.CM_IN_M    # Скорость в [м/с] и рост в [м]
        return ((self.WLK_weight_multiplier * self.weight
                + (speed**self.WLK_power / self.height)
                * self.WLK_speed_multiplier * self.weight) * duration_in_min)


class Swimming(Training):
    """Тренировка: плавание."""
    """Коэффициенты для формулы подсчета калорий при ПЛАВАНИИ"""
    SWM_speed_shift: float = 1.1        # Константа № 1 (для плавания)
    SWM_speed_multiplier: float = 2     # Константа № 2 (для плавания)
    LEN_STEP: float = 1.38              # Длина одного гребка при плавании

    def __init__(self, action: int, duration: float, weight: int,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SWM_speed_shift)
                * self.SWM_speed_multiplier * self.weight * self.duration)


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: dict[str, str] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in training_types:
        new_training = training_types[workout_type](*data)
    else:
        raise ValueError(f'Нет такой тренировки: {workout_type}')
    return new_training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
