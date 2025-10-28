# ----------------------------------------------------------
# Edmonds-Karp Algorithm for Maximum Flow
# ----------------------------------------------------------
# This program finds the maximum flow in a given flow network
# and displays the flow through each edge as well as the total
# maximum flow value.
# ----------------------------------------------------------

from collections import deque

# ---------- Function Definitions ----------

def edmonds_karp(capacity, source, sink):
    n = len(capacity)
    residual = [row[:] for row in capacity]
    parent = [-1] * n

    def bfs():
        """Find augmenting path using BFS."""
        for i in range(n):
            parent[i] = -1
        queue = deque([source])
        parent[source] = source
        while queue:
            u = queue.popleft()
            for v in range(n):
                if parent[v] == -1 and residual[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
                    if v == sink:
                        return True
        return False

    max_flow = 0
    while bfs():
        # Find bottleneck (minimum capacity in the path)
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = u

        # Update residual capacities
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = u

        max_flow += path_flow

    return residual, max_flow


# ---------- Example Network ----------

# Node names for readability
names = ["s", "v1", "v2", "v3", "t"]

# Capacity matrix
capacity = [
    [0, 16, 13, 0, 0],   # s
    [0, 0, 10, 12, 4],   # v1
    [0, 4, 0, 0, 14],    # v2
    [0, 0, 9, 0, 20],    # v3
    [0, 0, 0, 0, 0]      # t
]

# ---------- Run Edmonds-Karp ----------
residual, max_flow = edmonds_karp(capacity, 0, 4)

# ---------- Compute Forward Flows ----------
n = len(capacity)
forward_flow = [[0] * n for _ in range(n)]
for u in range(n):
    for v in range(n):
        if capacity[u][v] > 0:
            forward_flow[u][v] = max(0, capacity[u][v] - residual[u][v])

# ---------- Output ----------
print("----- Edmonds-Karp Maximum Flow -----\n")
print("Forward flow on original edges (flow / capacity):")
for u in range(n):
    for v in range(n):
        if capacity[u][v] > 0:
            print(f"{names[u]} -> {names[v]} : {forward_flow[u][v]} / {capacity[u][v]}")
print()
print("Total maximum flow from source (s):", max_flow)
