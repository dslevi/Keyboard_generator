import random

def individual(l, min, max):
    return[random.randint(min, max) for x in range(l)]

def population(count, length, min, max):
    return[individual(length, min, max) for x in range(count)]

#assign fitness score
def fitness(individual, target):
    total = 0
    for num in individual:
        total+= num
    return 100 - (abs(target-total)/ target * 100)

def evolve(population, target, min, max, retain=0.2, random_select=0.05, mutate=0.01):
    grades = [(fitness(ind, target), ind) for ind in population]
    graded = [ind_grade[1] for ind_grade in sorted(grades, reverse=True)]
    num_retained = int(len(graded) * retain)
    parents = graded[:num_retained]

    #randomly add other ind to promote diversity
    for ind in graded[num_retained:]:
        if random_select > random.randint(0, 1):
            parents.append(ind)

    #mutate some ind in parent pool
    for ind in parents:
        if mutate > random.randint(0, 1):
            position_to_mutate = random.randint(0, len(ind) -1)
            ind[position_to_mutate] = random.randint(min, max)

    num_parents = len(parents)
    desired_num_children = len(population) - num_parents
    children = []

    while len(children) < desired_num_children:
        p1 = random.choice(parents)
        p2 = random.choice(parents)

        if p1 != p2:
            half = int(len(p1)/2)
            child = p1[half:] + p2[:half]
            children.append(child)

        parents.extent(child)
        return parents

def main():
    target = 100
    pop_size = 10
    ind_length = 6
    min_num = 0
    max_num = 50

    pop = population(pop_size, ind_length, min_num, max_num)
    num_gen = 0

    loop = True

    while loop:
        for ind in pop:
            if fitness(ind, target) == 100:
                print "Winner ", ind
                loop = False

        pop = evolve(pop, target, min_num, max_num)
        num_gen += 1

        print("Goal reached! It took ", num_gen, "generations.")

main()