# IfcGraph

Use Networkx to manipulate an IFC file as a directed graph.


```python
#graph.py

import ifcopenshell
import ifcgraph
import sys

fn = sys.argv[1]
ifc_file = ifcopenshell.open(fn)

G = ifcgraph.create_graph(ifc_file)  
sorted = list(reversed(list(nx.topological_sort(G))))
      
SG = ifcgraph.get_subgraph(23946, G)

ifcgraph.draw_graph(SG)
```

`python graph.py input.ifc`


Output:

![image](https://github.com/johltn/IfcGraph/blob/master/ifcgraph_point.png)
