import sys, os
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",  package])

sys.path.insert(0, '../.resources/')


# if not os.path.exists('./figure'):
#     os.makedir('./figure')

from py2neo import Graph
from datasci4health.graphdrawer.visgraph import draw
graph = Graph("bolt://127.0.0.1:7687")

# print("Clearing down the database")
# graph.delete_all()
# print("Number of nodes: {} ".format(len(graph.nodes)))
# print("Number of relationships: {} ".format(len(graph.nodes)))

from IPython import get_ipython
ipython = get_ipython()
ipython.magic('load_ext cypher')

install("calplot")
install("wordcloud")