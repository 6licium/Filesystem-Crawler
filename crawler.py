import os 

path = "C:/Users/lucas/Documents/code"
search = "errorFatal.ejs".lower()

stacks = []
nbStacks = 4

start = os.listdir(path)
cut = len(start)//nbStacks

for i in range(nbStacks):
    if i == nbStacks-1:
        stacks.append(start[cut*i:])
    else:
        stacks.append(start[cut*i:cut*(i+1)])


def unstack(stack):
    found = False

    while len(stack) != 0:
        path_el = stack[0]
        path_full = f"{path}/{path_el}"
        
        if os.path.isfile(path_full):
            if path_el.split("/")[-1].lower() == search:
                found = True
        else:
            l = os.listdir(path_full)
            l = list(map(lambda x:f"{path_el}/{x}", l))
            stack += l
        
        del stack[0]

    return found

print(unstack(stacks[0]))