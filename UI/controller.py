import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._ddRetailerValue = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillddAnno(self):
        for a in self._model.getAnni():
            self._view.ddAnno.options.append(ft.dropdown.Option(a))
        self._view.update_page()

    def fillddBrand(self):
        for b in self._model.getBrand():
            self._view.ddBrand.options.append(ft.dropdown.Option(b))
        self._view.update_page()

    def fillddRetailer(self):
        for r in self._model.getRetailers():
            self._view.ddRetailer.options.append(ft.dropdown.Option(key=r.Retailer_code, text=r.Retailer_name, data=r, on_click=self.read_retailer))

    def read_retailer(self, e):
        self._ddRetailerValue = e.control.data

    def handleTopVendite(self, e):
        self._view.txt_result.controls.clear()
        anno = self._view.ddAnno.value
        if anno is None or anno == "Nessun filtro":
            anno = None
        else:
            anno = int(anno)
        brand = self._view.ddBrand.value
        if brand == "" or brand == "Nessun filtro":
            brand = None
        if self._view.ddRetailer.value == "Nessun filtro":
            retailer = None
        elif self._ddRetailerValue is None:
            retailer = None
        else:
            retailer = self._ddRetailerValue.Retailer_code

        topVendite = self._model.getTopVendite(anno, brand, retailer)
        #print(topVendite)
        if len(topVendite) == 0:
            self._view.txt_result.controls.append(ft.Text("nessuna vendita con questi filtri"))
            self._view.update_page()
            return
        for v in topVendite:
            #self._view.txt_result.controls.append(ft.Text(v))
            self._view.txt_result.controls.append(ft.Text(f"Data: {v[0]}; Ricavo: {v[1]}; Retailer: {v[2]}; Product: {v[3]}"))
        self._view.update_page()
        return


    def handleAnalizzaVendite(self, e): #finire punto 3
        self._view.txt_result.controls.clear()
        anno = self._view.ddAnno.value
        if anno is None or anno == "Nessun filtro":
            anno = None
        else:
            anno = int(anno)
        brand = self._view.ddBrand.value
        if brand == "" or brand == "Nessun filtro":
            brand = None
        if self._view.ddRetailer.value == "Nessun filtro":
            retailer = None
        elif self._ddRetailerValue is None:
            retailer = None
        else:
            retailer = self._ddRetailerValue.Retailer_code

        analizzaVendite = self._model.getAnalizzaVendite(anno, brand, retailer)
        #print(analizzaVendite)
        if analizzaVendite[0][0] is None: #prendo nella lista il primo elemento (cioè una tupla) e prendo il primo elemento della tupla
            self._view.txt_result.controls.append(ft.Text("nessuna statistica trovata"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text("Statistiche vendite:"))
        for v in analizzaVendite:
            self._view.txt_result.controls.append(ft.Text(f"Giro d'affari: {v[0]}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero vendite: {v[1]}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero retailers coinvolti: {v[2]}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero prodotti coinvolti: {v[3]}"))
        self._view.update_page()
        return
