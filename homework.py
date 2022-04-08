from typing import Dict, List, Type
from dataclasses import dataclass, asdict #Взято со слак, не особо понятно
@dataclass #Взято со слак, не особо понятно

class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, 
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    
    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message.format(**asdict(self)) #Взято со слак, не особо понятно


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000 #ввел константу
    LEN_STEP: float = 0.65 #временно тут константа переменная
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )        


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20 
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return  ((self.COEFF_CALORIE_1
                * self.get_mean_speed()
                - self.COEFF_CALORIE_2)
                * self.weight 
                / self.M_IN_KM 
                * (self.duration*60)) 


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029
        
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration,weight)
        self.height = height
    
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEFF_CALORIE_1 
                * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CALORIE_2
                * self.weight)
                * (self.duration*60))


class Swimming(Training):
    """Тренировка: плавание."""
    
    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration,weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool 
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2
                * self.weight)

def read_package(workout_type: str, data: List) -> Training:
    """Прочитать данные полученные от датчиков."""
    TICKER: Dict[str, Type[Training]] = {
       'SWM': Swimming,
       'RUN': Running,
       'WLK': SportsWalking,
    }
    if workout_type in TICKER: 
        result = TICKER[workout_type](*data)
        return result 

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    result = info.get_message()
    print(result)
   
if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)