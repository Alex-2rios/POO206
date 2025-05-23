while True:
    try:
        
        n = int(input("Escribe un número:"))
        if n % 2 == 0:
            print("El número es par")
        else:
            print("El número es impar") 
        break
    except:
        print("Error: Solo puedes escribir números.")
