import math
import random
import time

def chromSpawner(chromosomeLen):
    #init empty list
    chromosome = []
    #loop sepanjang chromosomeLen untuk mengisi dengan variabel kosong(✿´‿`)
    for i in range(chromosomeLen): 
        # random antara 0 dan 1 (representasi biner)
        chromosome.append(random.randint(0, 1))
    return chromosome

def decodeChromosome(chromosome):
    # reperesentasi panjang kromosom secara keseluruhan
    cLen = int(len(chromosome))
    # setengah cLen untuk representasi gen
    cGen = int(len(chromosome) / 2)
    #temporary kromosom dengan .copy() agar pointer berubah
    tempChromosome = chromosome.copy()
    # penyebut, dalam rumus sigma(i=1,N)(2^-i)
    denominator = 0
    for i in range(0,cGen):
        # decode first half chromosome atau x
        tempChromosome[i] = chromosome[i] * (2 ** -(i + 1))
        #decpde second half chromosome atau y
        tempChromosome[i + cGen] = chromosome[i + cGen] * (2 ** -(i + 1))
        denominator = denominator + (2 ** -(i + 1))
    
    # rumus binary decoding
    x = xMin + ((xMax - xMin) / denominator) * sum(tempChromosome[0:cGen])
    y = yMin + ((yMax - yMin) / denominator) * sum(tempChromosome[cGen:cLen])
    # memastikan variabel tempChromosome tidak memegang value apa apa
    return x, y

def firstPopulation(popSize):
    population = []
    # loop sebanyak panjang popsize dengan menggabungkan population dengan chromosome
    for i in range(popSize):
        population.append(chromSpawner(chromosomeLen))
    return population


def TournamentSelection(population,tournamentSize):
    # inisialisasi list kosong
    best = []
    # loop sepanjang tournamentSize
    for i in range(tournamentSize):
        # inisialisasi indv dengan populationp[random]
        indv = population[random.randint(0,len(population)-1)]
        # conditional pencarian best
        if best == [] or calculateFitness(indv) > calculateFitness(best):
            best = indv
    # return chromosome terbaik
    return best



# crossover 2 poin
def crossover(chromosome1, chromosome2, crossoverProc): 
    # generate currentProbability up to 1.00
    currentProbability = random.random()
    if (currentProbability <= crossoverProc):
        # titik titik crossover yang akan dijadikan batas pertukaran
        swapPoint = random.sample(range(0, chromosomeLen - 1), 2)
        #sort untuk memudahkan implementasi slicing
        swapPoint.sort()
        # slicing dengan asumsi tanpa batasan gen x dan gen y tertukar
        result1 = (chromosome1[:swapPoint[0]] + chromosome2[swapPoint[0]:swapPoint[1]] + chromosome1[swapPoint[1]:chromosomeLen])
        result2 = (chromosome2[:swapPoint[0]] + chromosome1[swapPoint[0]:swapPoint[1]] + chromosome2[swapPoint[1]:chromosomeLen])
        # return hasil kromosom yang sudah dislice dengan crossover point
        return result1, result2

    # jika kondisi if tidak dipenuhi, return kondisi awal
    return chromosome1, chromosome2

def mutation(chromosome, mutationProc):
    # generate currentProbability up to 1.00
    currentProbability = random.random()
    # if condition saat current probability
    if (currentProbability <= mutationProc):
        ranIndex = random.randint(0, chromosomeLen - 1)
        # perubahan nilai tiap gen dari 0 ke 1 dan sebaliknya
        if (chromosome[ranIndex] == 0):
            chromosome[ranIndex] = 1
        else:
            chromosome[ranIndex] = 0

# def mutation(chromosome, mutationProc):
#     # generate currentProbability up to 1.00
#     currentProbability = random.random()
#     # if condition saat current probability
#     for i in range (len(chromosome)):
#         if currentProbability <= mutationProc:
#         # perubahan nilai tiap gen dari 0 ke 1 dan sebaliknya
#             if (chromosome[i] == 0):
#                 chromosome[i] = 1
#             else:
#                 chromosome[i] = 0

