# clavier rectangulaire 10 * 4 touches , 40 touches
# 26 touches de A à Z

# double tableau pour representer le bigramme 
# 26 * 26 = 676 bigrammes
import random
import matplotlib.pyplot as plt
import numpy as np


bigramme = [[0 for x in range(26)] for y in range(26)]

# open freqBigrammes.txt
with open('freqBigrammes.txt', 'r') as f:
    next(f) # on passe la premiere qui ne contient que les noms des colonnes
    for i,line in enumerate(f):
        colonnes = line.split()
        ic = iter(colonnes)
        next(ic) # on passe la premiere colonne qui contient le nom de la ligne
        for j, c in enumerate(ic):
            # rempli le tableau sous la forme bigramme["A"]["B"] = 65222
            bigramme[i][j] = int(c)

print(bigramme[0][0])

def getBigrammeFrequency(bigramme, c1, c2):
    return bigramme[ord(c1) - ord('A')][ord(c2) - ord('A')]

# classe representant un clavier
class Keyboard:
    def __init__(self,layout):
        # self.touche = [[0 for x in range(10)] for y in range(4)]
        self.layout = layout
        self.score = 0
    def distance(self, letter1, letter2):
        # distance entre 2 touches
        return abs(letter1[0] - letter2[0]) + abs(letter1[1] - letter2[1])
clavier = Keyboard([["A","B","C","D","E","F","G","H","I","J"],["K","L","M","N","O","P","Q","R","S","T"],["U","V","W","X","Y","Z"]])
print(clavier.distance((0,0),(0,1)))


# objectiv function for a taboo search heuristic
def objectiveFunction(clavier, word):
    score = 0
    for i in range(len(word) - 1):
        score += getBigrammeFrequency(bigramme, word[i], word[i+1])
    return score

# taboo search heuristic
def tabooSearch(clavier, word, tabooList, tabooSize):
    bestScore = objectiveFunction(clavier, word)
    bestWord = word
    for i in range(len(word) - 1):
        for j in range(i+1, len(word)):
            newWord = word[:i] + word[j] + word[i+1:j] + word[i] + word[j+1:]
            if newWord not in tabooList:
                tabooList.append(newWord)
                if len(tabooList) > tabooSize:
                    tabooList.pop(0)
                newScore = objectiveFunction(clavier, newWord)
                if newScore > bestScore:
                    bestScore = newScore
                    bestWord = newWord
    return bestWord

# call taboo search heuristic



# genere une matrice de 4 lignes et 10 colonnes vide
def generateEmptyMatrix():
    return [["" for x in range(10)] for y in range(4)]

empty = generateEmptyMatrix()

# dessine le clavier dans la console avec les traits
def printKeyboardInCLI(clavier):
    for i in range(4):
        for j in range(10):
            print(clavier[i][j], end='')
            if j < 9:
                print(" - ", end='')
        print()

# rempli aléatoirement le clavier sachant qu'il y a 26 lettres et 40 touches
def fillRandomly(clavier):
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # list de touche vide
    empty = [" "] * (40 - len(letters))
    # concatene les 2 listes
    letters = letters + empty
    for i in range(4):
        for j in range(10):
            if clavier[i][j] == "":
                index = random.randint(0, len(letters) - 1)
                clavier[i][j] = letters[index]
                letters.pop(index)
    return clavier

rempli = fillRandomly(empty)
printKeyboardInCLI(rempli)

def printKeyboardInPlot(clavier):
    fig, ax = plt.subplots()
    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    # Calculer le nombre de lignes et de colonnes du clavier
    num_lignes = len(clavier)
    num_colonnes = len(clavier[0])
    # Créer une liste de largeurs de colonnes pour que les cases soient carrées
    cellWidths = [1.0] * num_colonnes
    # draw table
    table = ax.table(cellText=clavier, loc='center', cellLoc='center')
    fig.tight_layout()
    plt.show()


# affiche coeff bigramme AB
print(getBigrammeFrequency(bigramme, "A", "B"))

def distanceEuclidienne(clavier, letter1:str, letter2:str):
    # trouver la position de la lettre 1
    for i in range(4):
        for j in range(10):
            if clavier[i][j] == letter1:
                pos1 = (i,j)
            if clavier[i][j] == letter2:
                pos2 = (i,j)
    # calculer la distance euclidienne
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
def distanceManhattan(clavier, letter1:str, letter2:str):
    # trouver la position de la lettre 1
    for i in range(4):
        for j in range(10):
            if clavier[i][j] == letter1:
                pos1 = (i,j)
            if clavier[i][j] == letter2:
                pos2 = (i,j)
    # calculer la distance manhattan
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def adaptation(clavier):
    somme = 0
    for i in range(26):
        for j in range(26):
            if i == j:
                continue
            lettre1 = chr(ord('A') + i)
            lettre2 = chr(ord('A') + j)
            somme += getBigrammeFrequency(bigramme, lettre1, lettre2) * distanceEuclidienne(clavier, lettre1, lettre2)
    return somme

