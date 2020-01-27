f_input = open("female-names.txt", "r")
f_output = open("initials4redis.txt", "w")

prev = 'a'
count = 0

for w in f_input:
    if w[0] == prev:
        count += 1
    else:
        # write line
        f_output.write("SET " + prev.upper() + " " + str(count) + "\n")
        prev = w[0]
        count = 0

f_output.write("SET " + prev + " " + str(count) + "\n")
