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
        return

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

        self._view._ddLun.disabled = False
        self._view.btnCerca.disabled = False

        self._view.update_page()
        # riempiamo la droplist

        lunValues= list(range(2,dimesioneConn))

        #for v in lunValues:
        #    self._view.ddLun.options.append(ft.dropdown.Option(v))
        #sostituito da questo metodo

        lunValuesDD= map(lambda x:ft.dropdown.Option(x), lunValues)
        self._view._ddLun.options = lunValuesDD
        self._view.update_page()
        return
        #fine parte

    def handleCerca(self,e):
        source = self._model.getNodeFromID(int(self._view._txtIdOggetto.value))

        lun = self._view._ddLun.value
        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("ATTENZIONE Inserisci un valore numerico", color="red"))
            self._view.update_page()
            return
        lunINT = int(lun)
        path, cost= self._model.getOptPath(source, lunINT)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"HO TROVATO UN CAMMINO CHE PARETE da {source}"
                                                      f"e ha un peso pari a {cost}",
                                                      color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"di seguiro i nodi che compongono il cammino;", color="green"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))

        self._view.update_page()


