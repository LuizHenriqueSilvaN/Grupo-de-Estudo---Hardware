#!/usr/bin/env python

import numpy as np
from PIL import Image as Im

img = 'Imagem.png'
im = Im.open(img)


def change(median_nbr):  # obtendo a cor do pixel, ainda tô trabalhando nessa função
    """Se a cor do pixel for maior que o limite de 255, retorna a cor media,
    else mantem o valor original da cor do pixel"""

    if > :
        return int(median_nbr)
    elif cor < 255 - rng:
        return int(median_nbr)
    else:
        return cor


def get_matriz_median(im, i, j):  #Obtem os valores das cores dos vizinhos do pixel i,j


    mtz_gray = np.array(([im.getpixel((i - 1, j - 1))[0], im.getpixel((i - 1, j))[0], im.getpixel((1 - i, j + 1))[0]],
                        [im.getpixel((i, j - 1))[0], im.getpixel((i, j))[0], im.getpixel((i, j + 1))[0]],
                        [im.getpixel((i + 1, j - 1))[0], im.getpixel((i + 1, j))[0], im.getpixel((1 + i, j + 1))[0]]))

    gmedian = int(mtz_gray.median())

    changed_colors = [gmedian]

    return changed_colors


def check_inside_matrix(im, i, j, rng):


    median_colors = get_matriz_median(im, i, j)
    cor = {}
    color = []
    for m in range(i - 1, i + 2):
        for n in range(j - 1, j + 2):
            colors = im.getpixel((m, n))
            cor[(m, n)] = [change(colors[k], median_colors[k], rng) for k in range(3)]
    return cor



new_colors = {}
for i in range(1, im.size[0] - 1, 3):
    for j in range(1, im.size[1] - 1, 3):
        cor = check_inside_matrix(im, i, j, 200)
        for c in cor.keys():
            new_colors[c] = [cor[c][0], cor[c][1], cor[c][2]]



keys = [k for k in new_colors.keys()]
for k in keys:
    r, g, b = new_colors[(k)]
    im.putpixel((k), (r, g, b))

im.save('Imagem.png')
im2 = Im.open('Imagem.png')
im2.show()

