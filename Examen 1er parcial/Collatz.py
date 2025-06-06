while True:
    try:
        num = int(input("Numero entero: "))
        
        if num <= 0:
            print("El numero debe ser positivo")
            continue
        print("Collatz:")
        while num != 1:
            print(num, end=", ")
            if num % 2 == 0:  
                num //= 2
            else:  
                num = num * 3 + 1
        print(1)  
        break
    except ValueError:
        print("introduce un numero valido")
        continue

    