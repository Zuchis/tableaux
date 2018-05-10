import sys
from copy import deepcopy

class Node: 
    def __init__(self):
        self.value = False
        self.token = ''
        self.leftC = None
        self.rightC = None

    def printTree(self):
        print(self.token,end="")
        if self.leftC:
            self.leftC.printTree()
        if self.rightC:
            self.rightC.printTree()

    def formula(self):
        if self.leftC and self.rightC:
            return str(self.token) + self.leftC.formula() + self.rightC.formula()
        elif self.leftC:
            return str(self.token) + self.leftC.formula()
        
        return str(self.token)

    def printValue(self):
        print(self.token + " " + str(self.value))

count = 0
cardinality = 0
currentFormula = []
formulas = []

def parse():
    node = Node()
    node.token = currentFormula[0]
    currentFormula.pop(0)
    if (node.token in ['*','+',')']):
        node.leftC = parse()
        node.rightC = parse()
    elif (node.token == '-'):
        node.leftC = parse()
        node.rightC = None
    else:
        node.leftC = None
        node.rightC = None
    return node

with open('test/2.seq') as f:
    for l in f:
        line = []
        if (count == 0):
            cardinality = l
            count += 1
        else:
            line = l.split(" ")
            line[len(line)-1] = line[len(line)-1].rstrip()
            # print(line)
            currentFormula = line
            formulas.append(parse())

for i in range(0, int(cardinality)):
    formulas[i].value = True

for i in range(int(cardinality), len(formulas)):
    formulas[i].value = False

def checkAlphaExpansion(forms):
    for index, form in enumerate(forms):
        if ((form.token == '*' and form.value == True) or
            (form.token == '+' and form.value == False) or
            (form.token == ')' and form.value == False) or
            (form.token == '-')):
            return index
    return -1

def checkBetaExpansion(forms):
    for index, form in enumerate(forms):
        if ((form.token == '*' and form.value == False) or
            (form.token == '+' and form.value == True) or
            (form.token == ')' and form.value == True)):
            return index
    return -1

def alphaExpand(index, forms):
    form = forms[index]
    a1 = deepcopy(form.leftC)
    a2 = deepcopy(form.rightC)
    if form.token == '*':
        a1.value = True
        a2.value = True
    elif form.token == '+':
        a1.value = False
        a2.value = False
    elif form.token == ')':
        a1.value = True
        a2.value = False
    elif form.token == '-':
        a1.value = not form.value

    forms.pop(index)

    forms.append(a1)
    a1Formula = a1.formula()

    if (a2 is not None):
        forms.append(a2)
        a2Formula = a2.formula()
        for f in forms:
            fFormula = f.formula()
            if ((a1Formula == fFormula and a1.value == (not f.value)) or
                (a2Formula == fFormula and a2.value == (not f.value))):
                return True
    else:
        for f in forms:
            fFormula = f.formula()
            if (a1Formula == fFormula and a1.value == (not f.value)):
                return True

    return False

def betaExpand(index, forms):
    form = forms[index]
    b1 = deepcopy(form.leftC)
    b2 = deepcopy(form.rightC)
    if form.token == '*':
        b1.value = False
        b2.value = False
    elif form.token == '+':
        b1.value = True
        b2.value = True
    elif form.token == ')':
        b1.value = False
        b2.value = True

    forms.pop(index)

    return (b1,b2)

def checkForBetaClosed(forms):
    beta = forms[-1]
    betaFormula = beta.formula()
    
    for f in forms:
        fFormula = f.formula()
        if (betaFormula == fFormula and beta.value == (not f.value)):
            return True

    return False

def mainLoop(forms):
    index = 0
    closed = False
    while index != -1 and not closed:
        index = checkAlphaExpansion(forms)

        if index != -1:
            closed = alphaExpand(index, forms)

    if not closed: # Ramo aberto, verificar expansões beta
        index = checkBetaExpansion(forms)

        if index != -1: #Expansão beta
            b1, b2 = betaExpand(index, forms)
            formsB1 = deepcopy(forms)
            formsB1.append(b1)
            closedB1 = checkForBetaClosed(formsB1)

            if not closedB1:
                mainLoop(formsB1)

            formsB2 = deepcopy(forms)
            formsB2.append(b2)
            closedB2 = checkForBetaClosed(formsB2)

            if not closedB2:
                mainLoop(formsB2)

        else: # Ramo aberto e saturado
            for i in forms:
                i.printValue()
            sys.exit(0)


def prover(forms):
    mainLoop(forms)

    return True

if __name__ == "__main__":
    forms = deepcopy(formulas)

    result = prover(forms)

    print(result);
