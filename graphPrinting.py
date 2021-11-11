import networkx as nx
import matplotlib.pyplot as plt


# Prints average length of a generation
def printEvolutionGraph(averageList, best, filename):
    figure = plt.gcf()
    plt.plot(averageList)
    plt.xlabel('Generations')
    plt.ylabel('Length')
    if filename == 'bees':
        label = 'best bee length'
    else:
        label = 'generation\'s average length'
    plt.title('Last ' + label + ': ' + best)
    plt.savefig('./generations/' + filename + '.png', bbox_inches='tight')
    plt.tight_layout()
    figure.clear()
    plt.clf()


# Inits Graph with Networkx
def initPrintingGraph(flowersList):
    graph = nx.DiGraph(directed=True)
    nodePos = drawNodes(flowersList, graph)
    plt.savefig("./generations/flowerfield.png")
    plt.tight_layout()
    plt.axis("off")
    plt.clf()
    return graph, nodePos


# Chooses node color to add diversity
def chooseColor(index):
    if index % 5 == 0:
        return "#FCE205"
    elif index % 5 == 1:
        return "#FF0000"
    elif index % 5 == 2:
        return "#2986CC"
    elif index % 5 == 3:
        return "#C90076"
    else:
        return "#00f6ff"


# Adds and draws nodes = flowers
def drawNodes(flowersList, graph):
    # Adds nodes
    for flower in flowersList:
        index = flower.getIndex()
        coordinates = flower.getCoordinates()
        graph.add_node(index, pos=coordinates)
    graph.add_node(50, pos=(500, 500))  # beehive start
    nodePos = nx.get_node_attributes(graph, 'pos')
    # Draws nodes
    for flower in flowersList:
        index = flower.getIndex()
        color = chooseColor(flower.getIndex())
        nx.draw_networkx_nodes(graph, nodePos, node_size=100, nodelist=[index], node_color=color, node_shape="X")
    nx.draw_networkx_nodes(graph, nodePos, nodelist=[50], node_color="#27a906", node_shape="s")  # Draws beehive
    return nodePos


# Adds edges = bee path to graph and draws them
def drawEdges(nodePos, graph, bee):
    path = bee.getOrder()
    # Adds edge between first flower and beehive
    graph.add_edge(50, path[0].getIndex())
    for i in range(len(path) - 1):
        first_flower = path[i].getIndex()
        second_flower = path[i + 1].getIndex()
        graph.add_edge(first_flower, second_flower)
    # Draws edges
    nx.draw_networkx_edges(graph, nodePos, style="solid", width=2.0, label="S", arrows=True, arrowstyle='->')


# Prints NetworkX Graph
def printGraph(graph, nodePos, flowersList, generationId, bee):
    figure = plt.gcf()
    figure.canvas.manager.set_window_title('Flowerfield')
    figure.canvas.manager.window.SetPosition = (200, 200)
    drawNodes(flowersList, graph)
    drawEdges(nodePos, graph, bee)
    # plt.savefig("./generations/gen" + str(generationId) + ".png")
    title = 'Generation ' + str(generationId) + ' -- Length:' + str(bee.getLength())
    plt.title(title)
    plt.tight_layout()
    plt.axis("off")
    plt.draw()
    plt.pause(0.05)
    plt.clf()
    graph.remove_edges_from(list(graph.edges()))
