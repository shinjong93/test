import os
import sys
ROOT = "../result/"



def process(f):
        n1 = 0
        lines = []
        while True:
                line = f.readline()
                if not line: break
                for i in range(len(line)-1):
                    if line[i] == "{":
                        n1 += 1
                    if line[i] == ':':
                        line = line[:i] + '=' + line[i+1:]
                lines.append(line)
        f.seek(0)
        f.writelines(lines)
        f.close()


        while(n1 > 0):
            f.write("\n}")
            n1 -= 1


        while True:
            line = f.readline()
            if not line: break
            print(line, end='')
