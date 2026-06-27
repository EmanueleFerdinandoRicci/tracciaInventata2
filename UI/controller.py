import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDNazione(self):
        nazioni = self._model.getAllCountries()
        for n in nazioni:
            self._view._ddNazione.options.append(
                ft.dropdown.Option(n)
            )
        self._view.update_page()

    def handleCreaGrafo(self, e):
        country = self._view._ddNazione.value
        date1 = self._view._dp1.value
        date2 = self._view._dp2.value
        self._model.buildGraph(date1, date2, country)
        n, a = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Date selezionate:")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Start date:{self._view._dp1.value.date()}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"End date:{self._view._dp2.value.date()}")
        )
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato:")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi:{n}, numero di archi:{a}")
        )
        nodiArchi = self._model.getNodiConMaggiorNumArchiUscenti()
        self._view.txt_result.controls.append(
            ft.Text("Nodi con più archi:")
        )
        for p in nodiArchi:
            self._view.txt_result.controls.append(
                ft.Text(f"{p[0]} - score: {p[1]}")
            )
        self.fillDDCustomer()
        self._view.update_page()

    def handleCercaCammino(self,e):
        if self._view._txtLun == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore numerico in lun", color="red")
            )
            self._view.update_page()
            return

        try:
            lun = int(self._view._txtLun.value)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore numerico in lun", color="red")
            )
            self._view.update_page()
            return

        path, score = self._model.getBestPath(lun, self._view._ddCustomerStart.value, self._view._ddCustomerEnd.value)

        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(
                    f"Non ho trovato un cammino tra {self._view._ddCustomerStart.value} e {self._view._ddCustomerEnd.value}")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ecco il cammino migliore tra {self._view._ddCustomerStart.value} e {self._view._ddCustomerEnd.value}")
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

    def fillDDCustomer(self):
        nodes = self._model.getNodes()
        for n in nodes:
            self._view._ddCustomerStart.options.append(
                ft.dropdown.Option(key=str(n.CustomerId), text= str(n.FirstName) + " " + str(n.LastName))
            )
            self._view._ddCustomerEnd.options.append(
                ft.dropdown.Option(key=str(n.CustomerId), text= str(n.FirstName) + " " + str(n.LastName))
            )
        self._view.update_page()

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)