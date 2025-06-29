import random
import time
from colorama import Fore, Style
from .cats import CATS, Mood
from .menu import MENU
from .art import draw_cat
from .save_system import SaveSystem

class CatCoffee:
    def __init__(self):
        self.menu = MENU
        self.cats = CATS
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
        self._last_money_update = time.time()
        self.save_system = SaveSystem()
        
        if self.save_system.load_game():
            self._load_game_data()
    
