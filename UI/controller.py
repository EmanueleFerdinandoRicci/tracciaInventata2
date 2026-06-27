import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        genres = self._model.getAllGenres()
        for g in genres:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(key=str(g.GenreId), text=g.Name)
            )
        self._view.update_page()

    def handleCreaGrafo(self, e):
        genre_id = self._view._ddGenre.value

        if genre_id is None:
            self._view.create_alert("Seleziona un genere!")
            return
        self._model.buildGraph(genre_id)

        n_nodi, n_archi = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {n_archi}"))

        nodiArchi = self._model.getNodiConMaggiorNumArchiUscenti()
        self._view.txt_result.controls.append(
            ft.Text("Nodi con più archi:")
        )
        for p in nodiArchi:
            self._view.txt_result.controls.append(
                ft.Text(f"{p[0]} - score: {p[1]}")
            )
        self.fillDDTrack()
        self._view.update_page()

    def handleCercaCammino(self,e):
        if self._view._txtMin == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore numerico in lun", color="red")
            )
            self._view.update_page()
            return

        try:
            min = int(self._view._txtMin.value)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore numerico in max", color="red")
            )
            self._view.update_page()
            return

        path, score = self._model.getBestPath(min, self._view._ddTrackStart.value, self._view._ddTrackEnd.value)

        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(
                    f"Non ho trovato un cammino tra {self._view._ddTrackStart.value} e {self._view._ddTrackEnd.value}")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ecco il cammino migliore tra {self._view._ddTrackStart.value} e {self._view._ddTrackEnd.value}")
        )
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Il numero di nodi passati è {len(path)}")
        )
        for p in path:
            self._view.txt_result.controls.append(
                ft.Text(f"{p}")
            )
        self._view.txt_result.controls.append(
            ft.Text(f"Score: {score}")
        )
        self._view.update_page()

    def fillDDTrack(self):
        nodes = self._model.getNodes()
        for n in nodes:
            self._view._ddTrackStart.options.append(
                ft.dropdown.Option(key=str(n.TrackId), text=n.Name)
            )
            self._view._ddTrackEnd.options.append(
                ft.dropdown.Option(key=str(n.TrackId), text=n.Name)
            )
        self._view.update_page()