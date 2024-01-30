 import sys




if __name__== "__main__":


   numero = len(sys.argv) -1

if numero>3:
   print("mes de 3")
else:
   print("be")

for i in range(1,numero + 1):
   print("Argument",i,sys.argv[i])


