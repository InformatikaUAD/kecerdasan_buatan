from kanren import run, var, Relation, facts

x = var()
parent = Relation()
facts(parent, ("Heri", "Budi"), ("Budi", "Cinta"))
print(run(1, x, parent(x, "Cinta")))  # Output: ('Budi',)
