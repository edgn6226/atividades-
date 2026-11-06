n = [5, 3, 8, 3, 1, 9]
qunatia = len(n)

def moda():
  moda = 0
  voltas = 0
  indedice = 0
  for quantidade in n:
    a = n.count(quantidade)
    if a > moda:
      moda = a
      indedice = voltas
    voltas += 1  
  print(f"moda = {n[indedice]}")

def media():
  total = 0
  for soma in n:
    total = total + soma
  print(f"media = {total/qunatia:.2f}")

def mediana():
  n.sort()
  if qunatia % 2 == 0:

    metade = qunatia // 2
    numero2 = n[metade]
    numero1 = n[metade - 1]
    resultado_mediana = (numero1 + numero2) / 2
  else:
    posicao = qunatia // 2
    resultado_mediana = n[posicao]
  
  print(f"mediana = {resultado_mediana}")

moda()
media()
mediana()
