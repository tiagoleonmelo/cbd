import redis

## Function that generates a file that will be afterwards used as input with
# redis-cli < names-inpt.txt

def reader():
    fin = open("female-names.txt", "r")
    fout = open("names-inpt.txt", "w")

    for u in fin:
        fout.write("SET " + '"female_names:' + u[0:] + '"' + " random_val\n")


# Starting the Redis Client
r = redis.Redis(host='localhost', port=6379, db=0)

# Getting the pattern
inpt = input('Enter a keyword.. ')

# We're using the prefix "female_names:" to avoid getting results from other data
bin_res = r.keys("female_names:"+inpt+"*")
names = []

for name in bin_res:
    names.append(name.decode()[13:])

# Sorting
names = sorted(names)

for name in names:
    print(name)