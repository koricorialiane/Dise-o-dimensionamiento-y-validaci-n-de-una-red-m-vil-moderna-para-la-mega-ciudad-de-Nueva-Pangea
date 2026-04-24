import math

# Parámetros comunes
f = 2600  # MHz
hb = 30   # m
hm = 1.5  # m
d = 1     # km
Pt = 43   # dBm
Gt = 15   # dBi
Gr = 0    # dBi
S = -100  # dBm

# Función Okumura-Hata
def okumura_hata(f, hb, hm, d):
    a_hm = 3.2 * (math.log10(11.75 * hm))**2 - 4.97
    log_f = math.log10(f)
    log_hb = math.log10(hb)
    log_d = math.log10(d)
    pl = 69.55 + 26.16 * log_f - 13.82 * log_hb - a_hm + (44.9 - 6.55 * log_hb) * log_d
    return pl

pl = okumura_hata(f, hb, hm, d)
pr = Pt + Gt + Gr - pl

print(f"Pérdida de propagación: {pl:.2f} dB")
print(f"Potencia recibida: {pr:.2f} dBm")
print(f"Sensibilidad: {S} dBm")
print("Cobertura OK" if pr >= S else "Cobertura insuficiente")

# Para Erlang, función de bloqueo
def erlang_b(a, u):
    sum_k = sum(a**k / math.factorial(k) for k in range(u+1))
    return (a**u / math.factorial(u)) / sum_k

# Ejemplo: A=10 Erlang, u=5 canales
a = 10
u = 5
b = erlang_b(a, u)
print(f"Probabilidad de bloqueo: {b:.4f}")