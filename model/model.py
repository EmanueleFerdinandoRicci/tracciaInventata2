import copy

import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._tracks = []
        self._graph = nx.Graph()
        self._idMapT = {}
        self._bestPath = []
        self._bestScore = 0

    def getDateRange(self):
        return DAO.getDateRange()

    def getAllGenres(self):
        return DAO.getAllGenres()

    def getNodes(self):
        return self._tracks

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def buildGraph(self, genreId):
        self._graph.clear()
        self._tracks = DAO.getAllNodes(genreId)
        for t in self._tracks:
            self._idMapT[t.TrackId] = t
        self._graph.add_nodes_from(self._tracks)

        allEdges = DAO.getAllEdges(genreId,self._idMapT)
        for e in allEdges:
            self._graph.add_edge(e.t1, e.t2, weight=e.peso)

    def getNodiConMaggiorNumArchiUscenti(self):
        nodi_con_peso_max = []
        for n in self._graph.nodes:
            score = 0
            for e in self._graph.neighbors(n):
                score += int(self._graph[n][e]['weight'])
            nodi_con_peso_max.append((n, score))

        nodi_con_peso_max.sort(key=lambda x: x[1], reverse=True)
        return nodi_con_peso_max[0:5]

    def getBestPath(self, massimo, start, end):
        self._bestPath = []
        self._bestScore = 0
        start_node = self._idMapT[int(start)]
        end_node = self._idMapT[int(end)]
        parziale = [start_node]
        self._ricorsione(parziale,massimo,end_node)
        return self._bestPath,self._bestScore

    def _ricorsione(self, parziale, massimo, end):
        if parziale[-1] == end:
            if len(self._bestPath) == 0 or len(parziale) < len(self._bestPath):
                self._bestPath = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)
            return

        if len(self._bestPath) > 0 and len(parziale) >= len(self._bestPath):
            return

        ultimo = parziale[-1]
        vicini = list(self._graph.neighbors(ultimo))
        for vicino in vicini:
            if vicino not in parziale:
                peso_arco = int(self._graph[ultimo][vicino]['weight'])
                if peso_arco > massimo:
                    parziale.append(vicino)
                    self._ricorsione(parziale, massimo, end)
                    parziale.pop()

    def _getScore(self,parziale):
        score = 0
        for i in range(0,len(parziale)-1):
            score += int(self._graph[parziale[i]][parziale[i+1]]["weight"])
        return score