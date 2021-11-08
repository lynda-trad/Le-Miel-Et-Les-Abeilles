import networkx as nx
import matplotlib.pyplot as plt


# Prints average length of a generation
def printAverageGraph(averageList):
    figure = plt.gcf()
    plt.plot(averageList)
    plt.ylabel('Length')
    plt.savefig("./generations/average.png", bbox_inches='tight')
    plt.tight_layout()
    figure.clear()
    plt.clf()


# Inits Graph with Networkx
def initPrintingGraph(flowersList):
    graph = nx.Graph()
    nodePos = drawNodes(flowersList, graph)
    # drawCoordinates(flowersList, nodePos)
    plt.savefig("./generations/flowerfield.png")
    plt.tight_layout()
    plt.axis("off")
    plt.clf()
    return graph, nodePos


# Draws coordinates above nodes
def drawCoordinates(flowersList, nodePos):
    for flower in flowersList:
        coordinates = flower.getCoordinates()
        x, y = nodePos[flower.getIndex()]
        plt.text(x, y + 0.1, s=coordinates, bbox=dict(facecolor='red', alpha=0.5), horizontalalignment='center')


# Adds and draws nodes = flowers
def drawNodes(flowersList, graph):
    # Adds nodes
    for flower in flowersList:
        index = flower.getIndex()
        coordinates = flower.getCoordinates()
        graph.add_node(index, pos=coordinates)
    graph.add_node(0, pos=(500, 500))  # beehive start
    nodePos = nx.get_node_attributes(graph, 'pos')
    # Draws nodes
    for flower in flowersList:
        index = flower.getIndex()
        color = index % 5
        if color == 0:
            nx.draw_networkx_nodes(graph, nodePos, nodelist=[index], node_color="#FCE205", node_shape="X")
        elif color == 1:
            nx.draw_networkx_nodes(graph, nodePos, nodelist=[index], node_color="#FF0000", node_shape="X")
        elif color == 2:
            nx.draw_networkx_nodes(graph, nodePos, nodelist=[index], node_color="#2986CC", node_shape="X")
        elif color == 3:
            nx.draw_networkx_nodes(graph, nodePos, nodelist=[index], node_color="#C90076", node_shape="X")
        else:
            nx.draw_networkx_nodes(graph, nodePos, nodelist=[index], node_color="#00f6ff", node_shape="X")
    nx.draw_networkx_nodes(graph, nodePos, nodelist=[0], node_color="#27a906", node_shape="s")  # Draws beehive
    return nodePos


# Adds edges = bee path to graph and draws them
def drawEdges(nodePos, graph, bee):
    # Adds edges
    path = bee.getOrder()
    for i in range(len(path) - 2):
        first_flower = path[i].getIndex()
        second_flower = path[i + 1].getIndex()
        graph.add_edge(first_flower, second_flower)
    # Draws edges
    nx.draw_networkx_edges(graph, nodePos, style="solid", width=2.0, label="S", arrowstyle='->')


# Prints NetworkX Graph
def printGraph(graph, nodePos, flowersList, generationId, bee):
    figure = plt.gcf()
    figure.canvas.manager.set_window_title('Flowerfield')
    figure.canvas.manager.window.SetPosition = (200, 200)
    drawNodes(flowersList, graph)
    # drawCoordinates(flowersList, nodePos)
    drawEdges(nodePos, graph, bee)
    plt.savefig("./generations/gen" + str(generationId) + ".png")
    plt.tight_layout()
    plt.axis("off")
    plt.draw()
    plt.pause(1)
    figure.clear()
    plt.clf()
