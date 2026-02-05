import copy

import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self._artists_dictionary = {}
        self._nodes = []
        self.selected_artist = None

        self._soluzioneMigliore = []
        self._pesoMigliore = 0

        self.load_all_artists()


    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        for a in self._artists_list:
            self._artists_dictionary[a.id] = a

    def load_artists_with_min_albums(self, min_albums):
        self._nodes = DAO.get_artists_with_min_albums(min_albums, self._artists_dictionary)

    def build_graph(self):
        self._graph.clear()
        self._graph.add_nodes_from(self._nodes)

        connections = DAO.get_edges_with_complex_query(self._artists_dictionary)
        for c in connections:
            if c.artist1 in self._graph and c.artist2 in self._graph:
                self._graph.add_edge(c.artist1, c.artist2, weight=c.n_genres)


    def get_sorted_neighbors(self, v0):
        neighbors = self._graph.neighbors(v0)
        neighbors_tuples = []
        for v in neighbors:
            neighbors_tuples.append((v, self._graph[v0][v]["weight"]))
            #neighbors_tuples.sort(key = lambda x: x[1], reverse = True)
        return neighbors_tuples


    def find_max_path(self, v0, max_connections, min_duration_in_ms):
        print(v0)
        print(min_duration_in_ms)

        valid_artists = DAO.get_artists_for_min_track_duration(min_duration_in_ms, self._artists_dictionary)
        print(f"Valid: {valid_artists}")

        self._soluzioneMigliore = []
        self._pesoMigliore = 0

        if v0 in valid_artists:
            parziale = [v0]
            self.ricorsione(parziale, max_connections, valid_artists)

        return self._soluzioneMigliore, self._pesoMigliore


    def ricorsione(self, parziale, max_artists, valid_artists):

        if len(parziale) == max_artists:
            if self.calcolaPeso(parziale) > self._pesoMigliore:
                self._pesoMigliore = self.calcolaPeso(parziale)
                self._soluzioneMigliore = copy.deepcopy(parziale)
            return

        # Altrimenti qui faccio ricorsione
        for v in self._graph.neighbors(parziale[-1]):
            if v not in parziale and v in valid_artists:
                parziale.append(v)
                self.ricorsione(parziale, max_artists, valid_artists)
                parziale.pop()

    def calcolaPeso(self, listaNodi):
        pesoTotale = 0
        for i in range(0, len(listaNodi) - 1):
            u = listaNodi[i]
            v = listaNodi[i + 1]
            pesoTotale += self._graph[u][v]["weight"]
        return pesoTotale