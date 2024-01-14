import random
import tkinter
from typing import List, Type

import customtkinter
from tkinter import messagebox
import math
import sympy
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1000x800")
app.title("IA C1 A 1 Genetic Algorithms 01")
app.resizable(False, False)
opc = 0


def set_opc(number):
    global opc
    opc = number


def save_data():
    print("saving data...")

    data = [
        formula_text.get(),
        initial_pob_text.get(),
        resolution_text.get(),
        max_pob_text.get(),
        mut_ind_prob_text.get(),
        mut_gen_prob_text.get(),
        min_x_text.get(),
        max_x_text.get(),
        max_iteration_text.get(),
        opc
    ]

    if any(element == "" or element == 0 for element in data):
        print("error")
        messagebox.showerror("Error", "Por favor, complete toda la información.")
        return

    data[1:-1] = [float(x) for x in data[1:-1]]
    start(data)


def generate_chromosome(bits: int, size: int):
    list = []
    for i in range(size):
        num_aleatorio = random.randint(1, 2 ** bits - 1)
        representacion_binaria = bin(num_aleatorio)[2:].zfill(bits)
        list.append(representacion_binaria)
    return list


def get_number_bits():
    min_x = float(min_x_text.get())
    max_x = float(max_x_text.get())
    range = max_x - min_x
    jump_num = range / float(resolution_text.get())
    point_num = jump_num + 1
    return int(math.log2(point_num))


def get_number_from(binary: str):
    return int(binary, 2)


def get_x(num, bits):
    min_x = float(min_x_text.get())
    max_x = float(max_x_text.get())
    range = max_x - min_x
    return round(min_x + num * (range) / (2 ** bits - 1), 2)


def get_fx(x):
    try:
        result = eval(formula_text.get(), {'x': x})
        return round(result, 2)
    except Exception as e:
        print("error")
        print(e)


def get_gen(genome, size, bits):
    gen = []
    id = 0
    for e in genome:
        id = id + 1
        num = get_number_from(e)
        x = get_x(num, bits)
        fx = get_fx(num)
        gen.append([id, e, num, x, fx])
    if opc == 1:
        # menor a mayor
        gen0 = sorted(gen, key=lambda x: x[-1])
    elif opc == 2:
        # mayor a menor
        gen0 = sorted(gen, key=lambda x: x[-1], reverse=True)
    return gen0


def get_best_value(gen, element, opc):
    value = [row[element] for row in gen]
    return min(value) if opc == 1 else max(value)


def get_worst_value(gen, element, opc):
    value = [row[element] for row in gen]
    return max(value) if opc == 1 else min(value)


def get_media_value(gen, element):
    values = [row[element] for row in gen]
    media = sum(values) / len(values) if len(values) > 0 else None
    return round(media, 2)


def probability_function(prob):
    number = round(random.random(), 2)
    return number <= prob


def get_son(f1, f2, punto_cruza):
    s1 = f1[:punto_cruza] + f2[punto_cruza:]
    s2 = f2[:punto_cruza] + f1[punto_cruza:]
    return s1, s2


def reproduce(fathers, punto_cruza):
    sons = []
    if len(fathers) == 2:
        s1, s2 = get_son(fathers[0], fathers[0], punto_cruza)
        sons.append(s1)
        sons.append(s2)
    elif len(fathers) == 1:
        s1 = fathers[0]
        sons.append(s1)
        sons.append(s1)
    else:
        if len(fathers) % 2 == 1:
            s1, s2 = get_son(fathers[-1], fathers[-2], punto_cruza)
            sons.append(s1)
            sons.append(s2)
        else:
            for i in range(len(fathers)):
                for j in range(i + 1, len(fathers)):
                    s1, s2 = get_son(fathers[i], fathers[j], punto_cruza)
                    sons.append(s1)
                    sons.append(s2)

    return sons


def mutar_hijo(hijo):
    mut_ind_prob = float(mut_ind_prob_text.get())
    hijo_list = list(hijo)
    if probability_function(mut_ind_prob):
        for i in range(len(hijo_list)):
            mut_gen_prob = float(mut_gen_prob_text.get())
            if probability_function(mut_gen_prob):
                new_position = random.randint(0, len(hijo_list) - 1)
                hijo_list[i], hijo_list[new_position] = hijo_list[new_position], hijo_list[i]
    return ''.join(hijo_list)


def mutar_hijos(hijos):
    hijos_mutados = []
    for hijo in hijos:
        hijo_mutado = mutar_hijo(hijo)
        hijos_mutados.append(hijo_mutado)
    return hijos_mutados


def get_divition(gen):
    divition = len(gen) // 2 + len(gen) % 2
    div1 = gen[:divition]
    div2 = gen[divition:]
    return div1


