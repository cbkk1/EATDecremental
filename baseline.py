import sys
 
 
def parse_temporal_graph(filepath):
    """Parse a temporal graph file.
 
    Format:
        n m
        u1 v1 dt1 lambda1
        u2 v2 dt2 lambda2
        ...
    """
    with open(filepath, "r") as f:
        n, m = map(int, f.readline().split())
        edges = []
        for _ in range(m):
            parts = f.readline().split()
            u, v, dt, lam = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
            edges.append((u, v, dt, lam))
    return n, m, edges
 
 
def earliest_arrival_time(n, edges, source, start_time):
    """Compute earliest arrival time from source at start_time to all vertices.
 
    Algorithm:
        - Sort edges by departure time.
        - Sweep through edges: if we can reach u by departure time dt,
          then we can arrive at v by dt + lambda. Update if this improves
          the known earliest arrival at v.
    """
    INF = float("inf")
    eat = [INF] * (n + 1)  # 1-indexed; eat[0] unused if vertices start at 1
    eat[source] = start_time
 
    sorted_edges = sorted(edges, key=lambda e: e[2])
 
    changed = True
    while changed:
        changed = False
        for u, v, dt, lam in sorted_edges:
            if eat[u] <= dt and dt + lam < eat[v]:
                eat[v] = dt + lam
                changed = True
 
    return eat
 
 
def save_results(filepath, n, source, start_time, eat):
    with open(filepath, "w") as f:
        f.write(f"Source: {source}\n")
        f.write(f"Start time: {start_time}\n")
        f.write(f"{'Vertex':<10}{'Earliest Arrival Time'}\n")
        f.write("-" * 35 + "\n")
        for v in range(1, n + 1):
            arrival = eat[v] if eat[v] != float("inf") else "unreachable"
            f.write(f"{v:<10}{arrival}\n")
 
 
def main():
    if len(sys.argv) != 4:
        print("Usage: python earliest_arrival.py <graph_file> <source> <start_time>")
        sys.exit(1)
 
    graph_file = sys.argv[1]
    source = int(sys.argv[2])
    start_time = int(sys.argv[3])
 
    n, m, edges = parse_temporal_graph(graph_file)
    eat = earliest_arrival_time(n, edges, source, start_time)
 
    output_file = "earliest_arrival_result.txt"
    save_results(output_file, n, source, start_time, eat)
    print(f"Results saved to {output_file}")
 
 
if __name__ == "__main__":
    main()
