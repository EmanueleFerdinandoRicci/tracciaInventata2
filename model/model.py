import copy

import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._costumers = []
        self._idMapC = {}
        self._bestPath = []
        self._bestScore = 0

    def getDateRange(self):
        return DAO.getDateRange()

    def getAllCountries(self):
        return DAO.getAllCountries()

    def getNodes(self):
        return self._costumers

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def buildGraph(self, date1, date2, country):
        self._graph.clear()
        self._costumers = DAO.getNodes(date1, date2, country)
        for c in self._costumers:
            self._idMapC[c.CustomerId] = c
        self._graph.add_nodes_from(self._costumers)

        allEdgesDiversi = DAO.getAllEdgesDiversi(date1, date2, country, self._idMapC)
        for e in allEdgesDiversi:
            pesoNuovo = float(e.p1) + float(e.p2)
            self._graph.add_edge(e.c1, e.c2, weight=pesoNuovo)

        allEdgesUguali = DAO.getAllEdgesUguali(date1, date2, country, self._idMapC)
        for e in allEdgesUguali:
            pesoNuovo = float(e.p1) + float(e.p2)
            self._graph.add_edge(e.c1, e.c2, weight=pesoNuovo)

    def getNodiConMaggiorNumArchiUscenti(self):
        nodi_con_peso_max = []
        for n in self._graph.nodes:
            score = 0
            for e in self._graph.out_edges(n, data=True):
                score += e[2]["weight"]
            nodi_con_peso_max.append((n, score))

        nodi_con_peso_max.sort(key=lambda x: x[1], reverse=True)
        return nodi_con_peso_max[0:5]

    def getBestPath(self, lun, start, end):
        self._bestPath = []
        self._bestScore = 0
        start_node = self._idMapC[int(start)]
        end_node = self._idMapC[int(end)]
        parziale = [start_node]
        self._ricorsione(parziale, int(lun), end_node)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, lun, end):
        if len(parziale) <= lun:
            if parziale[-1] == end and self._getScore(parziale) > self._bestScore:
                self._bestPath = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)

        for n in self._graph.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, lun, end)
                parziale.pop()

    def _getScore(self, parziale):
        score = 0
        for i in range(0, len(parziale) - 1):
            score += int(self._graph[parziale[i]][parziale[i + 1]]["weight"])
        return score