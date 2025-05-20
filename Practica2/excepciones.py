try:
    numero = int(input("Introduce un número: "))
    resultado = 10 / numero

    print("El resultado es:", resultado)

except ZeroDivisionError:
    print("Error: No se puede dividir entre cero.")
except ValueError:
    print("Error: Debes introducir un número entero.")