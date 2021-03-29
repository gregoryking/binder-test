from IPython.display import IFrame
import json
import uuid
import os
import colorsys
from py2neo import Graph

def vis_network(nodes, edges, physics=True):
    html = """
    <html>
    <head>
      <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
      <meta content="utf-8" http-equiv="encoding">    
      <script type="text/javascript" src="https://thedatasociety.github.io/resources/purl/lab-neo4j/graphdrawer/vis.js"></script>
      <link   type="text/css"       href="https://thedatasociety.github.io/resources/purl/lab-neo4j/graphdrawer/vis.css" rel="stylesheet" >
    </head>
    <body>

    <div id="{id}"></div>

    <script type="text/javascript">
      var nodes = {nodes};
      var edges = {edges};

      var container = document.getElementById("{id}");

      var data = {{
        nodes: nodes,
        edges: edges
      }};

      var options = {{
          nodes: {{
              shape: 'dot',
              size: 25,
              font: {{
                  size: 14
              }}
          }},
          edges: {{
              font: {{
                  size: 14,
                  align: 'middle'
              }},
              color: 'gray',
              arrows: {{
                  to: {{enabled: true, scaleFactor: 0.5}}
              }},
              smooth: {{enabled: false}}
          }},
          physics: {{
              enabled: {physics}
          }}
      }};

      var network = new vis.Network(container, data, options);

    </script>
    </body>
    </html>
    """

    unique_id = str(uuid.uuid4())
    html = html.format(id=unique_id, nodes=json.dumps(nodes), edges=json.dumps(edges), physics=json.dumps(physics))

    try:
        os.makedirs('graphs')
    except OSError as e:
        pass 
    
    filename = "graphs/graph-{}.html".format(unique_id)

    file = open(filename, "w+")
    file.write(html)
    file.close()

    return IFrame(filename, width="100%", height="800")

# def draw(graph, options, physics=False, limit=100):
#     # The options argument should be a dictionary of node labels and property keys; it determines which property
#     # is displayed for the node label. For example, in the movie graph, options = {"Movie": "title", "Person": "name"}.
#     # Omitting a node label from the options dict will leave the node unlabeled in the visualization.
#     # Setting physics = True makes the nodes bounce around when you touch them!
#     query = """
#     MATCH (n)
#     WITH n, rand() AS random
#     ORDER BY random
#     LIMIT {limit}
#     OPTIONAL MATCH (n)-[r]->(m)
#     RETURN n AS source_node,
#            id(n) AS source_id,
#            r,
#            m AS target_node,
#            id(m) AS target_id
#     """

#     data = graph.run(query, limit=limit)

#     nodes = []
#     edges = []

#     def get_vis_info(node, id):
#         node_label = list(node.labels)[0]
#         prop_key = options.get(node_label)
#         vis_label = node['label']
        
#         if node['label'] == None:

#             return {
#                     "id": id, 
#                     "label": "\n{}".format(node.labels), 
#                     "group": node_label, "title": "Type(s) = {} <br/> Properties = ".format(node_label)+repr(dict(node))
#                    }
#         else:

#             return {
#                     "id": id, 
#                     "label": "\n\n{} ({})".format(node.labels,node['label']), 
#                     "group": node_label, "title": "Type(s) = {} <br/> Properties = ".format(node_label)+repr(dict(node))
#                    }

    
#     for row in data:
#         source_node = row[0]
#         source_id = row[1]
#         rel = row[2]
#         target_node = row[3]
#         target_id = row[4]

#         source_info = get_vis_info(source_node, source_id)

#         if source_info not in nodes:
#             nodes.append(source_info)

#         if rel is not None:
#             target_info = get_vis_info(target_node, target_id)

#             if target_info not in nodes:
#                 nodes.append(target_info)

#             edges.append({"from": source_info["id"], "to": target_info["id"], "label": "{}".format(type(rel).__name__)})

#     return vis_network(nodes, edges, physics=physics)

def draw(result, options, physics=False, limit=100):
    # The options argument should be a dictionary of node labels and property keys; it determines which property
    # is displayed for the node label. For example, in the movie graph, options = {"Movie": "title", "Person": "name"}.
    # Omitting a node label from the options dict will leave the node unlabeled in the visualization.
    # Setting physics = True makes the nodes bounce around when you touch them!

    sub_graph = result.get_graph()
    nx_nodes = sub_graph.nodes
    nx_edges = sub_graph.edges

    graph = Graph("bolt://127.0.0.1:7687")
    data = graph.run("CALL db.labels()").to_data_frame()
#     N = len(data)
#     HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
#     RGB_tuples = list(map(lambda x: "rgb" + str(tuple([int(255 * val) for val in colorsys.hsv_to_rgb(*x)])), HSV_tuples))
    RGB_tuples = ("rgb(0, 158, 73)","rgb(255, 140, 0)","rgb(232, 17, 35)","rgb(236, 0, 140)","rgb(104, 33, 122)","rgb(0, 24, 143)","rgb(0, 188, 242)","rgb(0, 178, 148)","rgb(186, 216, 10)","rgb(255, 241, 0)")
    labels = data['label'].to_list()
    labels_to_rgb = {labels[i]: RGB_tuples[i] for i in range(len(labels))}
    
    def node_format(id):
        node_labels = nx_nodes[id]['labels']
        if node_labels == None:
            return {
                    "id": id, 
                    "label": "None"
                   }
        else:
            label = node_labels[0]
            prop_key = options.get(node_labels[0])
            displayLabel = label if prop_key == None else str(nx_nodes[id][prop_key])
            displayLabel = (displayLabel[:20] + '..') if len(displayLabel) > 10 else displayLabel
            return {
                    "id": id, 
                    "label": displayLabel,
                    "color": labels_to_rgb[label]
                   }
        
    def edge_format(edge):
        return {"from": edge[0], "to": edge[1], "label": edge[2]}
    
    nodes = list(map(node_format, nx_nodes))
    edges = list(map(edge_format, nx_edges))

    return vis_network(nodes, edges, physics=physics)


