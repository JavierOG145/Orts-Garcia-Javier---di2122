lista = list(range(1,100))

def par(lista):
    if lista%2==0:
        return True
    return False
def impar(lista):
    if lista%2!=0:
        return True
    return False

numeros_pares_filtrado = filter(par,lista)
numeros_pares=list(numeros_pares_filtrado)

numeros_impares_filtrado = filter(impar,lista)
numeros_impares=list(numeros_impares_filtrado)

print("Numeros pares")
print(numeros_pares)

print("Numeros impares")
print(numeros_impares)