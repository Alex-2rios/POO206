while True:
    try:
        frase = input("Introduce una frase: ").strip()
        if frase == "":
            print("La frase no puede estar vacía.")
            continue

        letra = input("Introduce una letra: ").strip()
        if len(letra) != 1 or not letra.isalpha():
            print("Debes introducir exactamente una letra.")
            continue

        count = 0
        for c in frase:
            if c.lower() == letra.lower():
                count += 1

        print(f"La letra '{letra}' aparece {count} veces en la frase.")
        break
    except:
        print("Ocurrió un error, intenta de nuevo.")
        continue
