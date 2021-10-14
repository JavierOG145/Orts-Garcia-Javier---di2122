import os
import sys


def write():
    try:
        with open(os.path.join("test.txt"), "r+") as f,  \
            open(os.path.join("result.txt"),"a") as r:
        
            for linea in f:
                numero = linea.split(" ")
                numero1 = numero[0]
                temp = numero1.split()
                num = temp[0]

                signo = numero[1]
                temp = signo.split()
                sig = temp[0]

                numero2 = numero[2]
                temp = numero2.split()
                num2 = temp[0]

                if signo == "+":
                    def resultado(x, x2): return x+x2
                    print(num, sig, num2, "=", resultado(
                        int(numero1), int(numero2)))
                    r.write(num + sig + num2 + "=" + str(resultado(
                        int(numero1), int(numero2)))+"\n")
                if signo == "-":
                    def resultado(x, x2): return x-x2
                    print(num, sig, num2, "=", resultado(
                        int(numero1), int(numero2)))
                    r.write(num + sig + num2 + "=" + str(resultado(
                        int(numero1), int(numero2)))+"\n")
                if signo == "*":
                    def resultado(x, x2): return x*x2
                    print(num, sig, num2, "=", resultado(
                        int(numero1), int(numero2)))
                    r.write(num + sig + num2 + "=" + str(resultado(
                        int(numero1), int(numero2)))+"\n")
                if signo == "/":
                    def resultado(x, x2): return x/x2
                    print(num, sig, num2, "=", resultado(
                        int(numero1), int(numero2)))
                    r.write(num + sig + num2 + "=" + str(resultado(
                        int(numero1), int(numero2)))+"\n")

    except ValueError:
            print("Valor no correcto")
    except IndexError:
            print("Hay un espacio")
    
write()
