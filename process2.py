import os
from multiprocessing import Process, Manager, Queue, Value
from queue import Empty
import time
from collections import deque
from itertools import islice
import numpy as np

def split_deque(d: deque):
    half = len(d) // 2
    stolen = deque(islice(d, 0, half))
    # Effacer les éléments volés
    for _ in range(half):
        d.popleft()
    return stolen

def control(mainQueue, secondaryQueue, queues, sizes, nb_workers):
    workersAlive = nb_workers-1
    while workersAlive >= 0:
        msg, content = mainQueue.get()

        if msg == "help":
            snapshot = [sizes[i].value for i in range(nb_workers)]
            snapshot[content] = -1
            ma = max(snapshot)

            if ma == 0:
                queues[content].put(("empty", []))
            else:
                m = snapshot.index(ma)
                queues[m].put(("donate", m))

                stack = secondaryQueue.get()
                if len(stack) == 0 or type(stack) == tuple:
                    queues[content].put(("empty", []))
                else:
                    queues[content].put(("give", stack))
    
        elif msg == "dead":
            # print("dead", content)
            workersAlive -= 1


def worker(i, path_root, search, stack, queue, mainQueue, secondaryQueue, sizes, found):
    """Worker avec pile locale + work-stealing."""

    helpAsked = False

    while True:
        if len(stack) == 0 and not helpAsked:
            mainQueue.put(("help", i))
            helpAsked = True
        elif len(stack) != 0:
            rel_path = stack.pop()
            full_path = os.path.join(path_root, rel_path)

            if os.path.basename(full_path).lower() == search:
                found.append(full_path)
            elif not os.path.isfile(full_path):
                try:
                    children = os.listdir(full_path)
                    stack.extend(map(lambda x:os.path.join(rel_path, x), children))
                except PermissionError:
                    continue
            
            sizes[i].value = len(stack)

        try:
            msg, q = queue.get_nowait()

            if msg == "donate":
                half = len(stack) // 2
                if half != 0:
                    secondaryQueue.put(split_deque(stack))
                else:
                    secondaryQueue.put([])
            elif msg == "give":
                stack = q
                helpAsked = False
                if len(stack) == 0:
                    break
            elif msg == "empty":
                break
            
        except Empty:
            continue

    mainQueue.put(("dead", i))
        

def parallel_search(path, search, nb_workers=3):
    manager = Manager()

    # liste de piles partagée → chaque pile est une Manager.list()
    stacks = [deque() for _ in range(nb_workers)]
    found = manager.list()
    queues = [Queue() for _ in range(nb_workers)]
    mainQueue = Queue()
    secondaryQueue = Queue()
    

    # distribution initiale du travail comme ton initStack()
    start = os.listdir(path)
    for j, el in enumerate(start):
        stacks[j % nb_workers].append(el)

    processes = []
    sizes = [Value('i', len(stacks[i])) for i in range(nb_workers)]

    c = Process(target=control, args=(mainQueue, secondaryQueue, queues, sizes, nb_workers))
    c.start()
    
    for i in range(nb_workers):
        p = Process(target=worker, args=(i, path, search, stacks[i], queues[i], mainQueue, secondaryQueue, sizes, found))
        # worker(i, path, search, stacks[i], queues, found)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    
    c.join()

    return list(found)


# ===============================
# Exemple d'utilisation
# ===============================
if __name__ == "__main__":
    path = "C:/Users/lucas/Documents/code"
    search = "errorFatal.ejs".lower()

    d = {}
    for i in range(2, 20):
        print(i)
        l = []
        for j in range(3):
            ti = time.time()
            results = parallel_search(path, search, nb_workers=i)
            l.append(time.time() - ti)

            # print("Found:")
            # for r in results:
            #     print(r)
        d[i] = np.mean(l)

    print(d)