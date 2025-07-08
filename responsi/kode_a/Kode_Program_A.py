import random
import copy

courses = ["Matematika", "Pemrograman", "Jaringan"]
lecturers = {
    "Matematika": "Dosen A",
    "Pemrograman": "Dosen B",
    "Jaringan": "Dosen C"
}
available_times = {
    "Dosen A": ["Senin", "Selasa"],
    "Dosen B": ["Selasa", "Rabu"],
    "Dosen C": ["Senin", "Rabu"]
}
timeslots = ["Senin", "Selasa", "Rabu"]

# Fungsi untuk menghasilkan penjadwalan acak
def random_schedule():
    return {course: random.choice(timeslots) for course in courses}

# Fungsi untuk menghitung konflik
def calculate_conflict(schedule):
    conflict = 0
    used_slots = {}
    for course, day in schedule.items():
        lecturer = lecturers[course]
        # Konflik: dosen tidak tersedia
        if day not in available_times[lecturer]:
            conflict += 1
        # Konflik: dua kuliah di waktu yang sama
        if day in used_slots:
            conflict += 1
        else:
            used_slots[day] = course
    return conflict

# Fungsi mencari tetangga
def get_neighbors(schedule):
    neighbors = []
    for course in courses:
        for day in timeslots:
            if schedule[course] != day:
                neighbor = copy.deepcopy(schedule)
                neighbor[course] = day
                neighbors.append(neighbor)
    return neighbors

# Hill Climbing Algorithm
def hill_climbing():
    current = random_schedule()
    current_conflict = calculate_conflict(current)
    
    while True:
        neighbors = get_neighbors(current)
        next_candidate = None
        next_conflict = current_conflict
        
        for neighbor in neighbors:
            conflict = calculate_conflict(neighbor)
            if conflict < next_conflict:
                next_candidate = neighbor
                next_conflict = conflict
        
        if next_conflict < current_conflict:
            current = next_candidate
            current_conflict = next_conflict
        else:
            break
    
    return current, current_conflict

# Eksekusi
solution, conflicts = hill_climbing()
print("Penjadwalan Optimal:")
for course, day in solution.items():
    print(f"- {course} dijadwalkan pada hari {day}")
print(f"Jumlah konflik: {conflicts}")