import ifcopenshell
import sys
import networkx as nx

fn = sys.argv[1]
ifc_file = ifcopenshell.open(fn)

G = nx.DiGraph()

def add_to_graph(existing, new, G):
    G.add_node(new.id(), **new.get_info())
    G.add_edge(existing.id(), new.id(), weight=7)

def is_entity_instance(val):
    return val.id() != 0 and isinstance(val, ifcopenshell.entity_instance)

for entity in ifc_file:
    # if entity.id() == 8128:
    # import pdb; pdb.set_trace()
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
  

import pdb; pdb.set_trace()

