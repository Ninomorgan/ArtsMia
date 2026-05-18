from database.DAO import DAO
from model.model import Model

mdl= Model()
allObject=DAO.getAllNodes()
mdl.buildGraph()
#print(f"il grafo coniente {mdl.getNumNdes()} nodi - e {mdl.getNumEdges()} archi")

#print(len(allObject))

mdl.getInfoConnessione(1224)