def poda(gen):
    if opc == 1:
        # menor a mayor
        best_results = sorted(gen, key=lambda x: x[-1])[:int(initial_pob_text.get())]
    elif opc == 2:
        # mayor a menor
        best_results = sorted(gen, key=lambda x: x[-1], reverse=True)[:int(initial_pob_text.get())]
    while len(best_results) < int(max_pob_text.get()):
        best_results.append(gen[random.randint(0, len(gen) - 1)])
    return best_results


def start(data):
    #  id  |  binary | i    | x   | fx
    #  0   |   1     |  2   | 3  | 4
    size = int(initial_pob_text.get())
    bits = get_number_bits()
    chromosome = generate_chromosome(bits, size)
    # initial generation
    gen = get_gen(chromosome, size, bits)
    prev_gen = []
    prev_gen = gen
    coord_b_fx = []
    coord_w_fx = []
    coord_m_fx = []
    coord_b_x = []
    coord_w_x = []
    coord_m_x = []
    for i in range(int(max_iteration_text.get())):
        print("Iteration: ", i)
        print("Generation: ", gen)

        # aca falta get B W M de gen
        b_fx = get_best_value(gen, 4, opc)
        coord_b_fx.append([i, float(b_fx)])
        w_fx = get_worst_value(gen, 4, opc)
        coord_w_fx.append([i, float(w_fx)])
        m_fx = get_media_value(gen, 4)
        coord_m_fx.append([i, float(m_fx)])

        b_x = get_best_value(gen, 3, opc)
        coord_b_x.append([i, b_x])
        w_x = get_worst_value(gen, 3, opc)
        coord_w_x.append([i, w_x])
        m_x = get_media_value(gen, 3)
        coord_m_x.append([i, m_x])

        if len(gen) > int(max_pob_text.get()):
            print("borar excedentes")
            gen = poda(gen)
            print("nueva gen tras borrar: ", gen)
            # funcion clean gen
        # A3
        gen_usable_part = get_divition(gen)
        # C3
        chromosomes = [e[1] for e in gen_usable_part]
        chromosomes = reproduce(chromosomes, bits - 2)
        # M2
        chromosomes = mutar_hijos(chromosomes)
        new_gen = get_gen(chromosomes, size, bits)
        gen = prev_gen + new_gen
        if opc == 1:
            # menor a mayor
            gen = sorted(gen, key=lambda x: x[-1])
        elif opc == 2:
            # mayor a menor
            gen = sorted(gen, key=lambda x: x[-1], reverse=True)
        prev_gen = new_gen
    ax.plot(*zip(*coord_b_fx), label="Best fx", color="blue")
    ax.plot(*zip(*coord_w_fx), label="Worst fx", color="red")
    ax.plot(*zip(*coord_m_fx), label="Media fx", color="green")
    ax.legend()
    canvas.draw()

    ax2.plot(*zip(*coord_b_x), label="Best x", color="blue")
    ax2.plot(*zip(*coord_w_x), label="Worst x", color="red")
    ax2.plot(*zip(*coord_m_x), label="Media x", color="green")
    ax2.legend()
    canvas2.draw()


mFrame1 = customtkinter.CTkFrame(master=app, width=450, height=700)

masterFrame1 = customtkinter.CTkFrame(master=mFrame1, width=430, height=70, fg_color="transparent")

frame = customtkinter.CTkFrame(master=masterFrame1, width=430, height=20, fg_color="transparent")
customtkinter.CTkLabel(master=frame, text="Formula", width=430, ).pack(fill="x", expand=True)
frame.pack(side="top", fill="x", expand=True)

frame1 = customtkinter.CTkFrame(master=masterFrame1, width=300, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame1, text="f(x)", width=100).pack(side="left")
formula_text = customtkinter.CTkEntry(master=frame1, width=200)
formula_text.pack()
frame1.pack(padx=10, pady=5, side="left")

frame2 = customtkinter.CTkFrame(master=masterFrame1, width=130, height=70, fg_color="transparent")
minBttn = customtkinter.CTkButton(master=frame2, text="minimo", command=lambda: set_opc(1)).pack(pady=5)
maxBttn = customtkinter.CTkButton(master=frame2, text="maximo", command=lambda: set_opc(2)).pack(pady=5)
frame2.pack(padx=10, pady=10, side="left")

masterFrame1.pack(fill="x", padx=10, pady=10)

masterFrame1_1 = customtkinter.CTkFrame(master=mFrame1, width=430, height=70, fg_color="transparent")
frame1_1 = customtkinter.CTkFrame(master=masterFrame1_1, width=430, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame1_1, text="Resolucion", width=430).pack(fill="x", expand=True)
frame1_1.pack(side="top", fill="x", expand=True)

frame1_2 = customtkinter.CTkFrame(master=masterFrame1_1, width=430, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame1_2, text="Resolucion", width=215).pack(side="left")
resolution_text = customtkinter.CTkEntry(master=frame1_2, width=215)
resolution_text.pack()
frame1_2.pack(padx=10, pady=5, side="left")

masterFrame1_1.pack(fill="x", padx=10, pady=10)

