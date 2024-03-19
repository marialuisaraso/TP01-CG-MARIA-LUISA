import tkinter as tk
import transformation
from tkinter import Canvas, Scale
from PIL import Image, ImageTk, ImageGrab
import math

################################################### BARSKY E COHEN #####################################################
DENTRO = 0  # mesma coisa que 0000 
ESQUERDA = 1    # mesma coisa que 0001 
DIREITA = 2   # mesma coisa que 0010 
EMBAIXO = 4  # mesma coisa que 0100 
EMCIMA = 8     # mesma coisa que 1000 

def barsky(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    p = [-dx, dx, -dy, dy]
    q = [x1 - x_min, x_max - x1, y1 - y_min, y_max - y1]
    t_enter = 0.0
    t_exit = 1.0

    for i in range(4):
        if p[i] == 0:  # Checa a linha em relacao ao clipping window
            if q[i] < 0:
                return None  # Se estiver fora, é descartada
        else:
            t = q[i] / p[i]
            if p[i] < 0:
                if t > t_enter:
                    t_enter = t
            else:
                if t < t_exit:
                    t_exit = t

    if t_enter > t_exit:
        return None  # Linhas completamente fora

    x1_clip = x1 + t_enter * dx
    y1_clip = y1 + t_enter * dy
    x2_clip = x1 + t_exit * dx
    y2_clip = y1 + t_exit * dy

    return x1_clip, y1_clip, x2_clip, y2_clip

def computeCode(x, y): 
    code = DENTRO 
    if x < x_min:      # esquerda do retangulo
        code |= ESQUERDA 
    elif x > x_max:    # direita do retangulo
        code |= DIREITA 
    if y < y_min:      # abaixo do retangulo
        code |= EMBAIXO 
    elif y > y_max:    # acima do retangulo
        code |= EMCIMA 
    
    print(code)
    return code

def cohen(x1, y1, x2, y2):

    canvas.create_line(x1, y1, x2, y2, fill = 'red')
    canvas.grid(row = 0, column = 0)

    # region = [x1, y1, x2, y2]

    code1 = computeCode(x1, y1)
    code2 = computeCode(x2, y2)
    accept = False

    while True: 
  
        # Se os endpoints estiverem dentro do retangulo
        if code1 == 0 and code2 == 0: 
            accept = True
            break
  
        # se os endpoints estiverem fora do retangulo
        elif (code1 & code2) != 0: 
            break

        else: 
  
            x = 1.0
            y = 1.0
            if code1 != 0: 
                code_out = code1 
            else: 
                code_out = code2 
  
            # encontra intersecao
            if code_out & EMCIMA: 
                
                # ponto esta acima do clip
                x = x1 + ((x2 - x1) / (y2 - y1)) * (y_max - y1) 
                y = y_max 
  
            elif code_out & EMBAIXO: 
                  
                # ponto esta abaixo do clip
                x = x1 + ((x2 - x1) / (y2 - y1)) * (y_min - y1) 
                y = y_min 
  
            elif code_out & DIREITA: 
                  
                # ponto esta a direita do clip
                y = y1 + ((y2 - y1) / (x2 - x1)) * (x_max - x1) 
                x = x_max 
  
            elif code_out & ESQUERDA: 
                  
                # ponto esta a direita do clip
                y = y1 + ((y2 - y1) / (x2 - x1)) * (x_min - x1)  
                x = x_min 
  
            # intersecao x e y e encontrada

            if code_out == code1: 
                x1 = x 
                y1 = y 
                code1 = computeCode(x1, y1) 
  
            else: 
                x2 = x 
                y2 = y 
                code2 = computeCode(x2, y2) 
  
    if accept: 
        print ("Linha aceita: %.2f, %.2f to %.2f, %.2f" % (x1, y1, x2, y2)) 
        canvas.create_line(x1, y1, x2, y2, fill = 'YELLOW',  width = 1)
        canvas.grid(row = 0, column = 0)
  
    else: 
        print("Linha rejeitada") 



################################################### DDA E BRESENHAM #####################################################
def dda(x1, y1, x2, y2):
    __dda(x1, y1, x2, y2)

def __dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    x_incr = 0
    y_incr = 0
    x, y = x1, y1
    steps = 0
    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)
    x_incr = dx / steps
    y_incr = dy / steps
    __set_pixel(round(x), round(y))
    for k in range(1, steps):
        x = x + x_incr
        y = y + y_incr
        __set_pixel(round(x), round(y))

