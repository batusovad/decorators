from datetime import datetime as dt
from random import randint

from access_control import access_control
from constants import ADMIN_USERNAME, UNKNOWN_COMMAND


class GuessNumberGame:
    def __init__(self):
        # Атрибуты экземпляра (свойства игры)
        self.start_time = dt.now()
        self.total_games = 0
        self.username = ""

    def get_username(self) -> None:
        """Запрашивает имя пользователя при старте."""
        username = input("Представьтесь, пожалуйста, как Вас зовут?\n").strip()
        if username == ADMIN_USERNAME:
            print(
                "\nДобро пожаловать, создатель! "
                'Во время игры вам доступны команды "stat", "answer"'
            )
        else:
            print(f"\n{username}, добро пожаловать в игру!")
        self.username = username

    # Оставляем декоратор! Метод принимает только self.
    @access_control
    def get_statistics(self, **kwargs) -> None:
        """Выводит статистику. Доступно только админу."""
        game_time = dt.now() - self.start_time
        print(f"Общее время игры: {game_time}, текущая игра - №{self.total_games}")

    @access_control
    def get_right_answer(self, number: int, **kwargs) -> None:
        """Выводит правильный ответ. Доступно только админу."""
        print(f"Правильный ответ: {number}")

    def check_number(self, guess: int, number: int) -> bool:
        """Проверяет догадку пользователя."""
        if guess == number:
            print(f"Отличная интуиция, {self.username}! Вы угадали число :)")
            return True
        elif guess < number:
            print("Ваше число меньше того, что загадано.")
        else:
            print("Ваше число больше того, что загадано.")
        return False

    def play_round(self) -> None:
        """Проводит один раунд игры (одно загаданное число)."""
        self.total_games += 1
        number = randint(1, 100)
        print(
            "\nУгадайте число от 1 до 100.\n"
            'Для выхода из текущей игры введите команду "stop"'
        )

        while True:
            user_input = input("Введите число или команду: ").strip().lower()

            match user_input:
                case "stop":
                    break
                case "stat":
                    # Передаем имя пользователя в kwargs для декоратора
                    self.get_statistics(username=self.username)
                case "answer":
                    self.get_right_answer(number, username=self.username)
                case _:
                    try:
                        guess = int(user_input)
                    except ValueError:
                        print(UNKNOWN_COMMAND)
                        continue

                    if self.check_number(guess, number):
                        break

    def run(self) -> None:
        """Главный метод, который запускает игру."""
        print('Вас приветствует игра "Угадай число"!\n' "Для выхода нажмите Ctrl+C")
        self.get_username()

        while True:
            self.play_round()
            play_again = input("\nХотите сыграть ещё? (yes/no) ")
            if play_again.strip().lower() not in ("y", "yes"):
                break


# Точка входа в программу
if __name__ == "__main__":
    game = GuessNumberGame()
    game.run()
