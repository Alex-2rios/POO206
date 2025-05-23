while True:
    try:
        
        n = int(input("Introduce un año:"))
        if n <=0:
            print("El numero no puede ser cero ni negativo")
            continue
        if n % 4 == 0:
            print("El año es bisiesto.")
        else:
            print("El año no es bisiesto") 
        break
    except:
        print("Error: Debes escribir un año válido (número entero).")