import string
from collections import defaultdict
import database
import time
import queue
import threading

from houses.Retabet import Retabet
from houses.Bwin import Bwin
from houses.WilliamHill import WilliamHill

from bet import Bet

bwin = Bwin(headless=True)

bwin.sport_bets("table_tennis")

bwin.end()