def getElitisme(population):
    best = []
    # pencarian populasi dengan fitness terbaik sepanjang populasi
    for i in range(len(population)):
        # conditional if pencarian fitness terbaik
        if (best == [] or calculateFitness(population[i]) > calculateFitness(best)):
            best = population[i]
    return best

def calculateFitness(chromosome):
    # parameter menerima list chromosome untuk di decode menjadi variabel x dan y
    x , y = decodeChromosome(chromosome)
    # return berupa fitness value dengan f=h karena mencari nilai maks
    return float(math.cos((math.radians(pow(x,2)))) * math.sin((math.radians(pow(y,2)))) + x + y)


def nextGeneration(currentPop):
    # implementasi loop kedua pada generational replacement
    # sesuai pseudocode
    nextPopulation = []
    while len(nextPopulation) != len(currentPop) -2 :
        # mencari parent dengan metode seleksi orangtua tournament
        parent1 = TournamentSelection(currentPop,tournamentSize)
        parent2 = TournamentSelection(currentPop,tournamentSize)
        # jika identik lakukan perulangan hingga unik
        while parent1 == parent2:
            parent2 = TournamentSelection(currentPop,tournamentSize)
        # offspring 1 dan 2 dilakukan crossover
        offspring1,offspring2 = crossover(parent1,parent2,crossoverProc)
        # offsprint 1 dan 2 dilakukan mutation
        mutation(offspring1,mutationProc)
        mutation(offspring2,mutationProc)
        # menambahkan (add/append) offspring ke calon populasi baru
        nextPopulation.append(offspring1)
        nextPopulation.append(offspring2)
    # append hasil elitisme currentpop ke nextpop
    nextPopulation.append(getElitisme(currentPop))
    nextPopulation.append(getElitisme(currentPop))

    return nextPopulation
    

# START OF HYPER PAREMETER

#First initialization and constrains
# inisialisasi ukuran populasi
popSize = 60
#ada di soal, constrain masing masing x dan y
xMax ,xMin,yMax,yMin= 2,-1,1,-1
# panjang gen, pembuat setengah dari kromosom
genLen = 6
# terdiri atas gabungan dari gen x dan gen y
chromosomeLen = genLen * 2
#kemungkinan terjadinya crossover #kemungkinan terjadinya mutasi
crossoverProc,mutationProc = 0.7,0.1
# stop condition
expectedFitness = 3.017
# tournament size
tournamentSize = 5

# END OF HYPER PARAMETER

# START OF MAIN PROGRAM
bestChromosome = []
currentPop = firstPopulation(popSize)
# uncomment jika ingin print per gen
i = 0
# print('Current Generation', i, "Best Cromosome :", "".join(str(j) for j in getElitisme(currentPop)),end=' ')
# print("Fitness :", calculateFitness(getElitisme(currentPop)),end=' ')
# print("x,y :", decodeChromosome(getElitisme(currentPop)),end=' ')
# print("")
bestChromosome.append(getElitisme(currentPop))
# loop pertama pada generational replacement dengan stop condition fitness Constrain (expectedfitness)
# start = time.time()
while calculateFitness(getElitisme(currentPop)) < expectedFitness:   
    
    currentPop = nextGeneration(currentPop)
    bestChromosome.append(getElitisme(currentPop))
    # uncomment jika ingin print per gen
    # i = i + 1
    # print('Current Generation', i, "Best Cromosome :", "".join(str(j) for j in getElitisme(currentPop)),end=' ')
    # print("Fitness :", calculateFitness(getElitisme(currentPop)),end=' ')   
    # print("x,y:", decodeChromosome(getElitisme(currentPop)),end=' ')
    # print("")
    
# print("")
print("HASIL MAKSIMUM FUNGSI")
result = getElitisme(bestChromosome)
print("BEST Cromosome    : ", "".join(str(i) for i in result))
print("BEST Fitness      : ", calculateFitness(result))
print("BEST (X,Y)        : ", decodeChromosome(result))
# print("Runtime",time.time() - start)

# END OF MAIN PROGRAM
