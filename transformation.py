import math


######################### TRATAMENTO DE VERTICES DAS FUNÇÕES 2D #########################
def scaling(v, t):
    for i in range(len(v)):
        for j in range(0, 1):
            x2 = v[i][j] * t[j]
            y2 = v[i][j + 1] * t[j + 1]
            print("Coordenadas escaladas do vertice ", i + 1, " : x2 = ", x2, " ,  y2 = ", y2)
            vetor_resultado = [x2, y2]
    return (vetor_resultado)


def rotation(v, o, a, *, cr: bool = False):
    s = math.sin(math.radians(a))
    s = round(s, 2)
    c = math.cos(math.radians(a))
    c = round(c, 2)
    for i in range(len(v)):
        for j in range(0, 1):
            if cr is True:
                x2 = o[j] + ((v[i][j] - o[j]) * c) + ((v[i][j + 1] - o[j + 1]) * s)
                y2 = o[j + 1] + ((v[i][j] - o[j]) * (-s)) + ((v[i][j + 1] - o[j + 1]) * c)
                x2 = round(x2, 2)
                y2 = round(y2, 2)
            print("Coordenadas rotacionadas do vertice ", i + 1, " : x2 = ", x2, " ,  y2 = ", y2)
            vetor_resultado = [x2, y2]
    return(vetor_resultado)



def reflectionx(v):
    for i in range(len(v)):
        for j in range(0, 1):
            x2 = v[i][j]
            y2 = -v[i][j + 1]
            print("Reflexao x do vertice ", i + 1, " : x2 = ", x2, " ,  y2 = ", y2)
            vetor_resultado = [x2, y2]
    return (vetor_resultado)


def reflectiony(v):
    for i in range(len(v)):
        for j in range(0, 1):
            x2 = -v[i][j]
            y2 = v[i][j + 1]
            print("Reflexao y do vertice ", i + 1, " : x2 = ", x2, " ,  y2 = ", y2)
            vetor_resultado = [x2, y2]
    return (vetor_resultado)


def reflectionxy(v):
    for i in range(len(v)):
        for j in range(0, 1):
            x2 = v[i][j + 1]
            y2 = v[i][j]
            print("reflexao XY do vertice", i + 1, " : x2 = ", x2, " ,  y2 = ", y2)
            vetor_resultado = [x2, y2]
    return (vetor_resultado)
