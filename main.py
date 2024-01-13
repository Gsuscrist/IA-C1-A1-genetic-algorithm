import random

import customtkinter
from tkinter import messagebox
import math
import sympy

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("450x600")
app.title("IA C1 A 1 Genetic Algorithms 01")
app.resizable(False, True)
opc = 0


def set_opc(number):
    global opc
    opc = number


def save_data():
    print("saving data...")
    data = [
        formula_text.get(),
        initial_pob_text.get(),
        max_pob_text.get(),
        mut_ind_prob_text.get(),
        mut_gen_prob_text.get(),
        min_x_text.get(),
        max_x_text.get(),
        max_iteration_text.get(),
        fitness_por_text.get(),
        opc
    ]

    if any(element == "" or element == 0 for element in data):
        print("error")
        messagebox.showerror("Error", "Por favor, complete toda la información.")
        return

    data[1:-1] = [float(x) for x in data[1:-1]]
    start(data)


def evaluate_function(x):
    try:
        # replace x with value
        result = eval(formula_text.get(), {'x': x})
        return round(result, 2)
    except Exception as e:
        print("error")
        print(e)


def get_binary_number(num, bits):
    if num == 0:
        return "0" * bits
    bin_num = ""

    while num > 0:
        bin_num = str(num % 2) + bin_num
        num //= 2

    if len(bin_num) < bits:
        bin_num = "0" * (bits - len(bin_num)) + bin_num

    return bin_num


def get_delta_x():
    min_x = int(min_x_text.get())
    max_x = int(max_x_text.get())
    num = max_x - min_x
    num = num if num >= 0 else -num
    return num


def get_num_jumps():
    delta_x = get_delta_x()
    return delta_x / float(fitness_por_text.get())


def get_x_number(num, bits):
    # replace 5 with a number of bits for the
    min_x = float(min_x_text.get())
    delta_x = get_delta_x()
    if min_x <0 :
        min_x=-min_x
    x = min_x + num * (delta_x / (2 ** bits - 1))
    return round(x, 3)


def generate_number(max_num):
    delta_x = get_delta_x()
    return random.randint(1, delta_x)


def get_initial_pob():
    initial_pob = []
    id = 0
    jumps = get_num_jumps()
    bits = math.ceil(math.log2(jumps)) + 1
    for element in range(int(initial_pob_text.get())):
        id = id + 1
        i = generate_number(jumps)
        binary = get_binary_number(i, bits-1)
        x = get_x_number(i, bits-1)
        fx = evaluate_function(x)
        initial_pob.append([id, binary, i, x, fx])
    return initial_pob


def start(data):
    pob = []
    #  id  |  binary | i    | x   | fx
    #  0   |   1     |  2   | 3  | 4
    pob = get_initial_pob()

    print(pob)
    print(len(pob))

masterFrame1 = customtkinter.CTkFrame(master=app, width=430, height=70)

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

masterFrame2 = customtkinter.CTkFrame(master=app, width=430, height=70)

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

masterFrame3 = customtkinter.CTkFrame(master=app, width=430, height=70)

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

masterFrame4 = customtkinter.CTkFrame(master=app, width=430, height=70)

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

masterFrame5 = customtkinter.CTkFrame(master=app, width=430, height=70)

frame12 = customtkinter.CTkFrame(master=masterFrame5, width=430, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame12, text="Criterio de Finalización", width=430, ).pack(fill="x", expand=True)
frame12.pack(side="top", fill="x", expand=True)

frame13 = customtkinter.CTkFrame(master=masterFrame5, width=200, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame13, text="Iteraciones", width=100).pack(side="left")
max_iteration_text = customtkinter.CTkEntry(master=frame13, width=100)
max_iteration_text.pack()
frame13.pack(padx=10, pady=5, side="left")

frame14 = customtkinter.CTkFrame(master=masterFrame5, width=200, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame14, text="% fitness", width=100).pack(side="left")
fitness_por_text = customtkinter.CTkEntry(master=frame14, width=100)
fitness_por_text.pack()
frame14.pack(padx=10, pady=5, side="left")

masterFrame5.pack(fill="x", padx=10, pady=10)

button = customtkinter.CTkButton(master=app, text="Start Genetic Algorithm", command=save_data, width=200)
button.place(relx=0.3, rely=0.9)
app.mainloop()
