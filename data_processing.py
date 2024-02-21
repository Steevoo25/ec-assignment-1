from pickle import dump

# --- Read File contents
with open("att48.txt", "r") as file:
    file_contents = file.read()
    
# split by newline
file_lines = file_contents.splitlines()

# remove header info and EOF
file_lines = file_lines[6:-1]

# put into array
us_capitals = []
for capital in file_lines:
    # split each element
    _, x, y = capital.split()
    # put element into dictionary
    us_capitals.append((int(x),int(y)))

with open("us_capitals.pkl", "wb") as file:
    dump(us_capitals, file)