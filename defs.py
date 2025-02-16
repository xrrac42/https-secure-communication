import json

def soma(x: int, y: int) -> float:
    return x + y

def subtracao(x: int, y: int) -> float:
    return x - y

def multiplicacao(x: int, y: int) -> float:
    return x * y

def divisao(x: int, y: int) -> float:
    if y == 0:
        raise ValueError("Divisão por zero não permitida.")
    return x / y
