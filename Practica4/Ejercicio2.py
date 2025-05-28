while True:
    try:
        num = int(input("Número positivo: "))
        if num < 0:
            print("Debe ser positivo")
            continue
        for i in range(num, -1, -1):
            print(i, end=", " if i > 0 else "\n")
        break
    except:
        print("Introduce un número válido")
        continue
