from hydrodb import *
import random
from time import time

hydro = HydroDB("tests")

hydro.create_table(table_name="TABLE_1", columns=["name", "age", "gen"], pk="id")

names_list:list = ["Caio", "Pedro", "Felipe", "Ana", "Beatriz", "Maria"]

i=0


while i < 0:
    choised_name = random.choice(names_list)
    age = random.randint(15, 40)
    gen = random.choice(["F", "M"])

    hydro.add_rows(table_name="TABLE_1", into_columns=['name', 'age', "gen"], values=[choised_name, age, gen])

    i+=1


# hydro.update(from_="TABLE_1", columns=['name', "age"], where="id <= 10", with_values=["BANANA", 55])
    
print(hydro.querry(from_="TABLE_1", columns=['name'], where="id = 15"))

# hydro.delete(from_="TABLE_1", where="id <= 4")