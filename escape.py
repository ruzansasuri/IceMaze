
class GraphNode:
    """
    A node for the graph which contains the vertex coordinate and a list of its neighboring vertices.
    """
    __slots__ = 'point', 'neighbor'

    def __init__(self, p):
        """
        Initializes a node to a particular vertex.
        :pre: p should be a tuple of the coordinate of the vertex in the (y, x) format.
        :param p: A tuple of the coordinates of the point.
        """
        self.point = p
        self.neighbor = []

    def addneighbor(self, point):
        """
        Adds a neighboring vertex to the list.
        :pre: point should be a tuple of the coordinate of the neighboring vertex in the (y, x) format.
        :param point: A tuple of the coordinates of the neighboring vertex.
        :return: None.
        """
        self.neighbor.append(point)


class Maze:
    """
    Holds a graph of the maze with the vertex and its respective object.
    """
    __slots__ = 'row', 'column', 'pointgraph', 'mapexit'

    def __init__(self, r, c, e):
        """
        Initializes the Maze with its row, column and escape vertex.
        :pre: r and c should be non-zero integers. e should be a tuple of the coordinate of the neighboring vertex in the (y, x) format.
        :param r: The number of rows in the maze.
        :param c: The number of columns in the maze.
        :param e: The escape vertex of the maze
        """
        self.pointgraph = {}
        self.row = r
        self.column = c
        self.mapexit = e

    def addpoint(self, p):
        """
        Adds a new vertex to the graph.
        :pre: p should be a tuple of the coordinate of the vertex in the (y, x) format.
        :param p: A tuple of the coordinates of the vertex.
        :return: None.
        """
        self.pointgraph[p] = GraphNode(p)

    def addedge(self, src, dest):
        """
        Adds a single direction path from the point to the nearest obstacle in a particular direction.
        pre: src and dest should be a tuple of coordinates of vertices in the (y, x) format.
        :param src: The starting vertex of the edge.
        :param dest: The ending vertex of the edge.
        :return: None.
        """
        if src not in self.pointgraph:
            self.addpoint(src)
        if dest not in self.pointgraph:
            self.addpoint(dest)
        self.pointgraph[src].addneighbor(self.pointgraph[dest])

    def __iter__(self):
        """
        Returns an iterator to use via a for loop.
        :return: The iterator.
        """
        return iter(self.pointgraph.values())

    def addifnotcreated(self, p):
        """
        Adds a point to the graph if an edge from it does not exist.:pre: p should be a tuple of the coordinate of the vertex in the (y, x) format.
        :param p: A tuple of the coordinates of the vertex.
        :return: None.
        """
        if p not in self.pointgraph:
            self.addpoint(p)


def file_check(file, perm):
    try:
        f = open(file, perm)
        return f
    except FileNotFoundError:
        print("File", file, "does not exist...")
        exit()


def creategraph(file):
    """
    Creates a graph based on what is populated in the file.
    :pre: The file should not be empty. It should have its first row as the number of rows, number of columns and the
    escape row, separated by spaces. the pond it self should only be made of . for water and * for rocks, and each
    vertex should be separated by a space.
    :param file: The file handler to be used.
    :return: The graph object.
    """
    line = file.readline().split(' ')
    r = int(line[0])
    c = int(line[1])
    if int(line[2]) >= r:
        print("The exit can not be out of the maze.")
        exit()
    m = Maze(r, c, (c - 1, int(line[2])))
    points = []
    x = 0
    y = 0
    for line in file:
        line = line.split()
        line[len(line) - 1] = line[len(line) - 1].split('\n')[0]
        points.append([])
        for point in line:
            points[len(points) - 1].append(point)
            y += 1
        x += 1
    if points[m.mapexit[1]][m.mapexit[0]] == '*':
        print("The exit can not be a rock.")
        exit()
    for x in range(r):
        for y in range(c):
            if not points[x][y] == '*':
                if not y == 0:
                    lo = -1
                    for i in range(y):
                        if points[x][i] == '*':
                            lo = i
                    if not lo + 1 == y:
                        m.addedge((y, x), (lo + 1, x))
                if not y == c - 1:
                    ro = c
                    for i in range(c - 1, y, -1):
                        if points[x][i] == '*':
                            ro = i
                    if not ro - 1 == y:
                        m.addedge((y, x), (ro - 1, x))
                if not x == 0:
                    uo = -1
                    for i in range(x):
                        if points[i][y] == '*':
                            uo = i
                    if not uo + 1 == x:
                        m.addedge((y, x), (y, uo + 1))
                if not x == r - 1:
                    do = r
                    for i in range(r - 1, x, -1):
                        if points[i][y] == '*':
                            do = i
                    if not do - 1 == x:
                        m.addedge((y, x), (y, do - 1))
                m.addifnotcreated((y, x))
    return m


def findexit(m):
    """
    Provides a dictionary of keys as the number of paths taken to the exit and values a list of vertices for the same.
    :pre: The graph should not be empty.
    :param m: The graph.
    :return: A dictionary for the paths.
    """
    paths = dict()
    paths[-1] = []
    for node in m:
        path = m.row * m.column
        visited = [(node.point, 0)]
        cpoint = 0
        while cpoint != len(visited) and not visited[cpoint - 1][0] == m.mapexit:
            for n in m.pointgraph[visited[cpoint][0]].neighbor:
                found = False
                for i in visited:
                    if n.point == i[0]:
                        found = True
                        break
                if not found:
                    visited.append((n.point, visited[cpoint][1] + 1))
                if n.point == m.mapexit:
                    break
            cpoint += 1
        if visited[cpoint - 1][0] == m.mapexit:
            path = visited[cpoint - 1][1]
        else:
            paths[-1].append(node.point)
            continue
        if path not in paths.keys():
            paths[path] = []
        paths[path].append(node.point)
    if 1 not in paths.keys():
        paths[1] = []
    paths[1].append(m.mapexit)
    return paths


def printit(p, m):
    """
    Prints the solution.
    :pre: p and m should not be empty.
    :param p: the dictionary for printing.
    :param m: The graph.
    :return: None.
    """
    for i in range(1, m.row * m.column + 1):
        if i in p.keys():
            print(i, ':', p[i])
    if len(p[-1]) > 0:
        print('No Path:', p[-1])


def main():
    """
    The main method.
    :return: None.
    """
    f = input('Enter the file name: ')
    fh = file_check(f, 'r')
    mazed = creategraph(fh)
    paths = findexit(mazed)
    printit(paths, mazed)

if __name__ == '__main__':
    main()
