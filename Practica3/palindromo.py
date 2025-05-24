while True:
    c = input("Cadena: ")
    if c == "":
        print("Error: No puede estar vacía.")
        continue
    c = c.replace(" ", "").lower()
    if c == c[::-1]:
        print("Es palindromo")
    else:
        print("No es palindromo")
    break
