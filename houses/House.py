from bs4 import BeautifulSoup
from abc import ABC
from driver.selenium_driver import Driver
from bet.Bet import Bet
from database import *
import Levenshtein as lev
import time

class House(ABC):
    def __init__(self):
        self.driver = Driver(headless=True)
    def link_sport(self, sport):
        pass
    def sport_bets(self, sport):
        pass
    def real_names(self):
        pass
    def end(self):
        self.driver.close()
        self.driver.quit()