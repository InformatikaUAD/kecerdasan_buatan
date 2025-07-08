import heapq
import itertools
import pandas as pd

# Data nasabah dan kasir
customers = [("N1", 10), ("N2", 15), ("N3", 5), ("N4", 10), ("N5", 20), ("N6", 15)]
cashiers = {
    "Kasir A": 5,  # Kecepatan (semakin kecil, semakin cepat)
    "Kasir B": 7,
    "Kasir C": 10
}

# Fungsi menghitung total waktu pelayanan per kasir
def compute_total_time(assignments):
    total = {}
    for cashier in cashiers:
        total[cashier] = sum(
            duration * (1 / cashiers[cashier]) for name, duration in assignments.get(cashier, [])
        )
    return total

# Fungsi heuristik: maksimum waktu pelayanan antar kasir (makespan)
def heuristic(assignments):
    totals = compute_total_time(assignments)
    return max(totals.values())

# Best First Search
def best_first_search():
    queue = []
    counter = itertools.count()
    initial_state = {k: [] for k in cashiers}
    heapq.heappush(queue, (0, next(counter), initial_state, customers))
    visited = set()
    
    while queue:
        h, _, current_state, remaining = heapq.heappop(queue)
        
        if not remaining:
            return current_state, heuristic(current_state)
        
        # Hashable key untuk visited
        state_key = tuple(tuple((k, tuple(v)) for k, v in current_state.items()))
        
        if state_key in visited:
            continue
        visited.add(state_key)
        
        # Ambil customer pertama dari sisa
        customer = remaining[0]
        
        for cashier in current_state:
            new_state = {k: list(v) for k, v in current_state.items()}
            new_state[cashier].append(customer)
            new_remaining = remaining[1:]
            
            h_val = heuristic(new_state)
            heapq.heappush(queue, (h_val, next(counter), new_state, new_remaining))
    
    return None, None

# Jalankan algoritma
solution, total_time = best_first_search()

# Tampilkan hasil dalam tabel
rows = []
for cashier, assignments in solution.items():
    served = ", ".join([f"{name}({duration}m)" for name, duration in assignments])
    total = sum(duration * (1 / cashiers[cashier]) for name, duration in assignments)
    rows.append((cashier, served, round(total, 2)))

df = pd.DataFrame(rows, columns=["Kasir", "Nasabah Dilayani", "Total Waktu (unit waktu)"])
print(df)
print(f"\nTotal Waktu Terlama (Makespan): {round(total_time, 2)} unit waktu")