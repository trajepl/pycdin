# generate graph (node :n edge:e)
import random


def create_graph(n):
    node_list = []
    for i in range(n):
        node_list.append([])
        for j in range(n):
            if i == j:
                node_list[i].append(0)
                continue
            node_list[i].append(random.randint(1, n+1))
    for i in range(n):
        for j in range(i):
            node_list[i][j] = node_list[j][i]
    return node_list


def min_edge(close_edge, n, key):
    tmp = n*n
    ret = 0
    for i in range(n):
        if i in key:
            continue
        if close_edge[i][1] < tmp:
            tmp = close_edge[i][1]
            ret = i
    return ret


def empty_graph(n):
    node_list = []

    for i in range(n):
        node_list.append([])
        for j in range(n):
            node_list[i].append('*')

    return node_list


def prim(node_list):
    ret_graph = empty_graph(len(node_list))
    close_edge = []
    node_num = len(node_list)

    key_node_loop = 0
    node_visited = [0]

    # init the close_edge(node, len_edge)
    for node in range(node_num):
        if node != key_node_loop:
            close_edge.append([node, node_list[key_node_loop][node], [key_node_loop, node]])
        else:
            close_edge.append([node, 0, [node, node]])

    for node in range(1, node_num):
        key_node_loop = min_edge(close_edge, node_num, node_visited)

        start = close_edge[key_node_loop][-1][0]
        end = close_edge[key_node_loop][-1][1]
        ret_graph[start][end] = 1

        close_edge[key_node_loop][1] = 0
        node_visited.append(key_node_loop)

        for i_node in range(node_num):
            if node_list[key_node_loop][i_node] < close_edge[i_node][1]:
                close_edge[i_node] = [i_node, node_list[key_node_loop][i_node], [key_node_loop, i_node]]

    return ret_graph


def gen_connected_graph(n):
    graph = create_graph(n)
    ret_graph = prim(graph)
    print(ret_graph)
    node_num = len(ret_graph)
    num_edge_random = random.randint(0, int(node_num * 0.8))

    for i in range(num_edge_random):
        id_edge = random.randint(0, (node_num-1) * 2)
        x = id_edge // node_num
        y = id_edge % node_num
        if ret_graph[x][y] == '*' and ret_graph[y][x]:
            ret_graph[x][y] = 1
    print(ret_graph)
    return ret_graph



def gen_host_file(n):
    id = 0
    filename = 'hostlist'
    network = gen_connected_graph(n)

    for hosts in network:
        id += 1
        with open(filename+str(id), 'w') as host_out:
            host_out.write()




if __name__ == '__main__':
    gen_connected_graph(4)
