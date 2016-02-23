import os

c = 0.0
a = 0.0
with open("stats") as f:
	content = f.readlines()
	for line in content :
		a += int(line.split(":")[0])
		c += 1
print a/c
