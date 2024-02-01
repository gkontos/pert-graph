import yaml
import networkx as nx
import matplotlib.pyplot as plt


def parse_nodes(deps, graph):
    """Traverse the dictionary and add the nodes and edges to our graph

    We are also adding the duration as an attribute of the nodes and edges.
    Adding the attribute to the node allows us to display the information on the label, 
    Adding the attribute to the edges allows us to calculate the project duration.
    """
    for k, v in deps.items():
        graph.add_node(k, duration=v["duration"])
        if v.get("dependencies") is not None:
            for item in v["dependencies"]:
                parse_nodes(item, graph)
                for childkey in item.keys():
                    graph.add_edge(childkey, k, duration=v["duration"])
    return graph


def load_dependencies_from_file():
    """Load our dependencies into a Dict
    """
    with open("input/dependencies.yaml", "r", encoding="utf-8") as file:
        dependencies = yaml.safe_load(file)
    return dependencies


# node labels from 'edo': https://stackoverflow.com/a/46503250
def print_with_labels(graph):
    """Generate and save an image file of the graph with labels 
    """
    plt.figure()
    pos_nodes = nx.spectral_layout(graph)
    nx.draw(graph, pos_nodes, with_labels=True, font_weight="bold")

    pos_attrs = {}
    for node, coords in pos_nodes.items():
        pos_attrs[node] = (coords[0], coords[1] + 0.08)

    node_attrs = nx.get_node_attributes(graph, "duration")
    custom_node_attrs = {}
    for node, attr in node_attrs.items():
        custom_node_attrs[node] = f"duration: {attr}"

    nx.draw_networkx_labels(graph, pos_attrs, labels=custom_node_attrs)
    plt.savefig("output/path.png")


def main():
    """Generate a graph from our yaml file. 
    The methods nx.dag_longest_path and nx.path_weight are from the networkx project.
    Together they calculate the duration of the Critical Path -- which required a super computer in 1958
    """
    dependencies = load_dependencies_from_file()
    graph = nx.DiGraph()
    graph = parse_nodes(dependencies, graph)

    print_with_labels(graph)

    path = nx.dag_longest_path(graph, weight="duration")
    print(f"The critical path is {path}")
    duration = nx.path_weight(graph, path, weight="duration")
    print(f"The expected duration is {duration}")
    return


main()
