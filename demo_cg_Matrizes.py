# -*- coding: utf-8 -*-
from graphics import *
import numpy as np
import sys, math, time

class Vertice:
    def __init__(self, coordenadas):
        self.x = coordenadas[0]
        self.y = coordenadas[1]
        self.z = coordenadas[2]

class Aresta:
    def __init__(self, ini, fim):
        self.ini = ini
        self.fim = fim

class Solido:
    def __init__(self):
        self.vertices = []
        self.vertices = np.zeros((0,4))
        self.arestas = []

    def addVertices(self, vertLista):
        coluna_uns = np.ones((len(vertLista), 1))
        uns_added = np.hstack((vertLista, coluna_uns))
        self.vertices = np.vstack((self.vertices, uns_added))

    def addArestas(self, arestLista):
        self.arestas = arestLista

    def outVertices(self):
        print "\n --- Vertices --- "
        for i, (x, y, z, _) in enumerate(self.vertices):
            print " %d: (%.2f, %.2f, %.2f)" % (i, x, y, z)

    def outArestas(self):
        print "\n --- Arestas --- "
        for i, (vertice1, vertice2) in enumerate(self.arestas):
            print "%d: %d -> %d" % (i, vertice1, vertice2)

    def rotZ(self, angulo):
        c = np.cos(angulo)
        s = np.sin(angulo)
        rZ = np.array([[c, -s, 0, 0],
                       [s, c, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

        centro = self.getCentro()
        self.translacao(-centro[0], -centro[1], -centro[2])
        self.vertices = self.vertices.transpose()
        self.vertices = np.dot(rZ, self.vertices)
        self.vertices = self.vertices.transpose()
        self.translacao(centro[0], centro[1], centro[2])

    def rotY(self, radianos):
        c = np.cos(radianos)
        s = np.sin(radianos)
        rY = np.array([[c, 0, -s, 0],
                       [0, 1, 0, 0],
                       [s, 0, c, 0],
                       [0, 0, 0, 1]])

        centro = self.getCentro()
        self.translacao(-centro[0], -centro[1], -centro[2])
        self.vertices = self.vertices.transpose()
        self.vertices = np.dot(rY, self.vertices)
        self.vertices = self.vertices.transpose()
        self.translacao(centro[0], centro[1], centro[2])

    def rotX(self, radianos):
        c = np.cos(radianos)
        s = np.sin(radianos)
        rX = np.array([[1, 0, 0, 0],
                       [0, c, -s, 0],
                       [0, s, c, 0],
                       [0, 0, 0, 1]])

        centro = self.getCentro()
        self.translacao(-centro[0], -centro[1], -centro[2])
        self.vertices = self.vertices.transpose()
        self.vertices = np.dot(rX, self.vertices)
        self.vertices = self.vertices.transpose()
        self.translacao(centro[0], centro[1], centro[2])

    def translacao(self, dx=0, dy=0, dz=0):
        t = np.array([[1, 0, 0, dx],
                      [0, 1, 0, dy],
                      [0, 0, 1, dz],
                      [0, 0, 0, 1]])
        self.vertices = self.vertices.transpose()
        self.vertices = np.dot(t, self.vertices)
        self.vertices = self.vertices.transpose()

    def escala(self, sx=0, sy=0, sz=0):

        e = np.array([[sx, 0, 0, 0],
                      [0, sy, 0, 0],
                      [0, 0, sz, 0],
                      [0, 0, 0,  1]])
        centro = self.getCentro()
        self.translacao(-centro[0], -centro[1], -centro[2])
        self.vertices = np.dot(self.vertices, e)
        self.translacao(centro[0], centro[1], centro[2])

    def getCentro(self):
        n_vertices = len(self.vertices)
        vert = []
        vert = [sum(self.vertices[:,i])/n_vertices for i in range(4)]
        return(vert[0], vert[1], vert[2])

    def desenha(self, grafico):
        '''
        for vertice in self.vertices:
            c = Circle(Point(int(vertice[0]), int(vertice[1])), 2)
            time.sleep(.1)
            c.draw(grafico)
            update(60)
    	'''

        for n1,n2 in self.arestas:
            ptI = Point(int(self.vertices[n1][0]), int(self.vertices[n1][1]))
            ptF = Point(int(self.vertices[n2][0]), int(self.vertices[n2][1]))
            cI = Circle(ptI, 3)
            cF = Circle(ptF, 3)
            cI.setFill("yellow")
            cI.draw(grafico)
            time.sleep(.2)
            update(60)
            ln = Line(ptI, ptF)
            ln.draw(grafico)
            time.sleep(.2)
            update(60)
            cF.setFill("red")
            cF.draw(grafico)
            time.sleep(.2)
            update(60)
            cF.setFill("yellow")
            time.sleep(.2)
            update(60)
    
    def pinta(self, faces, window):
        cores = ["green", "blue", "grey", "orange", "purple"]
        j = 0
        for face in faces:
            pts = []
            for i in range(len(face)):
               pt = Point(self.vertices[face[i]][0], self.vertices[face[i]][1]) 
               pts.append(pt)
            p = Polygon(pts)
            p.setFill(cores[j])
            p.setOutline("black")
            p.draw(window)
            time.sleep(.4)
            update(60)
            if (j > 3):
                j = 0
            j += 1
    
    def pintaPontos(self, window):
        i = 40
        pontos = []
        for vertice in self.vertices:
            s = ' ,'.join(str(e) for e in vertice)
            ponto = Point(150,i)
            pontos.append(ponto)
            txt = Text(ponto,s)
            txt.setFace("arial")
            txt.setStyle("bold")
            txt.draw(window)
            i += 40
        return pontos

def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

def drawAll(win):
    for item in win.items[:]:
        item.draw(win)
    win.update()

def main():
    w,h = 700,700
    janela = GraphWin("janela", w, h, autoflush=False)
    janela.setBackground(color_rgb(255,255,255))
    cx,cy = w//2, h//2
   
    hexagonVertices = [[25,400,20],
                      [30,410,20],
                      [40,410,20],
                      [45,400,20],
                      [40,390,20],
                      [30,390,20],
                      [25,400,40],
                      [30,410,40],
                      [40,410,40],
                      [45,400,40],
                      [40,390,40],
                      [30,390,40]]
                      
    hexagonArestas = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,0],[0,6],[1,7],[2,8],[3,9],[4,10],[5,11],[6,7],[7,8],[8,9],[9,10],[10,11],[11,6]]
    hexagonoFaces1 = [[6,7,8,9,10,11], [1,7,8,2], [2,8,9,3], [3,9,10,4], [4,5,11,10], [5,0,6,11], [0,6,7,1], [0,1,2,3,4,5]]

    hexagono = Solido()
    hexagono.addVertices(np.array(hexagonVertices))
    hexagono.addArestas(hexagonArestas)
    #hexagono.outVertices()
    #hexagono.outArestas()

    hexagono.escala(6,6,6)
    hexagono.translacao(450,-150,0)
    hexagono.rotX(0.5)
    hexagono.rotY(0.5)
    
    pontos = hexagono.pintaPontos(janela)
    hexagono.desenha(janela)
    hexagono.pinta(hexagonoFaces1, janela)
    update(60)
   
    '''
    while True:
       clk = janela.checkMouse()
       for i in range(12):
           if(clk == pontos[i]):
               pt = Point(pontos[i][0], pontos[i][1])
               pt.setFill("red")
               pt.draw(janela)
               update(60)
               pt.undraw()

        while True:
            time.sleep(.05)
            clear(janela)
            hexagono.rotX(0.5)
            hexagono.rotY(0.5)
            hexagono.rotZ(0.5)
            drawAll(janela)
            time.sleep(0.5)
            update(60)
    '''

    janela.getMouse()
    janela.close()
main()
