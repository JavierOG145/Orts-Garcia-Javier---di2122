import random
import sys

class Error (Exception):
    """Clase Error"""
    pass
class ValorMenor(Error):
    """Error Valor Menor"""
    pass

class ValorMayor(Error):
    """Error Valor Mayor"""
    pass

numero_aleatorio = random.randint(0,100)
print(numero_aleatorio)
while True:
    try:
        numero  = input("Introduzca un numero: ")
        if int(numero) < numero_aleatorio:
            raise ValorMenor
        elif int(numero) > numero_aleatorio:
            raise ValorMayor
        break
    except ValorMenor:
        print("Valor Menor")
    except ValorMayor:
        print("Valor Mayor")        
print("FELICIDADES")

