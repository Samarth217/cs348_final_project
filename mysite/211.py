import sys
import StringIO
# Test input simulating sys.stdin.read()
test_input = """3
1 3 9
2 2 16
5 2 11
"""

# Simulating reading from stdin
sys.stdin = StringIO(test_input)  # Replace sys.stdin with the test input string

lines = sys.stdin.read().splitlines()

#print(lines)

num_planets = int(lines[0])
index = 1

for i in range(num_planets) :
    curr_data = lines[index].split()
    print(curr_data)
    P = curr_data[0]
    R = curr_data[1]
    F = curr_data[2]

    survival = 0

    while P <= F :
        survival +=1
        P *= R

        print(survival)
        index +=1
        
    print("finished")
