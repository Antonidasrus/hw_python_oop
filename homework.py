class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        msg = (f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.')
        return msg

    def __str__(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65    # Длина шага
    M_IN_KM = 1000     # Коэффициент для перевода километров в метры
    MIN_IN_H = 60      # Коэффициент для перевода часов в минуты
    CM_IN_M = 100      # Коэффициент для перевода метров в сантиметры
    training_type: str = None
    distance: float = 0
    mean_speed: float = 0
    spent_calories: float = 0

    def __init__(self, action: int, duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.get_distance()
        self.get_mean_speed()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed = self.distance / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        msg = InfoMessage(self.training_type, self.duration, self.distance,
                          self.mean_speed, self.spent_calories)
        return msg


class Running(Training):
    """Тренировка: бег."""
    RUN_K1 = 18
    RUN_K2 = 1.79

    def __init__(self, action: int, duration: float, weight: int) -> None:
        super().__init__(action, duration, weight)
        self.get_distance()
        self.get_spent_calories()
        self.training_type = 'Running'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        self.spent_calories = ((self.RUN_K1 * self.get_mean_speed()
                               + self.RUN_K2) * self.weight
                               * self.duration * self.MIN_IN_H
                               / self.M_IN_KM)
        return self.spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WLK_K1 = 0.035
    WLK_K2 = 0.029
    WLK_K3 = 0.278
    CM_IN_M = 100

    def __init__(self, action: int, duration: float,
                 weight: int, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.height /= self.CM_IN_M
        self.get_distance()
        self.get_spent_calories()
        self.training_type = 'SportsWalking'

    def get_spent_calories(self) -> float:
        duration_in_min = self.duration * self.MIN_IN_H
        speed = self.get_mean_speed() * self.WLK_K3
        self.spent_calories = ((self.WLK_K1 * self.weight
                               + (speed**2 / self.height)
                               * self.WLK_K2 * self.weight) * duration_in_min)
        return self.spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: int = 0
    count_pool: int = 0
    SWM_K1 = 1.1
    SWM_K2 = 2
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: int,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.get_distance()
        self.get_mean_speed()
        self.get_spent_calories()
        self.training_type = 'Swimming'

    def get_mean_speed(self) -> float:
        self.mean_speed = (self.length_pool * self.count_pool
                           / self.M_IN_KM / self.duration)
        return self.mean_speed

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.get_mean_speed() + self.SWM_K1)
                               * self.SWM_K2 * self.weight * self.duration)
        return self.spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in training_types.keys():
        new_training = training_types[workout_type](*data)
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
