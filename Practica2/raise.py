while True:
    try:
        nombre = input("Escribe tu nombre: ")
        if nombre == "":
            raise ValueError("El nombre no puede estar vacío")
        print("Hola, " + nombre + "!")
        break
    except ValueError as e:
        print("Error:", e, "Intenta de nuevo.")
