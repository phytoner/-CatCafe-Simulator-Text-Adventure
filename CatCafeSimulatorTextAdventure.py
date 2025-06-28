import random
import time
import sys
from colorama import Fore, init, Style
from enum import Enum
from collections import defaultdict

init(autoreset=True)

class Mood(Enum):
    PLAYFUL = "игривый"
    LAZY = "ленивый"
    MOODY = "капризный"
    HUNGRY = "голодный"
    ARISTOCRAT = "аристократичный"

class CatCoffee:
    def __init__(self):
        self.menu = {
            1: {"name": "Латте с кошачьей мятой", "price": 150, "prep_time": 2, "energy": 1},
            2: {"name": "Капучино с рыбной крошкой", "price": 180, "prep_time": 3, "energy": 2},
            3: {"name": "Молочко с меланхолией", "price": 90, "prep_time": 1, "energy": 0},
            4: {"name": "Эспрессо для хвостатых", "price": 120, "prep_time": 2, "energy": 1},
            5: {"name": "VIP-коктейль 'Золотая рыбка'", "price": 300, "prep_time": 5, "energy": 3}
        }
        
        self.cat_names = {
            "Барсик": {"rarity": "common", "fav_drink": 1},
            "Мурзик": {"rarity": "common", "fav_drink": 2},
            "Васька": {"rarity": "common", "fav_drink": 3},
            "Рыжик": {"rarity": "rare", "fav_drink": 4},
            "Снежок": {"rarity": "rare", "fav_drink": 1},
            "Пушок": {"rarity": "rare", "fav_drink": 2},
            "Компот": {"rarity": "legendary", "fav_drink": 5},
            "Гарфилд": {"rarity": "legendary", "fav_drink": 5}
        }
        
        self.stats = {
            "served": 0,
            "income": 0,
            "run_aways": 0,
            "vip_clients": 0,
            "broken_cups": 0
        }
        
        self.player = {
            "reputation": 0,
            "tips": 0,
            "mood_boost": False
        }
        
        self.day_counter = 1
        self.payment_fail_chance = 0.25
        self.game_active = True
        
    def show_header(self):
        print(Fore.BLUE + Style.BRIGHT + f"\n=== День {self.day_counter} в Кошачьей Кофейне ===")
        print(Fore.YELLOW + f"💰 Касса: {self.stats['income']}₽ | 🐾 Репутация: {self.player['reputation']}/100")
        print(Fore.CYAN + f"👑 VIP-клиентов: {self.stats['vip_clients']} | 🏃 Убежали: {self.stats['run_aways']}")
    
    def show_menu(self):
        print(Fore.YELLOW + "\n🐾 Меню кошачьей кофейни:")
        for key, item in self.menu.items():
            energy_icons = "⚡" * item["energy"]
            print(f"{Fore.GREEN}{key}. {item['name']} - {item['price']}₽ {energy_icons}")
    
    def get_cat_with_rarity(self):
        cats_by_rarity = {
            "common": [name for name, data in self.cat_names.items() if data["rarity"] == "common"],
            "rare": [name for name, data in self.cat_names.items() if data["rarity"] == "rare"],
            "legendary": [name for name, data in self.cat_names.items() if data["rarity"] == "legendary"]
        }
        
        # Шансы: common 70%, rare 25%, legendary 5%
        rarity = random.choices(
            ["common", "rare", "legendary"],
            weights=[70, 25, 5],
            k=1
        )[0]
        
        return random.choice(cats_by_rarity[rarity])
    
    def draw_cat(self, name):
        cats_art = {
            "common": r"""
 /\_/\  
( o.o ) 
 > ^ <
            """,
            "rare": r"""
  /\_/\  
 ( ^.^ ) 
 /  \  \
            """,
            "legendary": r"""
  /\_/\  
 ( ◕ᴗ◕ ) 
 /[] []\
            """
        }
        
        rarity = self.cat_names[name]["rarity"]
        print(Fore.CYAN + cats_art[rarity])
        print(Fore.MAGENTA + Style.BRIGHT + f"К вам пришел {rarity} кот {name}!")
    
    def calculate_tip(self, cat_name, drink_id, mood):
        base_tip = random.randint(10, 50)
        
        # Бонусы
        bonus = 0
        if self.cat_names[cat_name]["fav_drink"] == drink_id:
            bonus += 30
            print(Fore.GREEN + f"{cat_name} обожает этот напиток!")
        
        if mood == Mood.ARISTOCRAT.value:
            bonus += 40
        
        if self.player["mood_boost"]:
            bonus += 20
        
        return base_tip + bonus
    
    def take_order(self):
        cat_name = self.get_cat_with_rarity()
        mood = random.choice([m.value for m in Mood])
        
        self.draw_cat(cat_name)
        print(Fore.CYAN + f"Настроение: {mood}")
        
        self.show_menu()
        try:
            choice = int(input("Выбери напиток (1-5): "))
            if choice not in self.menu:
                raise ValueError
        except ValueError:
            print(Fore.RED + "Неверный выбор! Кот раздраженно махнул хвостом.")
            self.player["reputation"] = max(0, self.player["reputation"] - 5)
            return
        
        item = self.menu[choice]
        
        # Особое поведение для аристократичных котов
        if mood == Mood.ARISTOCRAT.value and choice != 5:
            print(Fore.RED + f"{cat_name} презрительно фыркает на такой простой напиток!")
            self.player["reputation"] = max(0, self.player["reputation"] - 10)
            return
        
        print(Fore.GREEN + f"\nГотовим {item['name']} для {cat_name}...")
        self.animate_preparation(item['prep_time'])
        
        # Реакция кота
        reactions = [
            f"{cat_name} мурлычет от удовольствия!",
            f"{cat_name} недовольно фыркает...",
            f"{cat_name} разлил напиток! Придется убирать.",
            f"{cat_name} заснул прямо в чашке. zZz...",
            f"{cat_name} игриво переворачивает чашку лапой!"
        ]
        
        reaction = random.choice(reactions)
        if "разлил" in reaction:
            self.stats["broken_cups"] += 1
        
        print(Fore.MAGENTA + reaction)
        
        # Оплата и чаевые
        if random.random() < self.payment_fail_chance:
            print(Fore.RED + f"{cat_name} убежал, не заплатив! 😾")
            self.stats["run_aways"] += 1
            self.player["reputation"] = max(0, self.player["reputation"] - 5)
        else:
            print(Fore.GREEN + f"+{item['price']}₽ в кассу!")
            self.stats["income"] += item['price']
            
            # Чаевые
            tip = self.calculate_tip(cat_name, choice, mood)
            print(Fore.YELLOW + f"🍪 {cat_name} оставил {tip}₽ чаевых!")
            self.player["tips"] += tip
            self.stats["income"] += tip
            
            # Репутация
            rep_gain = random.randint(1, 3)
            if self.cat_names[cat_name]["rarity"] == "legendary":
                rep_gain *= 2
                self.stats["vip_clients"] += 1
            self.player["reputation"] = min(100, self.player["reputation"] + rep_gain)
        
        self.stats["served"] += 1
        
        # Случайное событие
        self.random_event(cat_name)
    
    def animate_preparation(self, seconds):
        for i in range(seconds):
            print(Fore.YELLOW + "Приготовление" + "." * (i % 4), end="\r")
            time.sleep(1)
        print(" " * 20, end="\r")
    
    def random_event(self, cat_name):
        if random.random() < 0.15:
            events = [
                (f"{cat_name} привел своего друга! Завтра будет больше клиентов.", "positive"),
                ("Вы нашли монетку под столом! +20₽", "income"),
                ("Кто-то оставил восторженный отзыв в соцсетях! +10 к репутации", "reputation"),
                ("О нет! Один из котов поцарапал мебель. -15₽ на ремонт", "negative"),
                ("Вы чувствуете, что завтра коты будут в лучшем настроении!", "mood_boost")
            ]
            
            event, effect = random.choice(events)
            print(Fore.BLUE + "\n⚡ Случайное событие: " + event)
            
            if effect == "positive":
                self.player["reputation"] = min(100, self.player["reputation"] + 10)
            elif effect == "income":
                self.stats["income"] += 20
            elif effect == "reputation":
                self.player["reputation"] = min(100, self.player["reputation"] + 10)
            elif effect == "negative":
                self.stats["income"] = max(0, self.stats["income"] - 15)
            elif effect == "mood_boost":
                self.player["mood_boost"] = True
    
    def end_day(self):
        print(Fore.BLUE + "\n=== Конец дня ===")
        print(Fore.YELLOW + f"Всего обслужено котов: {self.stats['served']}")
        print(Fore.CYAN + f"Чаевые: {self.player['tips']}₽")
        
        # Бонус за репутацию
        if self.player["reputation"] >= 80:
            bonus = 100
            print(Fore.GREEN + f"Отличная репутация! Бонус +{bonus}₽")
            self.stats["income"] += bonus
        
        print(Fore.MAGENTA + f"Итоговый доход: {self.stats['income']}₽")
        
        # Сброс дневной статистики
        self.player["tips"] = 0
        self.day_counter += 1
        self.player["mood_boost"] = False
        
        # Увеличение сложности
        if self.day_counter % 3 == 0:
            self.payment_fail_chance = max(0.1, self.payment_fail_chance - 0.05)
            print(Fore.GREEN + "\nВаша кофейня становится популярнее! Коты реже убегают без оплаты.")
    
    def show_stats(self):
        print(Fore.BLUE + "\n📊 Статистика кофейни:")
        print(f"Дней работы: {self.day_counter - 1}")
        print(f"Всего клиентов: {self.stats['served']}")
        print(f"VIP-клиентов: {self.stats['vip_clients']}")
        print(f"Убежали без оплаты: {self.stats['run_aways']}")
        print(f"Разбито чашек: {self.stats['broken_cups']}")
        print(f"Общий доход: {self.stats['income']}₽")
    
    def start(self):
        print(Fore.BLUE + Style.BRIGHT + "Добро пожаловать в Кошачью Кофейню!")
        print(Fore.MAGENTA + "Ваша цель - заработать 2000₽ и получить 5 звезд репутации!\n")
        
        while self.game_active:
            self.show_header()
            
            print("\n1. Принять заказ")
            print("2. Закончить день")
            print("3. Посмотреть статистику")
            print("4. Выйти")
            
            try:
                choice = int(input("Выбери действие: "))
            except ValueError:
                print("Неверный ввод!")
                continue
            
            if choice == 1:
                self.take_order()
                
                # Проверка победы
                if self.stats["income"] >= 2000 and self.player["reputation"] >= 80:
                    print(Fore.GREEN + Style.BRIGHT + "\n🎉 Поздравляем! Вы достигли цели!")
                    print("Ваша кофейня стала самой популярной среди котов!")
                    self.show_stats()
                    self.game_active = False
            elif choice == 2:
                self.end_day()
            elif choice == 3:
                self.show_stats()
            elif choice == 4:
                print("Кофейня закрывается. До новых встреч! 😺")
                self.game_active = False
            else:
                print("Неверный выбор!")

if __name__ == "__main__":
    cafe = CatCoffee()
    cafe.start()