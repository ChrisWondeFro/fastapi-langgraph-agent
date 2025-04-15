from importlib import import_module
from pathlib import Path

def discover_graphs():
    base = Path(__file__).parent
    graphs = {}
    for graph_py in base.rglob("*/graph.py"):
        mod_path = (
            "app.core.langgraph_modules." +
            str(graph_py.relative_to(base).with_suffix("")).replace("/", ".")
        )
        module = import_module(mod_path)
        graph = getattr(module, "graph", None)
        if graph:
            graph_id = mod_path.split("langgraph_modules.")[-1].replace(".", "_")
            graphs[graph_id] = graph
    return graphs
