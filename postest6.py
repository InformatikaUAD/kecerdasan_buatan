from ai_pkg.planning import (HLA, Problem as PlanProblem)

# Library yang berisi informasi tentang langkah-langkah dan kondisi untuk mencapai tujuan
# Mengimpor kelas HLA dan Problem dari modul ai_pkg.planning
library = {
        'HLA': ['Go(Home,Airport)', 
                'Go(Home,Airport)', 
                'Drive(Home,AirportParking)', 
                'Shuttle(AirportParking,Airport)', 
                'Taxi(Home,Airport)'],
        'steps':[['Drive(Home,AirportParking)','Shuttle(AirportParking,Airport)'], 
                ['Taxi(Home,Airport)'], 
                [], 
                [], 
                []],
        'precond': [['At(Home) & Have(Car)'], 
                        ['At(Home)'], 
                        ['At(Home) & Have(Car)'], 
                        ['At(AirportParking)'], 
                        ['At(Home)']],
        'effect': [['At(Airport) & ~At(Home)'], 
                        ['At(Airport) & ~At(Home) & ~Have(Cash)'], 
                        ['At(AirportParking) & ~At(Home)'],
                        ['At(Airport) & ~At(LongTermParking)'], 
                        ['At(Airport) & ~At(Home) & ~Have(Cash)']] 
                        
        
}

# goto_airport = HLA('Go(Home,Airport)', precond='At(Home)', effect='At(Airport) & ~At(Home)')
# problem = PlanProblem('At(Home) & Have(Cash) & Have(Car) ', 'At(Airport) & Have(Cash)', [goto_airport])


"""
        Misalnya kita ingin menghindari penggunaan mobil pribadi,
        kita bisa menghilangkan Have(Car) dari precondition HLA dan dari initial state.
        Atau kita ingin menggunakan opsi taksi, karena itu tidak membutuhkan mobil
        dan tidak mempermasalahkan cash.

"""


goto_airport = HLA('Go(Home,Airport)', precond='At(Home) & Have(Cash)', effect='At(Airport) & ~At(Home) & ~Have(Cash)')

problem = PlanProblem('At(Home) & Have(Cash)', 'At(Airport)', [goto_airport])


solution = PlanProblem.hierarchical_search(problem, library)
for i in range(0, len(solution)):
    print('precondition : ', solution[i].precond)
    print('action : ', solution[i].name, solution[i].args)
    print('effect : ', solution[i].effect)