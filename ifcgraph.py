import ifcopenshell
import sys, time
import networkx as nx
import matplotlib.pyplot as plt
import datetime
import math

class fuzzy_dict(object):
    def __init__(self, d, eps=1e-5, guid=None):
        self.d = d
        self.eps = eps
        self.guid = guid
        
        mod = - int(round(math.log10(eps * 100)))
        def c(v):
            if isinstance(v, float):
                # print "round(%r, %r) = %r" % (v, mod, round(v, mod))
                return round(v, mod)
            elif isinstance(v, dict):
                return tuple(sorted((k,c(v)) for k, v in v.items()))
            elif isinstance(v, (tuple, list)):
                return type(v)(map(c, v))
            else:
                return v
                
        self.h = hash(c(self.d))
        
    def __hash__(self):
        return self.h
         
    def __eq__(self, other):
    
        def eq(v1, v2):
            if type(v1) != type(v2):
                return False
            if isinstance(v1, float):
                if abs(v1 - v2) > self.eps: return False
            elif isinstance(v1, dict):
                if not (fuzzy_dict(v1, eps=self.eps) == fuzzy_dict(v2, eps=self.eps)): return False
            elif isinstance(v1, (tuple, list)):
                if len(v1) != len(v2): return False
                for a, b in zip(v1, v2):
                    if not eq(a, b): return False
            else:
                if v1 != v2: return False
            return True
        
        if set(self.d.keys()) != set(other.d.keys()): return
        
        for v1, v2 in ((self.d[k], other.d[k]) for k in self.d):
            if not eq(v1, v2): return False
            
        return True


def add_to_graph(existing, new, G):
    G.add_node(new.id(), **new.get_info())
    G.add_edge(existing.id(), new.id(), weight=7)

def is_entity_instance(val):
    return val.id() != 0 and isinstance(val, ifcopenshell.entity_instance)

def remove_id_key(d):
    new_d = {}
    for k, v in d.items():
        if k != 'id':
            new_d[k] = v

    return new_d
    
def create_graph(ifc_file):
    G = nx.DiGraph()
    for entity in ifc_file:
        info = entity.get_info()
        G.add_node(info['id'], **info)

        # import pdb; pdb.set_trace()
       
        for attr_name, attr_val in info.items():
            if isinstance(attr_val, ifcopenshell.entity_instance):
                if attr_val.id() != 0:
                    add_to_graph(entity,attr_val, G)
            elif isinstance(attr_val, tuple):
                for element in attr_val:
                    if isinstance(element, ifcopenshell.entity_instance):
                        if element.id() != 0:
                            add_to_graph(entity,element, G)
    return G

def get_hashes():
    hashes = set()
    for k,v in G.nodes.items():
        attrs = fuzzy_dict(remove_id_key(v))
        # print(attrs)
        hashes.add(attrs)
        return hashes

def get_subgraph(node, G):
    neighbors = nx.all_neighbors(G,node) 
    sg = nx.DiGraph()
    sg.add_node(node, **G.nodes[node])

    for n in neighbors:
        print(n)
        # import pdb; pdb.set_trace()
        print(G.has_edge(node, n))
        sg.add_node(n,**G.nodes[n] )
        if G.has_edge(node, n):
            sg.add_edge(node, n)
        else:
            
            sg.add_edge(n, node)
    return sg

def draw_graph(G):
    # import pdb; pdb.set_trace()
    labels = {}
    for n in G.nodes.values():
        print(n)
        labels[n['id']] = "#" + str(n['id'])+"\n" + n['type']
 
    pos = nx.spring_layout(G, k=0.8, iterations=30)  # positions for all nodes
    nn = nx.draw_networkx_nodes(G, pos,nodelist=G.nodes,node_size=20)
    ne = nx.draw_networkx_edges(G, pos,edgelist=G.edges)
    #nl = nx.draw_networkx_labels(G, pos, labels=labels, font_size=16)
    #labels = nx.draw_networkx_labels(G, pos=pos)
    labels  = nx.draw_networkx_labels(G, pos, labels=labels, verticalalignment='bottom', font_size=8)

    plt.axis("off")
    plt.show()
    

if __name__ == "__main__":

    fn = sys.argv[1]
    ifc_file = ifcopenshell.open(fn)

    start_time = time.time()
    G = create_graph(ifc_file)        
    print("--- %s seconds ---" % (time.time() - start_time))
    
    sg = get_subgraph(23974, G)

    #import pdb; pdb.set_trace()
    
    draw_graph(sg)

 
    







  