#! python
# Lottoziehung.py simuliert den Ablauf einer Lottoziehung

import random
from random import shuffle

Lottozahlen = []
Gewinnzahlen = []

for i in range(1, 50):
    Lottozahlen.append(i)

for i in range(1, 7):
    shuffle(Lottozahlen)
    Gewinnzahl = Lottozahlen.pop(0)
    Gewinnzahlen.append(Gewinnzahl)

Gewinnzahlen.sort()
print(Gewinnzahlen)