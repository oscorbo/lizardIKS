from math import sqrt
from pyglet import shapes

def distanceBetween2Points(joint1: shapes.Circle, joint2: shapes.Circle):
    temp1 = (joint2.x - joint1.x)**2
    temp2 = (joint2.y - joint1.y)**2
    return sqrt(temp1 + temp2)

def set_size_array(amount):
    theArray = []
    for i in range(0, int(amount)):
        theArray.append(0)
    return theArray

def set_array_in_array(target):
    final = []
    for joint in target:
        toadd = [joint.x, joint.y]
        final.append(toadd)
    return final

def solveForwardPosition(inversePosition, lengths_bones):
    forwardPosition = set_size_array(len(inversePosition))
    i = 0
    while i < len(inversePosition):
        if i == 0:
            ## TO FIX
            forwardPosition[i] = [0, 0]
        else:
            posPrimalActual = inversePosition[i]
            posPrimalSecundaAnterior = forwardPosition[i - 1]
            ## make it void
            tempX = posPrimalActual[0] - forwardPosition[i - 1][0]
            tempY = posPrimalActual[1] - forwardPosition[i - 1][1]
            ##
            direction_no_normalized = [tempX, tempY]
            direction = normalize(direction_no_normalized)

            boneIterationLen = lengths_bones[i - 1]
            forwardTempX = posPrimalSecundaAnterior[0] + (direction[0] * boneIterationLen)
            forwardTempY = posPrimalSecundaAnterior[1] + (direction[1] * boneIterationLen)
            forwardPosition[i] = [forwardTempX, forwardTempY]
        i += 1
    return forwardPosition

def solveInversePosition(forwardPositions, target: shapes.Circle, lengths_bones):
    inversePosition = set_size_array(len(forwardPositions))
    amount_positions = len(forwardPositions)
    
    i = amount_positions - 1
    
    while i >= 0:
        if i == amount_positions - 1:
            xTarget = target.x + 500
            yTarget = target.y
            inversePosition[i] = [xTarget, yTarget]
        else:
            posPrimaNext = inversePosition[i + 1]
            posBaseActual = forwardPositions[i]
            ## make it void
            tempX = posBaseActual[0] - posPrimaNext[0]
            tempY = posBaseActual[1] - posPrimaNext[1]
            ##
            direction_no_normalized = [tempX, tempY]
            direction = normalize(direction_no_normalized)

            boneIterationLen = lengths_bones[i]
            ## make it void
            inverseTempX = posPrimaNext[0] + (direction[0] * boneIterationLen)
            inverseTempY = posPrimaNext[1] + (direction[1] * boneIterationLen)
            inversePosition[i] = [inverseTempX, inverseTempY]
        i -= 1
    return inversePosition

def normalize(vector):
    x = vector[0] * vector[0]
    y = vector[1] * vector[1]
    vector_leng = sqrt(x + y)
    if vector_leng == 0:
        return [0,0]
    vector_to_return = [vector[0]/vector_leng, vector[1]/vector_leng]
    return vector_to_return

def vector(joint1: shapes.Circle, joint2: shapes.Circle):
    return [joint1.x - joint2.x, joint1.y - joint2.y]
