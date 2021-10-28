import os
import sys

directory_carpeta = os.path.dirname(__file__)
ruta_test = os.path.join(directory_carpeta,"test.txt")
ruta_result = os.path.join(directory_carpeta,"result.txt")


def write():
    try:
        with open(ruta_test, "r+") as f,  \
            open(ruta_result,"a") as r:
        
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
    except FileNotFoundError:
        print("No exite el archivo")
    
write()
