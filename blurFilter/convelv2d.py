import numpy as np
import matplotlib.pyplot as plt 
import imageio

imName = input('Nome do Arquivo:')
im = imageio.imread(imName)

y = 99
x = 249

ksize = 3
kernel = np.array([[1,0,-1],[1,0,-1],[1,0,-1]]).astype('float').T

# Obter Região
region = im[y-ksize//2:y+ksize//2+1,x-ksize//2:x+ksize//2+1]

# Valor de Saída
output_value = 0
for i in range(ksize):
    for j in range(ksize):
        output_value += region[i,j]*kernel[i,j]

# Saída Para cada Píxel
im_out = np.zeros((im.shape))
for y in range(ksize//2, im.shape[0]-ksize//2):
    for x in range(ksize//2, im.shape[1]-ksize//2):
        region = im[y-ksize//2:y+ksize//2+1,x-ksize//2:x+ksize//2+1]
        for i in range(ksize):
            for j in range(ksize):
                im_out[y,x] += region[i,j]*kernel[i,j]

# Usando indexação do numpy
im_out = np.zeros((im.shape))
for y in range(ksize//2, im.shape[0]-ksize//2):
    for x in range(ksize//2, im.shape[1]-ksize//2):
        im_out[y,x] = (im[y-ksize//2:y+ksize//2+1,x-ksize//2:x+ksize//2+1]*kernel).sum()

plt.figure()
plt.imshow((im_out))
plt.show()