def bres(x1, y1, x2, y2):
    __bres(x1, y1, x2, y2)

def __bres(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    incr_x = 0
    incr_y = 0
    
    if (dx >= 0):
        incr_x = 1
    else:
        incr_x = -1
        dx = -dx
    
    if (dy >= 0):
        incr_y = 1
    else:
        incr_y = -1
        dy = -dy
    
    x = x1
    y = y1
    __set_pixel(x, y)

    if (dy < dx):
        p = 2*dy - dx
        const_a = 2*dy
        const_b = 2*(dy - dx)
        for i in range(0, dx):
            x = x + incr_x
            if (p < 0):
                p = p + const_a
            else:
                y = y + incr_y
                p = p + const_b
            __set_pixel(x, y)
    else:
        p = 2*dx - dy
        const_a = 2*dx
        const_b = 2*(dx - dy)
        for i in range(dy):
            y = y + incr_y
            if (p < 0):
                p = p + const_a
            else:
                x = x + incr_x
                p = p + const_b
            __set_pixel(x, y)


def __set_pixel(x, y):
    canvas.create_rectangle(x, y, x + 1, y + 1, fill="YELLOW")



################################## LIDANDO COM CLIQUES E PONTOS NA INTERFACE GRÁFICA#####################################################
def desenhar_linha(event):
    global x_inicial, y_inicial
    global inicial_x, inicial_y, final_x, final_y
    if x_inicial is None and y_inicial is None:
        x_inicial = event.x
        y_inicial = event.y
    else:
        canvas.create_line(x_inicial, y_inicial, event.x, event.y, fill="YELLOW")
        # Coordenadas do ponto inicial e final da linha
        inicial_x = int(x_inicial)
        inicial_y = int(y_inicial)
        final_x = int(event.x)
        final_y = int(event.y)
        # Reiniciar as coordenadas
        x_inicial = None
        y_inicial = None



def desenhar_retangulo(event):
    global x_retangulo_inicial, y_retangulo_inicial
    global pontoinicial_x_retangulo, pontoinicial_y_retangulo, pontofinal_x_retangulo, pontofinal_y_retangulo
    global x_max, x_min, y_max, y_min
    if x_retangulo_inicial is None and y_retangulo_inicial is None:
        x_retangulo_inicial = event.x
        y_retangulo_inicial = event.y
    else:
        canvas.create_rectangle(x_retangulo_inicial, y_retangulo_inicial, event.x, event.y, outline="YELLOW")
        # Coordenadas do ponto inicial e final do retangulo
        pontoinicial_x_retangulo = int(x_retangulo_inicial)
        pontoinicial_y_retangulo = int(y_retangulo_inicial)
        pontofinal_x_retangulo = int(event.x)
        pontofinal_y_retangulo = int(event.y)

        x_max = pontoinicial_x_retangulo
        y_max = pontoinicial_y_retangulo
        x_min = pontofinal_x_retangulo
        y_min = pontofinal_y_retangulo
        #reiniciar as coordenadas
        x_retangulo_inicial = None
        y_retangulo_inicial = None

def adjust_zoom(zoom_level):
    #para o item nao ficar sumindo da tela quando da zoom, zoom nele baseado no seu centro
    items = canvas.find_all()
    mid_x = canvas.winfo_reqwidth() / 2
    mid_y = canvas.winfo_reqheight() / 2
    
    for item in items:
        coords = canvas.coords(item)
        new_coords = []
        for i in range(0, len(coords), 2):
            x = mid_x + (coords[i] - mid_x) * zoom_level
            y = mid_y + (coords[i + 1] - mid_y) * zoom_level
            new_coords.extend([x, y])
        canvas.coords(item, *new_coords)

def limpar_canvas():
    canvas.delete("all")

def zoom_in():
    zoom_level = 1.0
    zoom_level *= 1.1
    adjust_zoom(zoom_level)
        
def zoom_out():
    zoom_level = 1.0
    zoom_level /= 1.1
    adjust_zoom(zoom_level)

############################################# FUNÇÕES 2D #####################################################
def translation_button_canvas():
    translacao = entrada_texto_translacao.get()
    translacao = int(translacao)
    x1 = inicial_x + translacao
    y1 = inicial_y + translacao
    x2 = final_x + translacao
    y2 = final_y + translacao
    canvas.create_line(x1, y1, x2, y2, fill="WHITE")

def scale_button_canvas():
    escala = entrada_texto_escala.get()
    escala = int(escala)
    x1 = inicial_x * escala
    y1 = inicial_y * escala
    x2 = final_x * escala
    y2 = final_y * escala
    canvas.create_line(x1, y1, x2, y2, fill="WHITE")


def rotation_button_canvas():
    v=[]
    angulo = entrada_texto.get()
    angulo = int(angulo)
    tupla1= (inicial_x, inicial_y)
    tupla2= (final_x, final_y)
    x = list(tupla2)
    v.append(x)
    origin = list(tupla1)
    vetor_resultado = transformation.rotation(v, origin, angulo, cr=True)
    x2 = vetor_resultado[0]
    y2 = vetor_resultado[1]
    canvas.create_line(inicial_x, inicial_y, x2, y2, fill="WHITE")

def refletion_x_button_canvas():
    v=[]
    tupla2= (final_x, final_y)
    x = list(tupla2)
    v.append(x)
    vetor_resultado = transformation.reflectionx(v)
    x2 = vetor_resultado[0]
    y2 = vetor_resultado[1]
    canvas.create_line(inicial_x, inicial_y, x2, y2, fill="WHITE")

def refletion_y_button_canvas():
    v=[]
    tupla2= (final_x, final_y)
    x = list(tupla2)
    v.append(x)
    vetor_resultado = transformation.reflectiony(v)
    x2 = vetor_resultado[0]
    y2 = vetor_resultado[1]
    canvas.create_line(inicial_x, inicial_y, x2, y2, fill="WHITE")

def refletion_xy_button_canvas():
    v=[]
    tupla2= (final_x, final_y)
    x = list(tupla2)
    v.append(x)
    vetor_resultado = transformation.reflectionxy(v)
    x2 = vetor_resultado[0]
    y2 = vetor_resultado[1]
    canvas.create_line(inicial_x, inicial_y, x2, y2, fill="WHITE")

######################################## CHAMADA DOS ALGORÍTMOS #####################################################
def alg_dda():
    dda(inicial_x, inicial_y, final_x, final_y)

def alg_bres():
    bres(inicial_x, inicial_y, final_x, final_y)

def alg_cohen():
    cohen(inicial_x, inicial_y, final_x, final_y)

def alg_barsky():
    clipped_line = barsky(inicial_x,inicial_y, final_x, final_y)

    if clipped_line is not None:
        x1_clip, y1_clip, x2_clip, y2_clip = clipped_line
        # Plota a linha original
        canvas.create_line(inicial_x, inicial_y, final_x, final_y, fill = 'red',  width = 1)
        # Plota a linha clippada
        canvas.create_line(x1_clip, y1_clip, x2_clip, y2_clip, fill = 'YELLOW',  width = 1)
    else:
        # linha totalmente fora
        print('Linha totalmente fora da janela')


############################################# CONFIGS DA INTERFACE GRÁFICA #####################################################
# Criar a janela principal
root = tk.Tk()
root.title("TP 1 - CG - MARIA LUISA")

# Criar um canvas para desenho
canvas = tk.Canvas(root, width=700, height=800, bg="PURPLE")
canvas.grid(row=0, column=0, padx=10, pady=10, rowspan=9)

# Variáveis para armazenar as coordenadas dos pontos iniciais e finais usados ao longo do programa
pontoinicial_x_retangulo, pontoinicial_y_retangulo = None, None
pontofinal_x_retangulo, pontofinal_y_retangulo = None, None
x_inicial, y_inicial = None, None

# Associar evento de clique com as funções de desenho
canvas.bind("<Button-1>", desenhar_linha)
canvas.bind("<ButtonPress-3>", desenhar_retangulo)

texto_ao_lado_rotacao = tk.Label(root, text="GRAU DE ROTAÇÃO:")
texto_ao_lado_rotacao.grid(row=1, column=1, padx=10, pady=10)

# ROTACIONAR FUNCTIONS
entrada_texto = tk.Entry(root)
entrada_texto.grid(row=1, column=2, padx=10, pady=10)

rotation_button = tk.Button(root, text="ROTACIONAR", command=rotation_button_canvas)
rotation_button.grid(row=1, column=3, padx=10, pady=10)
rotation_button.config(width=20, height=2)

# ESCALA FUNCTIONS
texto_ao_lado_escala = tk.Label(root, text="FATOR DE ESCALA:")
texto_ao_lado_escala.grid(row=2, column=1, padx=10, pady=10)


entrada_texto_escala = tk.Entry(root)
entrada_texto_escala.grid(row=2, column=2, padx=10, pady=10)

scaling_button = tk.Button(root, text="ESCALAR", command=scale_button_canvas)
scaling_button.grid(row=2, column=3, padx=10, pady=10)
scaling_button.config(width=20, height=2)

# TRANSLAÇÃO FUNCTIONS 
texto_ao_lado_translacao = tk.Label(root, text="FATOR DE TRANSLAÇÃO:")
texto_ao_lado_translacao.grid(row=3, column=1, padx=10, pady=10)

entrada_texto_translacao = tk.Entry(root)
entrada_texto_translacao.grid(row=3, column=2, padx=10, pady=10)

translation_button = tk.Button(root, text="TRANSLADAR", command=translation_button_canvas)
translation_button.grid(row=3, column=3, padx=10, pady=10)
translation_button.config(width=20, height=2)

#REFLEXÃO FUNCTIONS

rotation_button = tk.Button(root, text="REFLEXÃO X", command=refletion_x_button_canvas)
rotation_button.grid(row=4, column=1, padx=10, pady=10)
rotation_button.config(width=20, height=2)

rotation_button = tk.Button(root, text="REFLEXÃO Y", command=refletion_y_button_canvas)
rotation_button.grid(row=4, column=2, padx=10, pady=10)
rotation_button.config(width=20, height=2)

rotation_button = tk.Button(root, text="REFLEXÃO XY", command=refletion_xy_button_canvas)
rotation_button.grid(row=4, column=3, padx=10, pady=10)
rotation_button.config(width=20, height=2)

# ALGORUTMOS FUNCTIONS
texto_ao_lado_ddabres = tk.Label(root, text="ALGORÍTMOS:")
texto_ao_lado_ddabres.grid(row=5, column=1, padx=10, pady=10)

rotation_button = tk.Button(root, text="ALG - DDA", command=alg_dda)
rotation_button.grid(row=5, column=2, padx=10, pady=10)
rotation_button.config(width=20, height=2)

rotation_button = tk.Button(root, text="ALG - BRES", command=alg_bres)
rotation_button.grid(row=5, column=3, padx=10, pady=10)
rotation_button.config(width=20, height=2)

# RECORTES FUNCTIONS
texto_ao_lado_recorte = tk.Label(root, text="ESCOLHAS DE RECORTE:")
texto_ao_lado_recorte.grid(row=6, column=1, padx=10, pady=10)

rotation_button = tk.Button(root, text="ALG - COHEN", command=alg_cohen)
rotation_button.grid(row=6, column=2, padx=10, pady=10)
rotation_button.config(width=20, height=2)

rotation_button = tk.Button(root, text="ALG - BARSKY", command=alg_barsky)
rotation_button.grid(row=6, column=3, padx=10, pady=10)
rotation_button.config(width=20, height=2)

# LIMPAR FUNCTION
limpar_button = tk.Button(root, text="LIMPAR CANVAS", command=limpar_canvas)
limpar_button.grid(row=7, column=2, padx=10, pady=10)
limpar_button.config(width=20, height=2)

#ZOOM FUNCTIONS
zoom_in_button = tk.Button(root, text="ZOOM IN", command=zoom_in)
zoom_in_button.grid(row=7, column=1, padx=10, pady=10)
zoom_in_button.config(width=20, height=2)
        
zoom_out_button = tk.Button(root, text="ZOOM OUT", command=zoom_out)
zoom_out_button.grid(row=7, column=3, padx=10, pady=10)
zoom_out_button.config(width=20, height=2)
        


################################################## LOOP DA JANELA DO CANVAS #####################################################
root.mainloop()
