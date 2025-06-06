import numpy as np
from scipy import signal

def wyznacz_odpowiedz(num, den, rzad, czas_trwania_symulacji, czas_trwania_probki, pobudzenie, czestotliwosc, zakres):

    # w tym miejscu mamy gotowy licznik i mianownik naszej finalnej transmitancji dla ktorej musimy eulerem obliczyc odpowiedz

    N = int(czas_trwania_symulacji/czas_trwania_probki)
    Ts = czas_trwania_probki
    t = np.arange(N) * Ts
    u = np.zeros(N)

    
    if pobudzenie == 1:  #pobudzenie sinusoidalne
        u = np.sin(2 * np.pi * czestotliwosc * t) 
        u[(t < zakres[0]) | (t > zakres[1])] = 0
    elif pobudzenie == 2:  #pobudzenie trojkatne
        u = signal.sawtooth(2 * np.pi * czestotliwosc * t, width=0.5)
        u[(t < zakres[0]) | (t > zakres[1])] = 0
    elif pobudzenie == 3:  #pobudzenie prostokatne o sk. czasie trwania
        u = (signal.square(2 * np.pi * czestotliwosc * t) + 1) / 2
        u[(t < zakres[0]) | (t > zakres[1])] = 0


    y = np.zeros(N)
    dy = np.zeros(N)
    d2y = np.zeros(N)
    d3y = np.zeros(N)
    d4y = np.zeros(N)

    du = np.zeros(N)
    d2u = np.zeros(N)
    d3u = np.zeros(N)

    for k in range(1, N):
        du[k] = (u[k] - u[k-1]) / Ts
    for k in range(2, N):
        d2u[k] = (du[k] - du[k-1]) / Ts
    for k in range(3, N):
        d3u[k] = (d2u[k] - d2u[k-1]) / Ts



    if rzad == 4:
        for k in range(4, N):
            d4y[k] = (1 / den[0]) * (
                num[0] * d3u[k] + num[1] * d2u[k] + num[2] * du[k] + num[3] * u[k] - den[1] * d3y[k - 1] - den[2] * d2y[k - 1] - den[3] * dy[k - 1] - den[4] * y[k - 1]
            )
            d3y[k] = d3y[k - 1] + Ts * d4y[k]
            d2y[k] = d2y[k - 1] + Ts * d3y[k]
            dy[k] = dy[k - 1] + Ts * d2y[k]
            y[k] = y[k - 1] + Ts * dy[k]
    elif rzad == 3:
        for k in range(3, N):
            d3y[k] = (1 / den[0]) * (
                num[0] * d3u[k] + num[1] * d2u[k] + num[2] * du[k] + num[3] * u[k] - den[1] * d2y[k - 1] - den[2] * dy[k - 1] - den[3] * y[k - 1]
            )
            d2y[k] = d2y[k - 1] + Ts * d3y[k]
            dy[k] = dy[k - 1] + Ts * d2y[k]
            y[k] = y[k - 1] + Ts * dy[k]
    elif rzad == 2:
        for k in range(2, N):
            d2y[k] = (1 / den[0]) * (
                num[0] * d3u[k] + num[1] * d2u[k] + num[2] * du[k] + num[3] * u[k] - den[1] * dy[k - 1] - den[2] * y[k - 1]
            )
            dy[k] = dy[k - 1] + Ts * d2y[k]
            y[k] = y[k - 1] + Ts * dy[k]
    elif rzad == 1:
        for k in range(1, N):
            dy[k] = (1 / den[0]) * (
                num[0] * d3u[k] + num[1] * d2u[k] + num[2] * du[k] + num[3] * u[k] - den[1] * y[k - 1]
            )
            y[k] = y[k - 1] + Ts * dy[k]

    return y,u,t
