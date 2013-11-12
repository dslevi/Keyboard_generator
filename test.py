import random

def randomBlocks():
    blocks = []
    for x in range(55):
        blocks.append("block" + str(random.randint(1, 3)))
    return blocks