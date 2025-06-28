import random
import time
from colorama import Fore, Style
from .cats import CATS, Mood
from .menu import MENU
from .art import CAT_ART

class CatCafe:
    def __init__(self):
        self.menu = MENU
        self.cats = CATS
        self.stats = {
            "served": 0,
            "income": 0,
            "run_aways": 0,
            "vip_clients": 0
        }
        self.day = 1

    def start(self):
        print(Fore.BLUE + Style.BRIGHT + "Добро пожаловать в CatCafe!")
        while True:
            print(f"\nДень {self.day}")
            print("1. Принять заказ  2. Статистика  3. Выйти")
            choice = input("> ")

            if choice == "1":
                self.serve_cat()
            elif choice == "2":
                self.show_stats()
            elif choice == "3":
                print("До встречи! 😺")
                break

    def serve_cat(self):
        cat_name, cat_data = random.choice(list(self.cats.items()))
        print(CAT_ART[cat_data["rarity"]])
        print(f"К вам пришел {cat_name} ({cat_data['rarity']})")
        # ... (остальная логика сервиса)