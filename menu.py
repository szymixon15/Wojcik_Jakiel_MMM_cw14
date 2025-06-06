from euler import wyznacz_odpowiedz
import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#funkcja wywolujaca odczytanie zmiennych i uruchomienie funkcji wyznaczajacej odpowiedz
def funkcja():

    a1 = float(entrya1.get())
    a0 = float(entrya0.get())
    b2 = float(entryb2.get())
    b1 = float(entryb1.get())
    b0 = float(entryb0.get())

    c2 = float(entryc2.get())
    c1 = float(entryc1.get())
    c0 = float(entryc0.get())
    d2 = float(entryd2.get())
    d1 = float(entryd1.get())
    d0 = float(entryd0.get())

    l3 = a1 * c2
    l2 = a1 * c1 + a0 * c2
    l1 = a1 * c0 + a0 * c1
    l0 = a0 * c0

    licznik_oryginalny = [l3, l2, l1, l0]
    licznik = list(licznik_oryginalny) # Kopia do modyfikacji


    d4 = b2 * d2
    d3 = b2 * d1 + b1 * d2 + a1 * c2
    d2 = b2 * d0 + b1 * d1 + b0 * d2 + a1 * c1 + a0 * c2
    d1 = b1 * d0 + b0 * d1 + a1 * c0 + a0 * c1
    d0 = b0 * d0 + a0 * c0
    mianownik_oryginalny = [d4, d3, d2, d1, d0]
    mianownik = list(mianownik_oryginalny) # Kopia do modyfikacji


    rzad = 4



    if abs(mianownik[0]) < 1e-8:
        messagebox.showinfo("Informacja", "Wykryto układ 3 rzędu.")
        #licznik = licznik[1:]
        mianownik = mianownik[1:]
        rzad = 3
        if abs(mianownik[0]) < 1e-8:
            messagebox.showinfo("Informacja", "Wykryto układ 2 rzędu.")
            #licznik = licznik[1:]
            mianownik = mianownik[1:]
            rzad = 2
            if abs(mianownik[0]) < 1e-8:
                messagebox.showinfo("Informacja", "Wykryto układ 1 rzędu.")
                #licznik = licznik[1:]
                mianownik = mianownik[1:]
                rzad = 1
                if abs(mianownik[0]) < 1e-8:
                    messagebox.showerror("Błąd", "Mianownik jest zerowy. Nie można wyznaczyć odpowiedzi.")
                    return

    zakres = float(entryzakres0.get()), float(entryzakres1.get())

    y,u,t = wyznacz_odpowiedz(licznik,mianownik,rzad,float(entryczastrwania.get()),float(entryczasprobki.get()),pobudzenie.get(),float(entryczestotliwosc.get()),zakres)

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(t, u, label='Pobudzenie u(t)', linestyle='--')
    ax.plot(t, y, label='Odpowiedź y(t)')
    ax.set_xlabel('Czas [s]')
    ax.set_ylabel('Wyjście')
    ax.set_title(f'Odpowiedź układu {rzad} rzędu – metoda Eulera')
    ax.grid()
    ax.legend()
    canvas_matplotlib = FigureCanvasTkAgg(fig, master=root)
    canvas_matplotlib.draw()
    canvas_matplotlib.get_tk_widget().place(relx=0.5, rely=0.75, anchor="center")

    podmianka_okno = """
    plt.clf()
    plt.plot(t, u, label='Pobudzenie u(t)', linestyle='--')
    plt.plot(t, y, label='Odpowiedź y(t)')
    plt.xlabel('Czas [s]')
    plt.ylabel('Wyjście')
    plt.title('Odpowiedź układu – metoda Eulera')
    plt.grid()
    plt.legend()
    plt.show()
    """


#implementacja okna i canvas
root = Tk()
root.title("Symulator odpowiedzi ukladu")
root.resizable(False, False)
canvas = Canvas(root, width = 800, height = 950, bg = "light gray")
canvas.pack()


#Wybor ksztaltu pobudzenia
pobudzenie = IntVar()
#Domyślnie zaznaczony Sinus
pobudzenie.set(1) # 1 dla Sinusa

rb1 = Radiobutton(root, text="Sinus", variable=pobudzenie, value=1)
rb2 = Radiobutton(root, text="Trojkat", variable=pobudzenie, value=2)
rb3 = Radiobutton(root, text="Prostokat", variable=pobudzenie, value=3)

canvas.create_window(70, 400, window=rb1)
canvas.create_window(74, 430, window=rb2)
canvas.create_window(81, 460, window=rb3)



