#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import os


INF = 9999999


def initialize():
    # Leitura e exibição do diretório de entrada
    caminhos = [os.path.join("entrada/", nome) for nome in os.listdir("entrada/")]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    for i in range(len(arquivos)):
        print i, " - ", arquivos[i]
    opcao = raw_input("\nInsira o número equivalente à opção do arquivo que deseja determinar como entrada: ")
    # Inicia a leitura do grafo
    grafo = nx.Graph()
    arq = open(arquivos[int(opcao)])
    linha = arq.readline()
    vertices, arestas = linha.split()            # Recebe a quantidade de vértices e arestas
    linha = arq.readline()                      # Primeira flag -1
    cont = 0
    # Recebendo a posição e peso dos vértices
    for linha in arq:
        if len(linha.split()) < 3:
            break
        else:
            grafo.add_node(cont)
            pos_x, pos_y, peso = linha.split()
            grafo.node[cont]['x'] = int(pos_x)
            grafo.node[cont]['y'] = int(pos_y)
            grafo.node[cont]['weight'] = int(peso)
            cont += 1
    # Recebendo as arestas e seus pesos
    for linha in arq:
        v1, v2, peso = linha.split()
        grafo.add_edge(int(v1), int(v2), weight = int(peso))
        grafo[int(v1)][int(v2)]['added'] = False

    arq.close()

    return grafo


def prim(grafo_residual, grafo):
    arvore = nx.Graph()
    arvore.add_node(0)
    v_add = [0]
    arestas_arvore = []
    custo = 0
    menor_aresta = []
    # Loop para construir a AGM
    while arvore.number_of_nodes() != grafo_residual.number_of_nodes():
        menor_custo = INF
        for vertice in v_add:
            vizinhos = list(grafo_residual.neighbors(vertice))
            for neighbor in range(grafo_residual.degree(vertice)):
                if grafo_residual[vertice][vizinhos[neighbor]]['weight'] < menor_custo:
                    menor_custo = grafo_residual[vertice][vizinhos[neighbor]]['weight']
                    menor_aresta = ([vertice, vizinhos[neighbor]])
        arestas_arvore.append([menor_aresta[0], menor_aresta[1]])
        v_add.append(menor_aresta[1])
        grafo_residual.remove_edge(menor_aresta[0], menor_aresta[1])
        grafo[menor_aresta[0]][menor_aresta[1]]['added'] = True
        custo += menor_custo
        arvore.add_node(menor_aresta[1], weight=grafo_residual.node[menor_aresta[1]]['weight'])

    # Cria a AGM com a lista de arestas obtidas
    
    for i in range(len(arestas_arvore)):
        arvore.add_edge(arestas_arvore[i][0], arestas_arvore[i][1])

    print "\nO custo da AGM gerada pelo algoritmo de Prim é %d.\n" % custo
    
    return custo, arestas_arvore, arvore, grafo


def calculates_cost(arvore, grafo):
    custo_parcial = 0;
    # Soma o custo dos vértices não-folhas da AGM
    for vertice in arvore.nodes():
        if arvore.degree(vertice) > 1:
            custo_parcial += grafo.node[vertice]['weight']
    # Soma o custo das arestas da AGM ao custo parcial anterior
    for aresta in arvore.edges():
        v1, v2 = aresta
        custo_parcial += grafo[v1][v2]['weight']

    return custo_parcial            


def refinement_heuristic(grafo, arvore, grafo_residual, custo):
    custo = calculates_cost(arvore, grafo)
    # Função que remolda a AGM de acordo com o a heurística
    for vertice in range(grafo_residual.number_of_nodes()):
        for neighbor in range(grafo_residual.degree(vertice)):
            #print "zecas: ", vertice, neighbor
            if (vertice != neighbor) and (grafo.has_edge(neighbor, vertice)):
                if (not grafo[neighbor][vertice]['added']):           
                        if grafo[vertice][neighbor]['added'] == False:
                            arvore.add_edge(vertice, neighbor)
                            grafo[vertice][neighbor]['added'] = True
                        # Verifica se a árvore possui ciclo com a nova aresta inserida
                        #print "par: ", vertice, neighbor
                        #print nx.cycle_basis(arvore)    
                        aux = nx.cycle_basis(arvore)
                        ciclo = [zip(nodes,(nodes[1:]+nodes[:1])) for nodes in aux]

                        for aresta in ciclo[0]:
                            if aresta != arvore[vertice][neighbor]:
                                arvore.remove_edge(aresta[0], aresta[1])
                                custo_parcial = calculates_cost(arvore, grafo)
                                if custo_parcial < custo:
                                    custo = custo_parcial                       # Altera o custo se a AGM encontrada possuir menor custo
                                else:
                                    arvore.add_edge(aresta[0], aresta[1])       # Devolve a aresta inserida, caso o custo encontrado for maior que o atual

    print "O custo da nova AGM gerada pela heurística de refinamento considerando o peso dos vértices é %d.\n" % custo

    return arvore, custo


def main():
    os.system('cls')
    grafo = initialize()
    grafo_residual = grafo.copy()
    custo, arestas_arvore, arvore, grafo = prim(grafo_residual, grafo)
    arvore, custo = refinement_heuristic(grafo, arvore, grafo_residual, custo)


if __name__ == '__main__':
      main()  