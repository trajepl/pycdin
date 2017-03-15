# generate graph (node :n edge:e)

#
# linux cmd return ports which are used.
# netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'
#
import random


def create_graph(n):
    node_list = []
    for i in range(n):
        node_list.append([])
        for j in range(n):
            if i == j:
                node_list[i].append(0)
                continue
            node_list[i].append(random.randint(1, n + 1))
    for i in range(n):
        for j in range(i):
            node_list[i][j] = node_list[j][i]
    return node_list


def min_edge(close_edge, n, key):
    tmp = n * n
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
    """
    :param n: number of node in graph.
    :return:
    """
    graph = create_graph(n)
    ret_graph = prim(graph)
    
    node_num = len(ret_graph)
    num_edge_random = random.randint(0, int(node_num * 0.8))

    for i in range(num_edge_random):
        id_edge = random.randint(0, (node_num - 1) * 2)
        x = id_edge // node_num
        y = id_edge % node_num
        if ret_graph[x][y] == '*' and ret_graph[y][x] and x != y:
            ret_graph[x][y] = 1

    # print('return ret_graph')
    # print(ret_graph)
    return ret_graph


def host_maps(n, host_list):
    """
    :param n: number of root.
    :param host_list: cluster pc IP LIST.
    :return: graph(randomly generate connection graph) maps(hosts+IP).
    """
    if len(host_list) > MAX_PORT - MIN_PORT:
        print("Too much nodes.")
    else:
        maps = []
        count = 0
        for port in range(MIN_PORT, MIN_PORT + n):
            for host in host_list:
                host_port = [host, str(port)]
                maps.append(host_port)
                count += 1
                if count >= n:
                    break
            if count >= n:
                break

    random.shuffle(maps)
    graph = gen_connected_graph(n)
    return graph, maps


def host_list(n, host_list):
    """
    :param n: number of root.
    :param host_list: cluster pc IP LIST.
    :return: [[host port|*m] * n]  every item in return res means the address which should be send msg.
    """
    res = []
    graph, maps = host_maps(n, host_list)

    for i in range(n):
        s = ""
        for j in range(n):
            if graph[i][j] == 1:
                for item in maps[j]:
                    s += item
                    s += ' '
                s = s[:-1]
                s += '|'

        res.append(s)
    return maps, res


MIN_PORT = 9000
MAX_PORT = 9999

if __name__ == '__main__':
    host = ['1', '2', '3']
    maps, res = host_list(4, host)
    print(maps)
    print(res)
