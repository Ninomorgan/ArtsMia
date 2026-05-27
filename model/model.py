import copy
from contextlib import nullcontext

import networkx as nx

from database.DAO import DAO
from model import artObject


class Model:
    def __init__(self):

        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO= {}
        for n in self._nodes:
            self._idMapAO[n.object_id]= n #associa all'id di un oggetto (chiave primaria) l'oggeto

       #esempio
        #self._idMapFermate = {} associo elemaenti
        #for f in self._fermate:
        #    self._idMapFermate[f.id_fermata] = f

       #RICORSIONE
        self._bestPath=[]
        self._optCost= 0

    def getOptPath(self, source, lun ):
        parziale=[source]

        for n in self._graph.neighbors(source):
            if n.classification == parziale[-1].classification:
                parziale.append(n)
                self._ricorsione(parziale,lun)
                parziale.pop() #back

        return self._optPath, self._optCost

    def _ricorsione(self,parziale,lun):
        if len(parziale) == lun:

            if self._costo(parziale) < self._optCost:
                self._optCosto = self._costo(parziale)

                self._optPath = copy.deepcopy(parziale)

            return

        #se arrvio
        for n in self._graph.neighbors(parziale[-1]):
            if parziale[-1].classification ==  n.classification :
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()  # back

    def _costo(self,path):
        #mi calcoal somma dei peis
        tot= 0
        for i in range (len(path)-1):
            tot+= self._graph[path[i]][path[i+1]]["weight"]
        return tot



    def buildGraph(self):
        #aggiungi nodi
        self._nodes = DAO.getAllNodes()
        self._graph.clear()
        #self._grafo.add_nodes_from(self._fermate) aggiungi i on
        self._graph.add_nodes_from(self._nodes)
        #self.addEdges3()
        #self.addEdges()
        self.addEdgesV2()


    #metodi get
    def getNumNodes(self):
        return len(self._graph.nodes)
    def getNumEdges(self):
        return len(self._graph.edges)

    # aggiungi gli archi
    def addEdges(self):
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getEdgePeso(u,v)
                if peso is not None:
                    self._graph.add_edge(u,v, weight=peso)

    def addEdgesV2(self):
        allEdges= DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1,e.o2, weight=e.peso)

    def getInfoConnessione(self, id_obj):
        #arriva un id:obj e veifica la compnente connessa
        #il cammino o connessione totale è melgio la ricerca dfsn

        ogg = self._idMapAO.get(id_obj)
        if ogg is  None:
            return None
        source = ogg

        #metodo 1
        dfs_tree=nx.dfs_tree(self._graph,source) # tutti i nodi
        print (len(dfs_tree.nodes())) #dimensione numero archi

        #metodo 2
        #esploro successori e predecessori
        pred= nx.dfs_predecessors(self._graph,source)
        print ("siza con pdf predecessors: ",len(pred.values())) #non avrò il valore source

        #metodo 3 SEMPRE UTILIZZATO
        #metodo node connectonr
        conn= nx.node_connected_component(self._graph,source)
        print ("size connesaa conontre coonetcred", len(conn))

        return len(conn)

    def hasNode(self,id_obj):
        return id_obj in self._idMapAO



    def getBFSNodesFromEdges(self, source): #source rappresenta il nodo di partenza

        pass

    def getDFSNodesFromEdges(self, source):
      pass

    def getNodeFromID(self, id_oggetto):
        return self._idMapAO[id_oggetto]

    @property
    def artObject(self):
        return artObject

    @property
    def grafo(self):
        return self._graph


