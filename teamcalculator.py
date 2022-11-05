from copy import deepcopy

# format: type : ([strong against], [weak to])
typeData = {'bug' : (['dark', 'grass', 'psychic'], ['fire', 'flying', 'rock']),
            'dark' : (['ghost', 'psychic'], ['bug', 'fairy', 'fighting']),
            'dragon' : (['dragon'], ['dragon', 'fairy', 'ice']),
            'electric' : (['flying', 'water'], ['ground']),
            'fairy' : (['dark', 'dragon', 'fighting'], ['poison', 'steel']),
            'fighting' : (['dark', 'ice', 'normal', 'rock', 'steel'], ['fairy', 'flying', 'psychic']),
            'fire' : (['bug', 'grass', 'ice', 'steel'], ['ground', 'rock', 'water']),
            'flying' : (['bug', 'grass', 'fighting'], ['electric', 'ice', 'rock']),
            'ghost' : (['ghost', 'psychic'], ['dark', 'ghost']),
            'grass' : (['ground', 'rock', 'water'], ['bug', 'fire', 'flying', 'ice', 'poison']),
            'ground' : (['electric', 'fire', 'poison', 'rock', 'steel'], ['grass', 'ice', 'water']),
            'ice' : (['dragon', 'flying', 'grass', 'ground'], ['fighting', 'fire', 'rock', 'steel']),
            'normal' : ([], ['fighting']),
            'poison' : (['fairy', 'grass'], ['ground', 'psychic']),
            'psychic' : (['fighting', 'poison'], ['bug', 'dark', 'ghost']),
            'rock' : (['bug', 'fire', 'flying', 'ice'], ['fighting', 'grass', 'ground', 'steel', 'water']),
            'steel' : (['fairy', 'ice', 'rock'], ['fighting', 'fire', 'ground']),
            'water' : (['fire', 'ground', 'rock'], ['electric', 'grass'])
            }

typeDict = {'bug' : 0, 'dark' : 0, 'dragon' : 0, 'electric' : 0, 'fairy' : 0,
            'fighting' : 0, 'fire' : 0, 'flying' : 0, 'ghost' : 0, 'grass' : 0, 'ground' : 0, 'ice' : 0, 'normal' : 0, 'poison' : 0, 'psychic' : 0, 'rock' : 0, 'steel' : 0, 'water' : 0}

class Pokemon:
    def __init__(self, name, types, attacks):  # lists of types & attack types
        self.name = name
        self.types = types
        self.resistances = []
        self.vulnerabilities = []
        self.strengths = []
        self.weaknesses = []
        for t1 in self.types:
            (r, v) = typeData[t1]
            for t2 in typeDict:
                if (t2 in r) and (t2 in v):
                    pass
                elif t2 in r and t2 not in self.resistances:
                    self.resistances.append(t2)
                elif t2 in v and t2 not in self.vulnerabilities:
                    self.vulnerabilities.append(t2)
        for t1 in self.types:
            (s, w) = typeData[t1]
            for t2 in typeDict:
                if (t2 in s) and (t2 in w):
                    pass
                elif t2 in s and t2 not in self.strengths:
                    self.strengths.append(t2)
                elif t2 in w and t2 not in self.weaknesses:
                    self.weaknesses.append(t2)

class Team:
    def __init__(self, size, members=[]):
        self.size = size
        self.members = members
        self.resistanceCount = deepcopy(typeDict)
        self.vulnerabilityCount = deepcopy(typeDict)
        self.strengthCount = deepcopy(typeDict)
        self.weaknessCount = deepcopy(typeDict)
        for p in self.members:
            for r in p.resistances:
                self.resistanceCount[r] += 1
            for v in p.vulnerabilities:
                self.vulnerabilityCount[v] += 1
            for s in p.strengths:
                self.strengthCount[s] += 1
            for w in p.weaknesses:
                self.weaknessCount[w] += 1

    def evaluateStrengths(self):
        strongestScore = 0
        strongestTypes = []
        for t in typeDict:
            strongScore = self.resistanceCount[t] + self.strengthCount[t]
            if strongScore > strongestScore:
                strongestTypes = [t]
                strongestScore = strongScore
            elif strongScore == strongestScore and strongScore > 0:
                strongestTypes.append(t)
        return strongestTypes

    def evaluateWeaknesses(self):
        weakestScore = 0
        weakestTypes = []
        for t in typeDict:
            weakScore = self.weaknessCount[t] + self.vulnerabilityCount[t]
            if weakScore > weakestScore:
                weakestTypes = [t]
                weakestScore = weakScore
            elif weakScore == weakestScore and weakScore > 0:
                weakestTypes.append(t)
        return weakestTypes

    def score(self):
        scoreSum = 0
        weaknesses = self.evaluateWeaknesses()
        strengths = self.evaluateStrengths()
        for w in weaknesses:
            if w not in strengths:
                scoreSum -= 1
        for s in strengths:
            scoreSum += 1
        return scoreSum

    def fill(self):
        if self.size == len(self.members):  # return fully formed team
            return self
        # use recursion to generate & compare hypothetical team additions
        bestTeam = []
        bestScore = 0
        for t in typeDict:
            p = Pokemon('new '+t+'-type', [t], [t, t])  # just recommend basic one-type pokemon with same-type attacks
            nTeam = Team(self.size, self.members+[p])
            s = nTeam.score()
            if s > bestScore or not bestTeam:
                bestTeam = nTeam
                bestScore = s
        return bestTeam.fill()

def inputPokemon():
    types = []
    attacks = []
    print('\n'+'Enter this pokemon\'s information below. If it does not have a second type or second charged attack, just hit ENTER.')
    name = input('Pokemon name: ')
    t1 = input('Primary type: ')
    types.append(t1.lower())
    t2 = input('Second type: ')
    if t2:
        types.append(t2.lower())
    a1 = input('Fast attack type: ')
    attacks.append(a1.lower())
    a2 = input('First charged attack type: ')
    attacks.append(a2.lower())
    a3 = input('Second charged attack type: ')
    if a3:
        attacks.append(a3.lower())
    return Pokemon(name, types, attacks)

def printList(l):
    s = ''
    n = len(l)
    if n == 0:
        return 'nothing'
    elif n == 1:
        return l[0]
    else:
        for i in range(n):
            s += l[i] + ', '*(i!=n-1) + 'and '*(i==n-2)
        return s

# Main:
teamSize = int(input('Size of team: '))
teamMembers = []
for i in range(teamSize-1):
    usr = input(str(i)+'/'+str(teamSize)+' pokemon predetermined. Add pokemon? (Y/N) ')
    if usr.lower() == 'n':
        break
    else:
        p = inputPokemon()
        teamMembers.append(p)
oTeam = Team(teamSize, teamMembers)
nTeam = oTeam.fill()
teamNames = [m.name for m in nTeam.members]
print('\n'+
    'We generated the following team of '+str(teamSize)+' pokemon, with a rating of '+str(nTeam.score())+':\n'+
    printList(teamNames)+'.\n'+
    'It is strongest against '+printList(nTeam.evaluateStrengths())+' type pokemon, and weakest against '+printList(nTeam.evaluateWeaknesses())+'.\n')
