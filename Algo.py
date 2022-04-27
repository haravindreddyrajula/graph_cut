
def BFS(graph, s, t, arr):
    visited = [False] * (len(graph))
    que = []
    que.append(s)
    visited[s] = True

    while que:
        u = que.pop(0)
        for i, v in enumerate(graph[u]):
            if v > 0 and visited[i] == False:
                que.append(i)
                visited[i] = True
                arr[i] = u
    if visited[t]:
        return True
    else:
        return False


def dfs(graph, s, visited):
    visited[s] = True
    for i in range(len(graph)):
        if graph[s][i] > 0 and not visited[i]:
            dfs(graph, i, visited)


def algo(graph, source, sink):
    graph_initial = [i[:] for i in graph]
    # This array is filled by BFS and to store path
    arr = [-1] * (len(graph))

    max_flow = 0  # There is no flow initially

    while BFS(graph, source, sink, arr):

        path_flow = float("Inf")
        s = sink
        while (s != source):
            path_flow = min(path_flow, graph[arr[s]][s])
            s = arr[s]

        max_flow = max_flow + path_flow

        v = sink
        while (v != source):
            u = arr[v]
            graph[u][v] = graph[u][v] - path_flow
            graph[v][u] = graph[u][v] + path_flow
            v = arr[v]

    visited = len(graph) * [False]
    dfs(graph, s, visited)

    finalnodestocut = []
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == 0 and graph_initial[i][j] > 0 and visited[i]:
                finalnodestocut.append(str(i) + "-" + str(j))

    return finalnodestocut
