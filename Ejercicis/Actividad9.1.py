def main():
    aficions=[]
    valor=input(" Añadir aficion ")
    contador=0
    while contador<2:
        aficions.append(valor)
        contador=contador + 1
        valor=input(" Añadir")
    else:
        print("fin")

    print('\n'.join(map(str, aficions))) 

if __name__ == "__main__":
    main()