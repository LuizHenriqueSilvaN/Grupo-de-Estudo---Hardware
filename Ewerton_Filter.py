#!/usr/bin/env python

import numpy as np
from PIL import Image as Im

img = 'Imagem.png'
im = Im.open(img)


def change(cor, mean_nbr, rng):  # pega as cores do pixel
    #if the pixel color is bigger than the range or smaller than 255-range return the medium color else
    #maintains the original value

    if cor > rng:
        return int(mean_nbr)
    elif cor < 255 - rng:
        return int(mean_nbr)
    else:
        return cor


def get_matriz_mean(im, i, j):  # pega a mediana dos valores das matrizes

    #Cada matriz é criada com o valores das cores dos visinhos posições i,j de cada pixel

    mtz_red = np.array(([im.getpixel((i - 1, j - 1))[0], im.getpixel((i - 1, j))[0], im.getpixel((1 - i, j + 1))[0]],
                        [im.getpixel((i, j - 1))[0], im.getpixel((i, j))[0], im.getpixel((i, j + 1))[0]],
                        [im.getpixel((i + 1, j - 1))[0], im.getpixel((i + 1, j))[0], im.getpixel((1 + i, j + 1))[0]]))

    mtz_green = np.array(([im.getpixel((i - 1, j - 1))[1], im.getpixel((i - 1, j))[1], im.getpixel((1 - i, j + 1))[1]],
                          [im.getpixel((i, j - 1))[1], im.getpixel((i, j))[1], im.getpixel((i, j + 1))[1]],
                          [im.getpixel((i + 1, j - 1))[1], im.getpixel((i + 1, j))[1], im.getpixel((1 + i, j + 1))[1]]))

    mtz_blue = np.array(([im.getpixel((i - 1, j - 1))[2], im.getpixel((i - 1, j))[2], im.getpixel((1 - i, j + 1))[2]],
                         [im.getpixel((i, j - 1))[2], im.getpixel((i, j))[2], im.getpixel((i, j + 1))[2]],
                         [im.getpixel((i + 1, j - 1))[2], im.getpixel((i + 1, j))[2], im.getpixel((1 + i, j + 1))[2]]))

    rmean = int(mtz_red.median())
    gmean = int(mtz_green.median())
    bmean = int(mtz_blue.median())

    changed_colors = [rmean, gmean, bmean]  #retorna uma lista de valores dos eixos

    return changed_colors


def check_inside_matrix(im, i, j, rng):

    mean_colors = get_matriz_mean(im, i, j)
    cor = {}
    color = []
    for m in range(i - 1, i + 2):
        for n in range(j - 1, j + 2):
            colors = im.getpixel((m, n))
            cor[(m, n)] = [change(colors[k], mean_colors[k], rng) for k in range(3)]
    return cor


# execute a função check_inside_matriz na imagem inteira
# aplicando com grupos de 9
new_colors = {}
for i in range(1, im.size[0] - 1, 3):
    for j in range(1, im.size[1] - 1, 3):
        cor = check_inside_matrix(im, i, j, 200)
        for c in cor.keys():
            new_colors[c] = [cor[c][0], cor[c][1], cor[c][2]]

        # retorna um dicionario com as posições e listas de cores

keys = [k for k in new_colors.keys()]  # get  the positions as a list
for k in keys:
    r, g, b = new_colors[(k)]  # get the values as a list
    im.putpixel((k), (r, g, b))  # muda os valores das cores dos pixels

im.save('imagem2')  # salva a imagem
im2 = Im.open('imagem2')  # abre uma imagem nova
im2.show()  # abre a imagem
