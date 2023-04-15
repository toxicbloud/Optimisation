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


print(distanceEuclidienne(rempli, rempli[0][0], rempli[1][1]))

#affiche les deux lettres choisies
print(rempli[0][0], rempli[1][1])

print(adaptation(rempli))
printKeyboardInPlot(rempli)

