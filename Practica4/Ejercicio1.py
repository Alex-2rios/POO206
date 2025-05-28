while True:
    try:
        num = int(input("Número mayor que 10: "))
        if num <= 10:
            print("Debe ser mayor que 10")
            continue

        for i in range(3, num + 1, 2):
            print(i, end=", " if i < num else "\n")
        break
    except:
        print("Introduce un número valido")
        continue
