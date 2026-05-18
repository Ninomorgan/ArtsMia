import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grado creato"))
        self._view.txt_result.controls.append(ft.Text(f"il grafo creato contiene {self._model.getNumNodes()} node "
                                                      f"e {self._model.getNumEdges()} archi"))
        self._view.update_page()



    def handleCompConnessa(self,e):
        txtId_obg = self._view._txtIdOggetto.value

        if txtId_obg == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserisci un valore", color="red"))
            self._view.update_page()
            return

        try:
            id_ogg= int(txtId_obg)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserisci un valore numerico valido", color="red"))
            self._view.update_page()

        if not self._model.hasNode(id_ogg):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione l'id inserito non esiste", color="red"))
            self._view.update_page()
            return

        dimesioneConn= self._model.getInfoConnessione(id_ogg)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"la componente connessa dell'oggetto {id_ogg} è composta da {dimesioneConn}", color="green"))
        self._view.update_page()
        return
        #fine parte 1