import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            min_albums = float(self._view.txtNumAlbumMin.value)
        except ValueError:
            self._view.create_alert("Inserire un numero di album valido")
            return

        if min_albums<0:
            self._view.create_alert("Inserire un numero di album valido")
            return

        self._model.load_artists_with_min_albums(min_albums)
        self._model.build_graph()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato: {len(self._model._graph.nodes)} nodi (artisti), {len(self._model._graph.edges)} archi")
        )

        self.populate_dropdown()

        self._view.ddArtist.disabled = False
        self._view.btnArtistsConnected.disabled = False

        self._view.txtMaxArtists.disabled = False
        self._view.txtMinDuration.disabled = False
        self._view.btnSearchArtists.disabled = False

        self._view.update_page()



    def populate_dropdown(self):
        for n in self._model._nodes:
            self._view.ddArtist.options.append(ft.dropdown.Option(text=n.name, key=n.id))


    def read_dropdown(self, e):
        idArtist = int(self._view.ddArtist.value)
        self._model.selected_artist =self._model._artists_dictionary[idArtist]
        print(f"Artista selezionato: {self._model.selected_artist}")

    def handle_connected_artists(self, e):
        u = self._model.selected_artist
        print(u)
        if u is None:
            self._view.create_alert("Seleziona un artista")

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Artisti direttamente collegati all'artista {self._model.selected_artist}"))
        neighbor_tuples = self._model.get_sorted_neighbors(u)
        for tuple in neighbor_tuples:
            self._view.txt_result.controls.append(ft.Text(f"{tuple[0]} - Numero di generi in comune: {tuple[1]}"))
        self._view.update_page()



    def handle_search_artists_path(self, e):

        try:
            max_artists = float(self._view.txtMaxArtists.value)
        except ValueError:
            self._view.create_alert("Inserire un numero di artisti valido")
            return

        if max_artists>self._model._graph.number_of_nodes() or max_artists<1:
            self._view.create_alert("Inserire un numero di artisti valido")
            return

        u = self._model.selected_artist
        if u is None:
            self._view.create_alert("Seleziona un artista")

        try:
            min_duration_minutes = float(self._view.txtMinDuration.value)
        except ValueError:
            self._view.create_alert("Inserire una durata valida")
            return

        if min_duration_minutes<0:
            self._view.create_alert("Inserire una durata valida")
            return

        min_duration_in_ms = float(min_duration_minutes)*1000*60

        max_path, max_weight = self._model.find_max_path(self._model.selected_artist, max_artists, min_duration_in_ms)

        if len(max_path)==0:
            self._view.create_alert("Artista non valido")
            return


        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino di peso massimo dall'artista {self._model.selected_artist}"))
        self._view.txt_result.controls.append(ft.Text(f"Lunghezza {len(max_path)}"))
        for v in max_path:
            self._view.txt_result.controls.append(ft.Text(f"{v}"))
        self._view.txt_result.controls.append(ft.Text(f"Peso massimo {max_weight}"))
        self._view.update_page()


