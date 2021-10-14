import os
import sys


def write():
    try:
        with open(os.path.join("test.txt"), "r+") as f:
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
                    resultado = lambda x, x2: x+x2
                    print(num, sig, num2, "=", resultado(
                    int(numero1), int(numero2)))
                if signo == "-":
                    resultado = lambda x, x2: x-x2
                    print(num, sig, num2, "=", resultado(
                    int(numero1), int(numero2)))
                if signo == "*":
                    resultado = lambda x, x2: x*x2
                    print(num, sig, num2, "=", resultado(
                    int(numero1), int(numero2)))
                if signo == "/":
                    resultado = lambda x, x2: x/x2
                    print(num, sig, num2, "=", resultado(
                    int(numero1), int(numero2)))

    except ValueError:
            print("Valor no correcto")
    except IndexError:
            print("Hay un espacio")
    
write()
