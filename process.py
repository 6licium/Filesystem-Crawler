import os
import time
import numpy as np
from multiprocessing import Process, Manager, Queue

def worker(i, path_root, search, stack, empty, queue, found):
    """Worker avec pile locale + work-stealing."""
    print("start")
    while len(stack) != 0 and not np.any(empty):
        # if i == 0:
        #     print(len(stack))

        rel_path = stack.pop()
        full_path = os.path.join(path_root, rel_path)

        if os.path.isfile(full_path):
            if os.path.basename(full_path).lower() == search:
                found.append(full_path)
        else:
            try:
                children = os.listdir(full_path)
                for child in children:
                    stack.append(os.path.join(rel_path, child))
            except PermissionError:
                continue
        
        if np.any(empty):
            half = len(stack) // 2
            queue.put(stack[half:])
            stack = stack[:half]

        if len(stack) == 0:
            empty[i] = True

        if len(stack) == 0 and not np.all(empty):
            print(i, len(stack))
            stack = queue.get()
            empty[i] = False
            print(i, len(stack))
                
        # if len(stacks[i]) == 0:
        #     print(i)
        #     lens = [len(s) for s in stacks]
        #     j = max(range(len(stacks)), key=lambda k: lens[k])
        #     half = lens[j] // 2
        #     stacks[j], stacks[i] = stacks[j][:half], stacks[j][half:]


def parallel_search(path, search, nb_workers=3):

    # liste de piles partagée → chaque pile est une Manager.list()
    stacks = [[] for _ in range(nb_workers)]
    found = Manager().list([])
    empty = Manager().list([False for _ in range(nb_workers)])
    queue = Queue()

    # distribution initiale du travail comme ton initStack()
    start = os.listdir(path)
    for j, el in enumerate(start):
        stacks[j % nb_workers].append(el)

    processes = []
    for i in range(nb_workers):
        p = Process(target=worker, args=(i, path, search, stacks[i], empty, queue, found))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    return list(found)



if __name__ == "__main__":
    path = "test_arbo"
    search = "errorFatal.ejs".lower()

    ti = time.time()
    results = parallel_search(path, search, nb_workers=3)
    print(time.time() - ti)

    print("Found:")
    print(results)
