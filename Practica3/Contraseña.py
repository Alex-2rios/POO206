while True:
    c = input("Contraseña: ")

    if len(c) < 10:
        print("Contraseña demasiado corta")
        continue

    if not any(d.isdigit() for d in c):
        print("Debe tener al menos un número")
        continue

    if not any(ch in "@#%*" for ch in c):
        print("Debe tener al menos un carácter especial")
        continue

    print("Contraseña válida")
    break
