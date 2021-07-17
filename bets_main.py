import string
from collections import defaultdict
import database

from houses.Retabet import Retabet
from houses.Bwin import Bwin
from houses.WilliamHill import WilliamHill

from bet import Bet

def retorno(ca, cb):
    return ca / (1 + (ca / cb))

reta = Retabet()
bwin = Bwin()
william_hill = WilliamHill()
house_list = [reta, bwin, william_hill]

match_dict = defaultdict(lambda: [])
for house in house_list:
    house.sport_bets("tennis")
    for match in house.ret_bets:
        if match.is_error():
            continue
        match_dict[match.hash()].append(match)
    house.end()

retornos = []
for key, match in match_dict.items():
    if len(match) <= 1:
        continue
    for m1 in match:
        for m2 in match:
            ret = retorno(m1.bets[0], m2.bets[1])
            retornos.append((ret, m1, m2))
            if ret >= 1:
                print(ret)
                print(m1, m2)
retornos.sort(key=lambda x: x[0], reverse=True)
for r in retornos[:10]:
    print(f"{r[0]}: {r[1], r[2]}")