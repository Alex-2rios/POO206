try:
    numero = int(input("Escribe un número: "))
    resultado = 10 / numero
    print("Resultado:", resultado)
except ZeroDivisionError:
    print("Error: No puedes dividir entre cero")
except ValueError:
    print("Error: Eso no es un número")
finally:
    print("Vuelva a intentarlo")