bestScore = 1000000000000
bestKeyboard = None
# test de 10000 claviers sur 8 coeurs

def test():
    bestScore = 1000000000000
    bestKeyboard = None

    for i in range(10000):
        test = fillRandomly(generateEmptyMatrix())
        score = adaptation(test)
        if score < bestScore:
            bestScore = score
            bestKeyboard = test
    print("best score: ", bestScore)
    return bestScore, bestKeyboard

# vecteur de 26 cases qui contient la position de chaque lettre dans le clavier (ligne, colonne)
def getKeyboardVector(clavier):
    keyboardVector = dict()
    for i in range(4):
        for j in range(10):
            keyboardVector[clavier[i][j]] = (i, j)
    return keyboardVector

aleatoire = fillRandomly(generateEmptyMatrix())
printKeyboardInCLI(aleatoire)
print("===================================")
print(getKeyboardVector(aleatoire))

# def croisement(parent1:dict, parent2:dict):
#     child1 = dict()
#     child2 = dict()
#     # choisir un point de croisement
#     point = random.randint(1, 25)
#     # créer les enfants
#     for i in range(26):
#         if i <= point:
#             child1[chr(ord('A') + i)] = parent1[chr(ord('A') + i)]
#             child2[chr(ord('A') + i)] = parent2[chr(ord('A') + i)]
#         else:
#             child1[chr(ord('A') + i)] = parent2[chr(ord('A') + i)]
#             child2[chr(ord('A') + i)] = parent1[chr(ord('A') + i)]
#     return child1, child2

def croisement(parent1: dict, parent2: dict):
    child1 = dict()
    child2 = dict()
    # choisir deux points de croisement distincts
    point1 = random.randint(1, 25)
    point2 = random.randint(1, 25)
    while point1 == point2:
        point2 = random.randint(1, 25)
    if point1 > point2:
        point1, point2 = point2, point1
    # copier la portion entre les points de croisement des parents dans les enfants
    for i in range(point1, point2 + 1):
        child1[chr(ord('A') + i)] = parent1[chr(ord('A') + i)]
        child2[chr(ord('A') + i)] = parent2[chr(ord('A') + i)]
    # compléter les enfants en copiant les lettres restantes des parents
    letters_to_copy = set(parent1.values()) | set(parent2.values())
    letters_assigned = set(child1.values()) | set(child2.values())
    letters_to_assign = letters_to_copy - letters_assigned
    for i in range(26):
        letter1 = parent1[chr(ord('A') + i)]
        letter2 = parent2[chr(ord('A') + i)]
        if i < point1 or i > point2:
            if letter1 not in child1.values():
                child1[chr(ord('A') + i)] = letter1
            if letter2 not in child2.values():
                child2[chr(ord('A') + i)] = letter2
    # compléter les lettres manquantes dans les enfants en utilisant les lettres restantes
    letters_to_assign = list(letters_to_assign)
    for i in range(26):
        if i < point1 or i > point2:
            letter1 = parent1[chr(ord('A') + i)]
            letter2 = parent2[chr(ord('A') + i)]
            if letter1 in letters_to_assign:
                for key, value in parent2.items():
                    if value not in child1.values() and value not in child2.values():
                        child1[chr(ord('A') + i)] = value
                        letters_to_assign.remove(value)
                        break
            if letter2 in letters_to_assign:
                for key, value in parent1.items():
                    if value not in child1.values() and value not in child2.values():
                        child2[chr(ord('A') + i)] = value
                        letters_to_assign.remove(value)
                        break
    return child1, child2


def verifyDuplicateLetters(clavier):
    # créer une liste vide pour stocker les lettres
    letters = []
    # vérifier les lettres dupliquées
    for i in range(4):
        for j in range(10):
            if clavier[i][j] in letters:
                return False
            letters.append(clavier[i][j])
    return True


def mutation(clavier:dict):
    # choisir deux lettre a échanger
    letter1 = random.randint(0, 25)
    letter2 = random.randint(0, 25)
    # échanger les lettres
    clavier[chr(ord('A') + letter1)], clavier[chr(ord('A') + letter2)] = clavier[chr(ord('A') + letter2)], clavier[chr(ord('A') + letter1)]
    return clavier

def adaptation(clavier:dict):
    somme = 0
    for i in range(26):
        for j in range(26):
            if i == j:
                continue
            lettre1 = chr(ord('A') + i)
            lettre2 = chr(ord('A') + j)
            somme += getBigrammeFrequency(bigramme, lettre1, lettre2) * distanceEuclidienne(clavier, lettre1, lettre2)
    return somme