#teksty
canvas.create_text(590, 65, text="Transmitancja obiektu", font=("Arial", 14), fill="black")
canvas.create_text(330, 65, text="Transmitancja sterownika", font=("Arial", 14), fill="black")
canvas.create_text(100, 360, text="Kształt pobudzenia", font=("Arial", 14), fill="black")
canvas.create_text(280, 360, text="Czas pobudzenia", font=("Arial", 14), fill="black")
canvas.create_text(278, 430, text="Częstotliwość", font=("Arial", 14), fill="black")
canvas.create_text(500, 360, text="Czas trwania symulacji", font=("Arial", 14), fill="black")
canvas.create_text(500, 430, text="Długość jednej próbki", font=("Arial", 14), fill="black")
canvas.create_text(527, 395, text="s", font=("Arial", 14), fill="black")
canvas.create_text(527, 465, text="s", font=("Arial", 14), fill="black")
canvas.create_text(308, 466, text="Hz", font=("Arial", 14), fill="black")
canvas.create_text(280, 394, text="[         ,         ]s", font=("Arial", 14), fill="black")


#wejscia transmitancji
#obiekt
#licznik
entrya1 = Entry(root, width = 5)
canvas.create_window(550,155, window=entrya1)
entrya0 = Entry(root, width = 5)
canvas.create_window(625,155, window=entrya0)
#mianownik
entryb2 = Entry(root, width = 5)
canvas.create_window(517,209, window=entryb2)
entryb1 = Entry(root, width = 5)
canvas.create_window(598,209, window=entryb1)
entryb0 = Entry(root, width = 5)
canvas.create_window(672,209, window=entryb0)

#sterownik
#licznik
entryc2 = Entry(root, width = 5)
canvas.create_window(252,154, window=entryc2)
entryc1 = Entry(root, width = 5)
canvas.create_window(335,154, window=entryc1)
entryc0 = Entry(root, width = 5)
canvas.create_window(408,154, window=entryc0)
#mianownik
entryd2 = Entry(root, width = 5)
canvas.create_window(252,208, window=entryd2)
entryd1 = Entry(root, width = 5)
canvas.create_window(335,208, window=entryd1)
entryd0 = Entry(root, width = 5)
canvas.create_window(408,208, window=entryd0)


#entry dla parametrow sygnalu pobudzajacego 
entryzakres0 = Entry(root, width = 5)
canvas.create_window(250,395, window=entryzakres0)

entryzakres1 = Entry(root, width = 5)
canvas.create_window(300,395, window=entryzakres1)

entryczestotliwosc = Entry(root, width = 5)
canvas.create_window(275,465, window=entryczestotliwosc)


#entry dla czasu (czas trwania symulacji oraz czas trwania próbki)

entryczastrwania = Entry(root, width = 5)
canvas.create_window(500,395, window=entryczastrwania)

entryczasprobki = Entry(root, width = 5)
canvas.create_window(500,465, window=entryczasprobki)


#entry - default values

# Ustawienie domyślnych wartości

# Transmitancja obiektu: 1/(s^2 + s +1 )
entrya1.insert(0, "0")
entrya0.insert(0, "1")

entryb2.insert(0, "1")
entryb1.insert(0, "1")
entryb0.insert(0, "1")

# Transmitancja sterownika: (s+2)/(s^2 + 2s + 2)
entryc2.insert(0, "0")
entryc1.insert(0, "1")
entryc0.insert(0, "2")

entryd2.insert(0, "1")
entryd1.insert(0, "2")
entryd0.insert(0, "2")

# Czas pobudzenia: [0 , 10] s
entryzakres0.insert(0, "0")
entryzakres1.insert(0, "10")

# Częstotliwość: 0.5 Hz
entryczestotliwosc.insert(0, "0.5")

# Czas trwania symulacji: 10 s
entryczastrwania.insert(0, "10")

# Długość jednej próbki: 0.01 s
entryczasprobki.insert(0, "0.01")


# tlo - uklad

img = Image.open("C:/Users/szyme/Desktop/sem4/MMMy projekt/uklad.png")
img = img.resize((777, 246))
photo = ImageTk.PhotoImage(img)
canvas.create_image(400,200,anchor = "center", image=photo)


#button - start

przycisk = Button(root, text="Start symulacji", command=funkcja, bg="lightblue", fg="black", font=("Arial", 14, "bold"))

canvas.create_window(700, 420, window=przycisk, width=150, height=100)

root.mainloop()