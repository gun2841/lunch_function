filename ="./test.txt"

f = open(filename,'r',encoding='utf-8')
lines = f.readlines()


for line in lines:
    print(line.split(','))