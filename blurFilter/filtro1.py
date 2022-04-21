import numpy as np
import matplotlib.pyplot as plt   #plt.imshow para mostar imagens na tela
import imageio                    # im.imread e im.imsave para carregar e salvar imagens em .png
from scipy.signal import convolve2d 


# cores básicas 
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)
black = (0,0,0)
white = (255,255,255)

# alguns filtros de convolução 
blurFilter = np.array(
    [
        [2, 4, 5, 4, 2],
        [4, 9, 12, 9, 4],
        [5, 12, 15, 12, 5],
        [4, 9, 12, 9, 4],
        [2, 4, 5, 4, 2]
    ]
)

# Filtro detector de borda
borderFilter = np.array(
     [
        [ 0, -8,  0],
        [-8, 16, -8],
        [ 0, -8,  0]
    ]
)

sobelFilter = np.array(
        [[47, 0,-47], 
         [162, 0, -162], 
         [47, 0, -47]]
)

# Desfoque de caixa ou Filtro Linear de Caixa; Filtro Passa Baixa de Raio 4, Matrix 9x9
# O parâmetro d deve ser preferencialmente ímpar; d >= 3
d = 9
boxBlurFilter = np.ones((d,d))

# PROGRAMA PRINCIPAL -----------------------------------------------------------------------

def main():
    # leitura dos parâmetros
    in_Name    = input('Nome do Arquivo de entrada:')
    out_Name   = 'saídaProvisória.jpg'#input('Nome do Arquivo na Saída:')
    threshold  = int(input('Limiar desejado (Número inteiro):'))
    

    # carrega a imagem de entrada
    in_imag = Image() # entrada
    in_imag.load(in_Name) # carregamento da entrada
    print('Imagem de Entrada:', in_Name)
    print('LIMIAR(threshold) = ',threshold)
    original_imag = imageio.imread(in_Name)
    
    # pré-processamento para segmentar as bordas
    gray = in_imag.toGray() ################ 1 - FEITO ########
    
    # imagem Binarizada
    rgbBin = in_imag.binarize(threshold)

    #Mostra Imagens
    legenda = ['Imagem original','Imagem com níveis de Cinza','Imagem Binarizada']
    showImages([original_imag,gray,rgbBin], legenda, (17,11), 3, 1)
    
    # normaliza os pesos dos filtros 
    blurKernel     = boxBlurFilter/int(np.abs(boxBlurFilter).sum()) ###################### borramento ###################
    sobelKernel    = sobelFilter/(np.abs(sobelFilter).sum())
    detectorBordas = borderFilter/(np.abs(borderFilter).sum())

    #borramento elimina as bordas que são menos intensas
    blurred = in_imag.filtre(gray, blurKernel) ###########   2 - FEITO    ########
    Sobel   = in_imag.filtre(gray, sobelKernel)
    bordas  = in_imag.filtre(gray, detectorBordas)
    legenda = ['Imagem Borrada', 'Filtro Sobel',' Detector de Bordas']
    showImages([blurred, Sobel, bordas], legenda, (17,11), 3, 1)

    edges = blurred.segmentEdges(threshold) ######    3 - FALTA FAZER   #####
    print('Imagem das bordas Segmentadas: ')
    edges.show()

    #realce das bordas na imagem original
    painted = in_imag.paint(black, edges) ######   4 - FALTA FAZER   ###########
    print('Imagens com bordas realçadas')
    painted.show()

    # Salvar o resultado
    painted.saved(out_Name)
    print('A imagem realçada foi salva em', out_Name)


# CLASSE IMAGEM ------------------------------------------------------------------------

