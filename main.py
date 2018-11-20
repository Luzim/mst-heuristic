#!/usr/bin/env python
# -*- coding: utf-8 -*-

from igraph import *


def initialize():
    grafo = Graph()
    arq = open('teste.dat')
    linha = arq.readline()
    vertices, arestas = linha.split()            # Recebe a quantidade de vértices e arestas
    grafo.add_vertices(int(vertices))
    linha = arq.readline()                      # Primeira flag -1
    cont = 0
    # Recebendo a posição e peso dos vértices
    for linha in arq:
        if len(linha.split()) < 3:
            break
        else:
            pos_x, pos_y, peso = linha.split()
            grafo.vs[cont]["x"] = int(pos_x)
            grafo.vs[cont]["y"] = int(pos_y)
            grafo.vs[cont]["weight"] = int(peso)
            cont += 1
    # Recebendo as arestas e seus pesos
    for linha in arq:
        v1, v2, peso = linha.split()
        grafo.add_edges([(int(v1), int(v2))])
        grafo.es[grafo.get_eid(int(v1), int(v2))]["weight"] = int(peso)

    arq.close()

    return grafo


def prim(grafo):
    arvore = Graph()
    arvore.add_vertex()
    v_add = [0]
    arestas_arvore = []
    custo = 0
    # Loop para construir a AGM
    while arvore.vcount() != grafo.vcount():
        aresta_peso = []
        for vertice in v_add:
            for aresta in grafo.incident(vertice):
                aresta_peso.append([aresta, grafo.es[aresta]["weight"]])
        aresta_peso.sort(key=lambda x: x[1])
        arestas_arvore.append([grafo.es[aresta_peso[0][0]].source, grafo.es[aresta_peso[0][0]].target])
        v_add.append(grafo.es[aresta_peso[0][0]].target)
        grafo.delete_edges(aresta_peso[0][0])
        custo += aresta_peso[0][1]
        arvore.add_vertex()
    # Cria a AGM com a lista de arestas obtidas
    for i in range(len(arestas_arvore)):
        arvore.add_edges([(arestas_arvore[i][0], arestas_arvore[i][1])])
        print arestas_arvore[i]

    print "O custo da AGM é ", custo


def main():
    grafo = initialize()
    prim(grafo)

if __name__ == '__main__':
      main()  