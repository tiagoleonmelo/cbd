import redis
import csv

## Function that will read from the .csv with popular names
# and turn them into redis commands

def reader():
    fin = open("nomes-registados-2018.csv", "r")
    fout = open("popular_names.txt", "w")

    csv_reader = csv.reader(fin)

    for row in csv_reader:
        fout.write(f'SET "popular_names:{row[0]}" {row[2]}\n')


def quick_sort(l):

    if len(l) <= 1:
        return l

    pivot = l[0]
    lst = l[:]

    smaller, larger = helper(pivot[1], lst[1:])

    return quick_sort(smaller) + [pivot] + quick_sort(larger)


def helper(elem, l):
    if l == []:
        return [[],[]]

    call = helper(elem, l[1:])

    if l[0][1] > elem:
        return [ call[0] + [l[0]], call[1] ]

    return [ call[0], call[1] + [l[0]] ]  


# Starting the Redis Client
r = redis.Redis(host='localhost', port=6379, db=0)

# Getting the pattern
inpt = input('Enter a keyword.. ')
inpt = inpt[0].upper() + inpt[1:]

# We're using the prefix "female_names:" to avoid getting results from other data
bin_res = r.keys("popular_names:"+inpt+"*")
names = []

for name in bin_res:
    # Inserting tuples that will be sorted by tuple[1]
    names.append( ( name.decode()[14:], int(r.get(name.decode()).decode()) ) )    

# Sorting
names = quick_sort(names)

for name in names:
    print(name[0])

