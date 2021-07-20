import time

import threading

def f(num):
    print(num)
    print(sum([x for x in range(10000000)]))
    

if __name__ == '__main__':
    start = time.time()
    for i in range(5):
        f(50)
    end = time.time()
    print(end-start)
    
    
    start = time.time()
    threads = []
    for i in range(5):
        t = threading.Thread(target=f, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end = time.time()
    print(end-start)