def verifierVecteurClavier(clavier:dict):
    if len(clavier) != 26:
        return False, "Le vecteur clavier n'a pas 26 lettres"
    # vérifier que les lettres sont bien dans l'alphabet
    for letter in clavier:
        if letter < 'A' or letter > 'Z':
            print("pas bon")
            return False, "La lettre " + letter + " n'est pas dans l'alphabet"
    # verifier que les positions ne sont pas dupliquées
    verif = []
    for position in clavier.values():
        if position in verif:
            return False, "La position " + str(position) + " est dupliquée"
        verif.append(position)
    return True, "Le vecteur clavier est valide"

def distanceEuclidienne(clavier, letter1:str, letter2:str):
    # trouver la position de la lettre 1
    pos1 = clavier[letter1]
    pos2 = clavier[letter2]
    # calculer la distance euclidienne
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def getBestKeyboard(clavier1:dict, clavier2:dict):
    if adaptation(clavier1) < adaptation(clavier2):
        return clavier1
    return clavier2

def getWorstKeyboard(clavier1:dict, clavier2:dict):
    if adaptation(clavier1) > adaptation(clavier2):
        return clavier1
    return clavier2

def generateRandomKeyboardVector():
    positionsToFill = [(i, j) for i in range(4) for j in range(10)]
    keyboardVector = dict()
    for i in range(26):
        # choisir une position au hasard
        position = random.choice(positionsToFill)
        # ajouter la lettre dans le vecteur
        keyboardVector[chr(ord('A') + i)] = position
        # supprimer la position de la liste
        positionsToFill.remove(position)
    return keyboardVector

keyboardvector1 = generateRandomKeyboardVector()
keyboardvector2 = generateRandomKeyboardVector()
print("keyboardvector1: ", keyboardvector1)
print("keyboardvector2: ", keyboardvector2)
print("===================================")
croise1,croise2 = croisement(keyboardvector1, keyboardvector2)
print("croise 1: ", croise1)
print("croise 2: ", croise2)
print("===================================")
print("mutation: ", mutation(keyboardvector1))
print("===================================")
print("adaptation: ", adaptation(keyboardvector1))


# générer une population de 100 claviers
def generatePopulation():
    population = []
    for i in range(135):
        vec = generateRandomKeyboardVector()
        population.append(vec)
    return population

# sélectionner les meilleurs claviers
def selection(population:list):
    population.sort(key=adaptation)
    return population[:50]

# générer une nouvelle population
def generateNewPopulation(population:list):
    newPopulation = []
    # ajouter les meilleurs claviers
    parents = selection(population)
    newPopulation.extend(parents)
    # ajouter des enfants
    for i in range(35):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child1, child2 = croisement(parent1, parent2)
        t,r = verifierVecteurClavier(child1)
        if not t:
            print("erreur enfant 1")
            print(r)
            print(child1)
        t,r = verifierVecteurClavier(child2)
        if not t:
            print("erreur enfant 2")
            print(r)
            print(child2)
        if not t:
            exit()
        newPopulation.append(child1)
        newPopulation.append(child2)
    # ajouter des mutations
    for i in range(15):
        clavier = random.choice(population)
        mutant = mutation(clavier)
        # newPopulation.append()
        if not verifierVecteurClavier(mutant):
            print("erreur")
        newPopulation.append(mutant)
    return newPopulation

# générer une population
population = generatePopulation()
for p in population:
    t,r = verifierVecteurClavier(p)
    if not t:
        print("erreur init")
        print(r)
        exit()

parent1 = random.choice(population)
parent2 = random.choice(population)
child1, child2 = croisement(parent1, parent2)

print("parent 1: ", parent1)
print("-----------------------------------")
print("parent 2: ", parent2)
print("-----------------------------------")
print("enfant 1: ", child1)
print("-----------------------------------")
print("enfant 2: ", child2)


meilleuresAdaptations = []

# générer 100 nouvelles populations
for i in range(300):
    population = generateNewPopulation(population)
    for p in population:
        t,r = verifierVecteurClavier(p)
        if not t:
            print("erreur APRES GENERATION de la ", i, " ème population")
            print(r)
            exit()
    population.sort(key=adaptation)
    meilleuresAdaptations.append(adaptation(population[0]))
    print("Génération ", i,"taille de la population : ",len(population), " Meilleur individu : ", adaptation(population[0]))
population.sort(key=adaptation)
# afficher le meilleur clavier sous forme de tableau
print("===================================")
print("Meilleur clavier: ")
print(population[0])
print(adaptation(population[0]))

# transforme le vecteur clavier en matrice
def keyboardVectorToMatrix(keyboardVector:dict):
    keyboardMatrix = generateEmptyMatrix()
    for letter in keyboardVector:
        keyboardMatrix[keyboardVector[letter][0]][keyboardVector[letter][1]] = letter
    return keyboardMatrix

mres = keyboardVectorToMatrix(population[0])

printKeyboardInPlot(mres)

# genere un graphique avec meilleure adaptation en fonction du numéro de génération
plt.plot(meilleuresAdaptations)
plt.show()