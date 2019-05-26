import glob
'''
out = open('a/full.txt', 'a')
for file in glob.glob("*.txt"):
    f = open(file, 'r')
    for line in f:
        out.write(line.replace(' ', ','))
    f.close
out.close()
'''
out = open('angl.txt', 'a')
f = open('291Anglia.txt', 'r')
for line in f:
    out.write(line.replace(' ', ','))
f.close
out.close()