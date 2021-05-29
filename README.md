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

![image](https://user-images.githubusercontent.com/48138129/111918298-bb711a80-8a84-11eb-82c5-52cde13038e3.png)
