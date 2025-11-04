# ----------------------------------------------------------
# Edmonds-Karp Algorithm for Maximum Flow (Colorized Edition)
# ----------------------------------------------------------
# Same logic, cleaner layout, and colorful terminal output.
# Uses 'colorama' for colored text. Run: pip install colorama
# ----------------------------------------------------------

from collections import deque
from colorama import Fore, Style, init

# Initialize colorama for Windows
init(autoreset=True)


def edmonds_karp(capacity, source, sink):
    """
    Compute max flow using Edmonds-Karp (BFS-based Ford-Fulkerson).
    Returns (residual_matrix, max_flow).
    """
    n = len(capacity)
    residual = [row[:] for row in capacity]
    parent = [-1] * n

    def bfs():
        """Find an augmenting path using BFS."""
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
        # Find bottleneck
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = u

        # Update residuals
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = u

        max_flow += path_flow

    return residual, max_flow


def compute_forward_flow(capacity, residual):
    """Compute forward flows on original edges."""
    n = len(capacity)
    forward_flow = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if capacity[u][v] > 0:
                forward_flow[u][v] = max(0, capacity[u][v] - residual[u][v])
    return forward_flow


def pretty_print_flow(names, capacity, forward_flow, max_flow):
    """Print a colorful table of flows and total max flow."""
    n = len(capacity)
    rows = []
    for u in range(n):
        for v in range(n):
            if capacity[u][v] > 0:
                rows.append((names[u], names[v], forward_flow[u][v], capacity[u][v]))

    col1 = max(len(r[0]) for r in rows)
    col2 = max(len(r[1]) for r in rows)
    col3 = max(len(f"{r[2]} / {r[3]}") for r in rows)

    # Title
    print(Fore.CYAN + Style.BRIGHT + "\n+" + "-" * 58 + "+")
    print("|{:^58}|".format("✨ Edmonds-Karp Maximum Flow Results ✨"))
    print("+" + "-" * 58 + "+\n" + Style.RESET_ALL)

    # Header
    print(
        Style.BRIGHT
        + Fore.YELLOW
        + "{:<{w1}}  ->  {:<{w2}}   :   {:>{w3}}".format(
            "From", "To", "Flow / Capacity", w1=col1, w2=col2, w3=col3
        )
    )
    print(Fore.YELLOW + "-" * (col1 + col2 + col3 + 12))

    # Rows
    for (u_name, v_name, flow, cap) in rows:
        fc = f"{flow} / {cap}"
        color = (
            Fore.GREEN
            if flow == cap
            else (Fore.MAGENTA if flow > 0 else Fore.LIGHTBLACK_EX)
        )
        print(
            f"{Fore.CYAN}{u_name:<{col1}}{Fore.WHITE}  ->  {Fore.CYAN}{v_name:<{col2}}"
            f"{Fore.WHITE}   :   {color}{fc:>{col3}}"
        )

    print(Fore.YELLOW + "\n" + "-" * 58)
    print(
        Style.BRIGHT
        + Fore.GREEN
        + f"Total maximum flow from source (s): {max_flow}"
    )
    print(Fore.CYAN + "+" + "-" * 58 + "+" + Style.RESET_ALL)


# ---------------- Example Network ----------------

names = ["s", "v1", "v2", "v3", "t"]

capacity = [
    [0, 16, 13, 0, 0],   # s
    [0, 0, 10, 12, 4],   # v1
    [0, 4, 0, 0, 14],    # v2
    [0, 0, 9, 0, 20],    # v3
    [0, 0, 0, 0, 0]      # t
]

# ---------------- Run & Display ----------------

residual, max_flow = edmonds_karp(capacity, 0, 4)
forward_flow = compute_forward_flow(capacity, residual)
pretty_print_flow(names, capacity, forward_flow, max_flow)