class Image:
    
    #-----------------------------------------------------------------------------------------------------------
    
    def _init_(self, array = None): 
        #Construtor de um objeto Imagem, que recebe um array com o conteúdo da imagem.
        if array is not None:
            self.data = np.copy(array)
        else:
            self.data = None 

    def getpixel(self, lin, col): 
        # (self, inteiro, inteiro) >>> retorna o valor do pixel na posição (lin, col)
        return self.data[lin,col]

    def setpixel(self, lin, col, valor): 
        # (self, inteiro, inteiro) >>> atribui valor ao pixel na posição (lin, col)
        self.data[lin, col] = valor

    def load(self, file): 
        # (Str) >>> None; arquivo extensão .png
        self.data = imageio.imread(file)

    def saved(self, file):
         # (Str) >>> None; Aqui também será salvo em extensão .png
        imageio.imsave(file,self.data)

    #-----------------------------------------------------------------------------------------------------------
    
    def toGray(self): 

        rgb = self.data
        r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
        gray = (0.2126 * r) + (0.7152 * g) + (0.0722 * b)

        return gray
        
    #-----------------------------------------------------------------------------------------------------------
    
    def binarize(self, threshold): 
        # (self, inteiro) >>> retorna uma imagem convertida para binário. 
        rgbBin = self.data
        for row in range(0, rgbBin.shape[0]):
            for col in range(0, rgbBin.shape[1]):
                if (rgbBin[row][col] <= threshold).any():
                    rgbBin[row,col] = (0,0,0)
                else:
                    rgbBin[row,col] = (255,255,255)
                
        return rgbBin
    
    #-----------------------------------------------------------------------------------------------------------
    
    def filtre(self,gray, filtro): 
        # (self, ndarray) >>> Imagem Cinza. Este Método retorna uma imagem da convolução de Self com o filtro.
        # Como os valores do filtro são reais, os valores da imagem resultado também serão reais.
        A = gray
        B = filtro
        imFiltered = convolve2d( A, B, mode='valid')
        return imFiltered

    #-----------------------------------------------------------------------------------------------------------    
    
    #def paint(self, color, mask): 
        # (self, cor, Imagem) >>> Imagem; Recebe uma imagem binária e pinta os pixels de self correspondentes aos pixels Trfue da mascara com a cor.
        # Obeservar  que a cor  deve ter o mesmo numero de bits da imagem em self.
    
    #-----------------------------------------------------------------------------------------------------------
    
    #def segmentEdges(self, threshold): 
        """Assumir que self é uma imagem com níveis de cinza. 
        O método calcula as matrizes gradiente gH e gV
        utilizando os filtros Sh e Sv de Sobel, e retorna uma imagem 
        binária com as mesmas dimensões da imagem cinza self, 
        onde os valores True satisfazem:
        sqrt(gH*gH + gV*gV) > limiar.
        Pixels que não satisfazem a condições devem receber False.

        Importante: como o limiar é um número entre 0 e 255,
        antes de aplicar o limiar (comparar), a imagem correspondente ao 
        módulo do gradiente (sqrt(gH*gH + gV*gV)) deve ser normalizada para
        o intervalo 0 a 255."""

#-----------------------------------------------------------------------------------------------------------

# Métodos apenas para exibição de imagens

def showImage(imag, title, size):
    fig, axis = plt.subplots(figsize = size)

    axis.imshow(imag,'gray')
    axis.set_title(title, fontdict = {'fontsize':22,'fontweight':'medium'})
    plt.show()

def showImages(imagArray,titleArray, size, x,y):
    if(x<1 | y<1):
        print('ERRO: x e y não podem ser zero ou abaixo de zero.')
        return
    elif(x==1 & y==1):
        showImage(imagArray, titleArray)
    elif(x==1):
        fig, axis = pltsubplots(y, figsize = size)
        yId = 0
        for imag in imagArray:
            axis[yId].imshow(imag,'gray')
            axis[yId].set_anchor('NW')
            axis[yId].set_title(titleArray[yId], fontdict = {'fontsize': 18, 'fontweight': 'medium'}, pad = 10)

            yId += 1

    elif(y ==1):
        fig, axis = plt.subplots(1,x,figsize = size)
        fig.suptitle(titleArray)
        xId = 0
        for imag in imagArray:
            axis[xId].imshow(imag,'gray')
            axis[xId].set_anchor('NW')
            axis[xId].set_title(titleArray[xId], fontdict = {'fontsize': 18, 'fontweight': 'medium'}, pad = 10)

            xId += 1

    else:
        fig, axis = plt.subplots(y,x,figsize =size)
        xId, yId, titleId = (0,0,0)
        for imag in imagArray:
            axis[yId,xId].imshow(imag,'gray')
            axis[yId,xId].set_anchor('NW')
            axis[yId,xId].set_title(titleArray[titleId], fontdict = {'fontsize': 18, 'fontweight': 'medium'}, pad = 10)
            if len(titleArray[titleId])==0:
                axis[yId,xId].axis('off')

            titleId += 1
            xId += 1
            if xId == x:
                xId = 0
                yId += 1
    plt.show()

#Execução da main
main()