masterFrame2 = customtkinter.CTkFrame(master=mFrame1, width=430, height=70, fg_color="transparent")

frame3 = customtkinter.CTkFrame(master=masterFrame2, width=430, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame3, text="Población", width=430, ).pack(fill="x", expand=True)
frame3.pack(side="top", fill="x", expand=True)

frame4 = customtkinter.CTkFrame(master=masterFrame2, width=200, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame4, text="Inicial", width=100).pack(side="left")
initial_pob_text = customtkinter.CTkEntry(master=frame4, width=100)
initial_pob_text.pack()
frame4.pack(padx=10, pady=5, side="left")

frame5 = customtkinter.CTkFrame(master=masterFrame2, width=200, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame5, text="Maxima", width=100).pack(side="left")
max_pob_text = customtkinter.CTkEntry(master=frame5, width=100)
max_pob_text.pack()
frame5.pack(padx=10, pady=5, side="left")

masterFrame2.pack(fill="x", padx=10, pady=10)

masterFrame3 = customtkinter.CTkFrame(master=mFrame1, width=430, height=70, fg_color="transparent")

frame6 = customtkinter.CTkFrame(master=masterFrame3, width=430, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame6, text="Mutacion", width=430, ).pack(fill="x", expand=True)
frame6.pack(side="top", fill="x", expand=True)

frame7 = customtkinter.CTkFrame(master=masterFrame3, width=200, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame7, text="% Individuo", width=100).pack(side="left")
mut_ind_prob_text = customtkinter.CTkEntry(master=frame7, width=100)
mut_ind_prob_text.pack()
frame7.pack(padx=10, pady=5, side="left")

frame8 = customtkinter.CTkFrame(master=masterFrame3, width=200, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame8, text="% Gen", width=100).pack(side="left")
mut_gen_prob_text = customtkinter.CTkEntry(master=frame8, width=100)
mut_gen_prob_text.pack()
frame8.pack(padx=10, pady=5, side="left")

masterFrame3.pack(fill="x", padx=10, pady=10)

masterFrame4 = customtkinter.CTkFrame(master=mFrame1, width=430, height=70, fg_color="transparent")

frame9 = customtkinter.CTkFrame(master=masterFrame4, width=430, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame9, text="Rango de soluciones", width=430, ).pack(fill="x", expand=True)
frame9.pack(side="top", fill="x", expand=True)

frame10 = customtkinter.CTkFrame(master=masterFrame4, width=200, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame10, text="X Min.", width=100).pack(side="left")
min_x_text = customtkinter.CTkEntry(master=frame10, width=100)
min_x_text.pack()
frame10.pack(padx=10, pady=5, side="left")

frame11 = customtkinter.CTkFrame(master=masterFrame4, width=200, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame11, text="X Max.", width=100).pack(side="left")
max_x_text = customtkinter.CTkEntry(master=frame11, width=100)
max_x_text.pack()
frame11.pack(padx=10, pady=5, side="left")

masterFrame4.pack(fill="x", padx=10, pady=10)

masterFrame5 = customtkinter.CTkFrame(master=mFrame1, width=430, height=70, fg_color="transparent")

frame12 = customtkinter.CTkFrame(master=masterFrame5, width=430, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame12, text="Criterio de Finalización", width=430, ).pack(fill="x", expand=True)
frame12.pack(side="top", fill="x", expand=True)

frame13 = customtkinter.CTkFrame(master=masterFrame5, width=430, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame13, text="Iteraciones", width=215).pack(side="left")
max_iteration_text = customtkinter.CTkEntry(master=frame13, width=215)
max_iteration_text.pack()
frame13.pack(padx=10, pady=5, side="left")

masterFrame5.pack(fill="x", padx=10, pady=10)

button = customtkinter.CTkButton(master=mFrame1, text="Start Genetic Algorithm", command=save_data, width=200)
button.pack(padx=10, pady=20)

mFrame1.pack(side="left", fill="y")

mFrame2 = customtkinter.CTkFrame(master=app, width=550, height=700, fg_color="transparent")
new_frame = customtkinter.CTkFrame(master=mFrame2, width=550, height=100)
fig, ax = plt.subplots()  # Create the figure and axes
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=new_frame)
canvas.get_tk_widget().pack()
ax.set_xlabel("Generation")
ax.set_ylabel("Value")
canvas.draw()
new_frame.pack(pady=10, expand=False)

new_frame2 = customtkinter.CTkFrame(master=mFrame2, width=550, height=100)
fig2, ax2 = plt.subplots()  # Create the figure and axes
canvas2 = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig2, master=new_frame2)
canvas2.get_tk_widget().pack()
ax2.set_xlabel("Generation")
ax2.set_ylabel("Value")
canvas2.draw()
new_frame2.pack(pady=10)
mFrame2.pack(padx=10, expand=False)
app.mainloop()
