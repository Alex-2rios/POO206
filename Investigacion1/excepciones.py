try:
    entrada = input("Escribe un número: ")
    numero = int(entrada)
    print("Doble del número:", numero * 2)
except (ValueError, TypeError):
    print("Error: Solo puedes escribir números.")
