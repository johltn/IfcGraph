import ifcopenshell
import sys, time
import networkx as nx
import matplotlib.pyplot as plt
import datetime



def add_to_graph(existing, new, G):
    G.add_node(new.id(), **new.get_info())
    G.add_edge(existing.id(), new.id(), weight=7)

def is_entity_instance(val):
    return val.id() != 0 and isinstance(val, ifcopenshell.entity_instance)


def create_graph(ifc_file):
    G = nx.DiGraph()
    for entity in ifc_file:
        info = entity.get_info()
        G.add_node(info['id'], **info)
        for attribute_value in info.values():
            if isinstance(attribute_value, ifcopenshell.entity_instance):
                if attribute_value.id() != 0:
                    add_to_graph(entity,attribute_value, G)
            elif isinstance(attribute_value, tuple):
                for element in attribute_value:
                    if isinstance(element, ifcopenshell.entity_instance):
                        if element.id() != 0:
                            add_to_graph(entity,element, G)
    return G



if __name__ == "__main__":

    fn = sys.argv[1]
    ifc_file = ifcopenshell.open(fn)

    start_time = time.time()
    G = create_graph(ifc_file)

    l = list(nx.topological_sort(G))
    
    print("--- %s seconds ---" % (time.time() - start_time))

    pos = nx.spring_layout(G, k=0.8, iterations=60)  # positions for all nodes
    nc = nx.draw_networkx_nodes(G, pos,nodelist=G.nodes,node_size=50)
    nc = nx.draw_networkx_edges(G, pos,nodelist=G.edges,node_size=50)
  
    plt.axis("off")
    plt.show()