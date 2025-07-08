import heapq
import itertools

# Data kota: waktu tempuh dan tingkat kemacetan
cities = {
    "Kota A": {"waktu": 3, "macet": 4},
    "Kota B": {"waktu": 5, "macet": 6},
    "Kota C": {"waktu": 2, "macet": 8},
    "Kota D": {"waktu": 4, "macet": 3},
}

# Fungsi biaya (semakin rendah semakin baik)
def city_cost(city):
    data = cities[city]
    return data["waktu"] + (data["macet"] / 2)

# Heuristik: total biaya sisa
def heuristic(path):
    remaining = [c for c in cities if c not in path]
    return sum(city_cost(c) for c in remaining)

# Best First Search
def best_first_delivery():
    queue = []
    counter = itertools.count()
    heapq.heappush(queue, (0, next(counter), [], 0))  # (heuristik, id, path, cost_so_far)
    
    while queue:
        h, _, path, cost = heapq.heappop(queue)
        
        if len(path) == len(cities):
            return path, cost
        
        for city in cities:
            if city not in path:
                new_path = path + [city]
                new_cost = cost + city_cost(city)
                h_val = new_cost + heuristic(new_path)
                heapq.heappush(queue, (h_val, next(counter), new_path, new_cost))

# Jalankan pencarian
result_path, total_cost = best_first_delivery()

# Tampilkan hasil
print("Urutan Pengiriman Optimal:")
for i, city in enumerate(result_path, 1):
    print(f"{i}. {city} (Biaya: {city_cost(city)})")
print(f"\nTotal Biaya Perjalanan: {round(total_cost, 2)}")