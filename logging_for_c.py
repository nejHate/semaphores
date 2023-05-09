"""
This script will read a file you specified on input and 
it will write a logging function on each line
! note that this program create temporary file
logging_output.temp (which will be deleted) and output 
file logging_output.c so don't have this files
in folder ot it will rewrite them
after finish you can compile logging_output.c and run them
if the compilation failed, please delete mentioned lines
the program isn't that smart so it can write the function
where it shouldn't
"""

import re
import os

filein = open(input("write a name of file you want to log (write ./name_of_file.file_extension): "), "r")
fileout1 = open("logging_output.temp", "w")
fileout2 = open("logging_output.c", "w")


"""while (True):
  line1 = filein.readline()
  if (line1.startswith("#include")):
    fileout1.write(line1)
  else:
    break"""

#fileout1.write("toto je debugovací funkce\n")

line1 = filein.readline()

while True:
  if line1 == "":
    break
  if line1.isspace():
    line1 = filein.readline()
  else:
    fileout1.write(line1)
    line1 = filein.readline()
fileout1.close()
filein.close()

fileout1 = open("logging_output.temp", "r")
line1 = fileout1.readline()

while True:
  if(re.match(r"#include *<.*>", line1) != None):
    fileout2.write(line1)
    line1 = fileout1.readline()
  else:
    break

fileout2.write("\n\
sem_t *log_sem;\n\
void logfun(int line, char *text){\n\
  sem_wait(log_sem);\n\
  FILE *logfunfile = fopen(\"logfun_out.txt\", \"a\");\n\
  fprintf(logfunfile, \"%d, %s\\n\", line, text);\n\
  fclose(logfunfile);\n\
  sem_post(log_sem);\n\
  return;\n\
}\n")

main = 0

while(True):
  if not line1.endswith("\n"):
    fileout2.write(line1)
    break
  spacelen = re.match(r" *", line1).span()
  spacelen = spacelen[1] - spacelen[0]
  fileout2.write(line1)
  if(re.match(r" *} *\n", line1) != None):
    line1 = fileout1.readline()
    continue
  if(re.match(r" *//.*", line1) != None):
    line1 = fileout1.readline()
    continue
  if(re.match(r"int main\(", line1) != None):
    fileout2.write("  sem_unlink(\"log_sem\");\n")
    fileout2.write("  log_sem = sem_open(\"log_sem\", O_CREAT | O_EXCL, 0644, 1);\n")
    line1 = fileout1.readline()
    continue
  line1 = re.sub(r'\\', r'\\\\', line1)
  line1 = re.sub(r'"', r'\"', line1)
  fileout2.write(" "*spacelen + 'logfun(__LINE__, "{}");\n'.format(line1[0+spacelen:len(line1)-1]))
  line1 = fileout1.readline()
  

fileout1.close()
fileout2.close()

try:
    os.remove("./logging_output.temp")
except OSError as e:
    print(f"Error deleting file: {e}")