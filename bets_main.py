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

def houses_exec(q, house):
    for sport in house.sports:
            house.sport_bets(sport)
            for match in house.ret_bets[sport]:
                if match.is_error():
                    continue
                q.put(match)
                
                
def retorno(ca, cb):
    return ca / (1 + (ca / cb))

reta = Retabet()
bwin = Bwin()
william_hill = WilliamHill()
house_list = [reta, bwin, william_hill]

while True:
    match_dict = defaultdict(lambda: [])
    
    threads = []
    q = queue.Queue()
    for house in house_list:
        t = threading.Thread(target=houses_exec, args=(q, house,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
    
    for match in q.queue:
        match_dict[match.hash()].append(match)
    
    retornos = []
    luck = False
    cnt = 0
    for key, match in match_dict.items():
        if len(match) <= 1:
            continue
        cnt += 1
        for m1 in match:
            for m2 in match:
                ret = retorno(m1.bets[0], m2.bets[1])
                retornos.append((ret, m1, m2))
                if ret >= 1:
                    print(ret)
                    print(m1, m2)
                    print(m1.link)
                    print(m2.link)
                    luck = True
    retornos.sort(key=lambda x: x[0], reverse=True)
    if len(retornos) and not luck:
        print(f"No luck: {retornos[0][0], cnt}")
    #time.sleep(5)
    exit()
#retornos.sort(key=lambda x: x[0], reverse=True)
#for r in retornos[:10]:
#    print(f"{r[0]}: {r[1], r[2]}")