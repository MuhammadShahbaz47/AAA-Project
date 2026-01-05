# ----------------------------------------------------------
# Dynamic Bandwidth Allocation using Edmonds-Karp Algorithm
# Topic: Network Flow for Resource Allocation
# ----------------------------------------------------------

from collections import deque
from colorama import Fore, Style, init

# Enable colored output
init(autoreset=True)


# ----------------------------------------------------------
# Edmonds-Karp Algorithm (Max Flow)
# ----------------------------------------------------------
def edmonds_karp(capacity, source, sink):
    n = len(capacity)
    residual = [row[:] for row in capacity]
    parent = [-1] * n

    def bfs():
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
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = u

        max_flow += path_flow

    return residual, max_flow


# ----------------------------------------------------------
# Compute Forward Flow
# ----------------------------------------------------------
def compute_forward_flow(capacity, residual):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]

    for u in range(n):
        for v in range(n):
            if capacity[u][v] > 0:
                flow[u][v] = capacity[u][v] - residual[u][v]

    return flow


# ----------------------------------------------------------
# Pretty & Structured Output
# ----------------------------------------------------------
def print_network_state(time_label, names, capacity, flow, max_flow):
    print(Fore.CYAN + Style.BRIGHT + "\n╔" + "═" * 66 + "╗")
    print(f"║{time_label.center(66)}║")
    print("╚" + "═" * 66 + "╝\n")

    header = f"{'FROM':<12}{'TO':<12}{'USED':<10}{'TOTAL':<10}{'STATUS'}"
    print(Style.BRIGHT + Fore.YELLOW + header)
    print(Fore.YELLOW + "-" * 66)

    for u in range(len(names)):
        for v in range(len(names)):
            if capacity[u][v] > 0:
                used = flow[u][v]
                total = capacity[u][v]
                ratio = used / total

                # Visual usage bar
                bar_length = 15
                filled = int(ratio * bar_length)
                bar = "█" * filled + "░" * (bar_length - filled)

                # Color logic
                if used == 0:
                    color = Fore.LIGHTBLACK_EX
                    status = "Idle"
                elif used < total:
                    color = Fore.MAGENTA
                    status = "Active"
                else:
                    color = Fore.GREEN
                    status = "Full"

                print(
                    f"{Fore.CYAN}{names[u]:<12}"
                    f"{names[v]:<12}"
                    f"{color}{used:<10}"
                    f"{total:<10}"
                    f"{color}{bar} {status}"
                )

    print(Fore.YELLOW + "\n" + "-" * 66)
    print(
        Style.BRIGHT
        + Fore.GREEN
        + f"🚀 Total Network Throughput: {max_flow} Mbps"
    )
    print(Fore.CYAN + "═" * 66)


# ----------------------------------------------------------
# Network Nodes
# ----------------------------------------------------------
names = ["Source", "R1", "R2", "R3", "Destination"]
SOURCE = 0
SINK = 4


# ----------------------------------------------------------
# 2:00 PM — Normal Conditions
# ----------------------------------------------------------
capacity_200 = [
    [0, 100, 0,   0,   0],
    [0, 0,   80,  0,   0],
    [0, 0,   0,   70,  0],
    [0, 0,   0,   0,   90],
    [0, 0,   0,   0,   0]
]

residual, max_flow = edmonds_karp(capacity_200, SOURCE, SINK)
flow = compute_forward_flow(capacity_200, residual)
print_network_state("🕑 2:00 PM — Normal Network Load", names, capacity_200, flow, max_flow)


# ----------------------------------------------------------
# 2:01 PM — Congestion
# ----------------------------------------------------------
capacity_201 = [
    [0, 100, 0,   0,   0],
    [0, 0,   60,  0,   0],  # Congestion here
    [0, 0,   0,   70,  0],
    [0, 0,   0,   0,   90],
    [0, 0,   0,   0,   0]
]

residual, max_flow = edmonds_karp(capacity_201, SOURCE, SINK)
flow = compute_forward_flow(capacity_201, residual)
print_network_state("🕑 2:01 PM — Congestion Detected", names, capacity_201, flow, max_flow)


# ----------------------------------------------------------
# 2:02 PM — Backup Link Added
# ----------------------------------------------------------
capacity_202 = [
    [0, 100, 0,   50,  0],  # Backup link added
    [0, 0,   60,  0,   0],
    [0, 0,   0,   70,  0],
    [0, 0,   0,   0,   90],
    [0, 0,   0,   0,   0]
]

residual, max_flow = edmonds_karp(capacity_202, SOURCE, SINK)
flow = compute_forward_flow(capacity_202, residual)
print_network_state("🕑 2:02 PM — Backup Link Active", names, capacity_202, flow, max_flow)
