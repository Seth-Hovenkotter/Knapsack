import numpy as np

#File reader def
def fileReader(filename):
    vectors = np.genfromtxt(filename, delimiter=',', skip_header=1)
    return vectors

#our greedy algorithm
def greedy(data, sackSize):
    #compute the cost desnsity of an object (cost to weight ratio)
    costDensity = data[:,1] / data[:,0]
    inSack = 0
    items = []
    #while our items in the sack are less than our sack maximum size
    while inSack < sackSize:
        #find the best cost desnsity item
        bestIndex = np.argmax(costDensity)
        costDensity[bestIndex] = 0
        #if the weight of the best density item won't put us over the limit
        if inSack + data[bestIndex, 0] <= sackSize:
            inSack += data[bestIndex, 0]
            #put it in the sack
            items.append(data[bestIndex])
    #return our score
    return np.array(items)

#generate our origional population    
def generatePop(popSize, dataSize):
    pop = np.zeros((popSize, dataSize))
    for i in pop:
        i[np.random.randint(0, dataSize)] = 1
    return pop
    
#def to calculate the fitness of an individual 
def fitness(individual, data, sackSize):
    items = []
    i = 0
    #while our individual still has data
    while i < len(individual):
        if individual[i] == 1:
            #add it to our fitness test list
            items.append(data[i])
        i+=1
    items = np.array(items)
    #if the weight of our individual exceeded the maximum
    if sum(items)[0] > sackSize:
        #give it 0 fitness
        return 0
    else:
        #else sum it and give it its overall fitness
        return sum(items)[1]
    
#def to create our children
def breed(child1, child2):
    r = np.random.randint(0, len(child1))
    return np.concatenate((child1[:r], child2[r:])), np.concatenate((child2[:r], child1[r:]))
 
#def to mutate a child based on our rate
def mutate (child, mutationRate):
    mutatedChild = []
    #for each item in our child
    for i in child:
        #if a random number is less than our mutation rate
        if np.random.random() < mutationRate:
            #change something about the child
            if i == 1:
                #change a 1 to a 0
                mutatedChild.append(0)
            else:
                #or a 0 to a 1
                mutatedChild.append(1)
        #or give them an extra item
        else:
            mutatedChild.append(i)   
    #return our mutant child
    return mutatedChild
    
#def for measuring the fitness of our population
#this makes sure that we don't eliminate all of our individuals 
#it also makes sure that those with a higher fitness are more liketly but not garutneed to survive 
def populationFitness(population, sackSize):
    popFitness = []
    currentFitness = 0
    for i in population:
        currentFitness += fitness(i, data, sackSize)
        popFitness.append(currentFitness)
    return np.array(popFitness) / popFitness[-1]

#def ot selet who lives and who dies       
def tournament(population, data, sackSize, mutationRate):
    childPop = []
    i = 0
    #with our original population create enough children to double it
    while i < len(population)-1:
        child1, child2 = breed(population[i], population[i+1])
        #mutate our kids
        child1 = mutate(child1, mutationRate)
        child2 = mutate(child2, mutationRate)
        childPop.append(child1)
        childPop.append(child2)
        #+2 makes sure that we don't get a ton of extra kids
        #though doing it this way means that each parent will only breed once
        i+=2
    #put our child population and our parent population into one array
    tempPop = np.concatenate((population, np.array(childPop)))
    #our new population before removing individuals
    newPop = populationFitness(tempPop, sackSize)
    newPop = []
    #while we have less than our origional population
    while len(newPop) < len(population):
        r = np.random.random()
        popFitness = populationFitness(tempPop, sackSize)
        i = 0
        #while we have individuals left
        while i < len(popFitness):
            #probability of an indivdual, more fit indivuals have a higher probability
            prob = popFitness[i]
            #if our random is less than our probability then our individual survives and moves on
            if r < prob:
                newPop.append(tempPop[i])
                np.delete(tempPop, i, 0)
                break
            i+=1  
    #return our new population after pruning 
    return np.array(newPop)

#read in our file
data = fileReader('items.csv')
#generate our population from the data
bitPop = generatePop(100, len(data))
#number of generations to run our GA for
generations = 100
#loop to run the GA
print('Fitness:')
for i in range(generations):
    bitPop = tournament(bitPop, data, 200, 0.1)
    #print out our fitness every 10 generations 
    if i%1 == 0:
        print (fitness(bitPop[0], data, 200))

#greedy algorithm 
greed = greedy(data, 200.)
print ('Greedy Algorithm')
print ('Items in Sack:')
print (greed)
print ('\nTotal:')
print (sum(greed))