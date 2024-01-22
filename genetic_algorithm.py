import math
import os
import random

import imageio.v2 as imageio
import matplotlib.animation as animation

import matplotlib.pyplot as plt
import numpy as np

from sympy import symbols, sin, cos, log, sqrt, exp, pi, lambdify

import customtkinter
from tkinter import messagebox

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

opc = 0


def set_opc(num):
    global opc
    opc = num


def check_data():
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


def get_bits():
    min_x = float(min_x_text.get())
    max_x = float(max_x_text.get())
    range = max_x - min_x
    jump_num = range / float(resolution_text.get())
    point_num = jump_num + 1
    return int(math.log2(point_num))


def get_individuals(bits, size):
    individuals = []
    for i in range(size):
        num = random.randint(1, 2 ** bits - 1)
        binary = bin(num)[2:].zfill(bits)
        individuals.append(binary)
    return individuals


def get_number_from(binary):
    return int(binary, 2)


def get_x(num, bits):
    min_x = float(min_x_text.get())
    max_x = float(max_x_text.get())
    range = max_x - min_x
    x = (min_x + num * (range) / (2 ** bits - 1))
    return x


def get_fx(x):
    value = symbols('x')
    try:
        func = lambdify(value, formula_text.get(), 'numpy')
        result = func(x)
        return result
    except Exception as e:
        print("error")


# a3 divition
def get_best_half_from(gen):
    if opc == 1:
        # Ordenar de menor a mayor
        # gen.sort(key=lambda x: x[-1])
        sorted_gen = sorted(gen, key=lambda x: x[-1])
    elif opc == 2:
        # Ordenar de mayor a menor
        # gen.sort(key=lambda x: x[-1], reverse=True)
        sorted_gen = sorted(gen, key=lambda x: x[-1], reverse=True)

    div = len(sorted_gen) // 2 + len(sorted_gen) % 2
    return sorted_gen[:div]


def get_gen_info(individuals, bits):
    gen_info = []
    for individual in individuals:
        num = get_number_from(individual)
        x = get_x(num, bits)
        fx = get_fx(x)
        gen_info.append([individual, num, x, fx])

    return gen_info


def get_gen0(bits, size):
    individuals = get_individuals(bits, size)
    print("individuals: ", individuals)
    return get_gen_info(individuals, bits)


def get_cross(father1, father2, cross_point):
    cross1 = father1[:cross_point] + father2[cross_point:]
    cross2 = father2[:cross_point] + father1[cross_point:]
    return cross1, cross2


def crossover(fathers, cross_point):
    new_individuals = []
    if len(fathers) == 1:
        cross1, cross2 = get_cross(fathers[0], fathers[0], cross_point)
        new_individuals.append(cross1)
        new_individuals.append(cross2)
    else:
        for i in range(1, len(fathers)):
            cross1, cross2 = get_cross(fathers[0], fathers[i], cross_point)
            new_individuals.append(cross1)
            new_individuals.append(cross2)
    return new_individuals


def is_possible(probability):
    number = round(random.random(), 2)
    return probability >= number


def mutate(individual):
    mut_ind = float(mut_ind_prob_text.get())
    individual_list = list(individual)
    if is_possible(mut_ind):
        for i in range(len(individual_list)):
            mut_gen = float(mut_gen_prob_text.get())
            if is_possible(mut_gen):
                new_position = random.randint(0, len(individual_list) - 1)
                individual_list[i], individual_list[new_position] = individual_list[new_position], individual_list[i]
    return ''.join(individual_list)


def mutation(individuals):
    new_individuals = []
    for individual in individuals:
        individual = mutate(individual)
        new_individuals.append(individual)
    return new_individuals


def get_best_from(gen, element, opc):
    value = [row[element] for row in gen]
    return min(value) if opc == 1 else max(value)


def get_worst_from(gen, element, opc):
    value = [row[element] for row in gen]
    return max(value) if opc == 1 else min(value)


def get_average_from(gen, element):
    values = [row[element] for row in gen]
    average = sum(values) / len(values) if len(values) > 0 else None
    return round(average, 2)


def pruning(gen_info):
    new_gen_info = []
    if opc == 1:
        # menor a mayor
        new_gen_info = sorted(gen_info, key=lambda x: x[-1])[:int(initial_pob_text.get())]
    elif opc == 2:
        # mayor a menor
        new_gen_info = sorted(gen_info, key=lambda x: x[-1], reverse=True)[:int(initial_pob_text.get())]

    return new_gen_info


def get_initial_data(bits, size):
    print("bits: ", bits)

    gen = get_gen0(bits, size)
    print("gen: ", gen)
    return gen


def optimization(gen, bits):
    coord_b_fx = []
    coord_w_fx = []
    coord_a_fx = []
    gen_data2 = []
    for i in range(int(max_iteration_text.get())):
        prev_gen = gen
        # A3
        gen = get_best_half_from(gen)
        print("gen: ", gen)
        individuals = [element[0] for element in gen]
        print("A new individuals: ", individuals)
        # C3
        individuals = crossover(individuals, bits // 2 + (bits % 2))
        print("C new individuals: ", individuals)
        # M2
        individuals = mutation(individuals)
        print("M new individuals: ", individuals)

        # get all gen_info
        new_gen = get_gen_info(individuals, bits)
        print("la tabla de nuevos indiviuos: ", new_gen)

        # join prev gen with new gen
        gen = prev_gen + new_gen
        # Individual Data
        gen_data = []
        for ind in gen:
            last_data = ind[-2:]
            gen_data.append(last_data)
        gen_data2.append(gen_data)

        print("la union de toda la gen es: ", gen)
        # sacar mejores
        best_fx = get_best_from(gen, 3, opc)
        worst_fx = get_worst_from(gen, 3, opc)
        average_fx = get_average_from(gen, 3)
        print("Best individual: ", best_fx)
        coord_b_fx.append([i, best_fx])
        print("worst individual: ", worst_fx)
        coord_w_fx.append([i, worst_fx])
        print("Average individual: ", average_fx)
        coord_a_fx.append([i, average_fx])
        # P1
        gen = pruning(gen)

        print("after pruning: ", gen)
    return coord_b_fx, coord_w_fx, coord_a_fx, gen_data2


def generate_evolution_graphic(coord_b_fx, coord_w_fx, coord_a_fx):
    best = np.array(coord_b_fx)
    worst = np.array(coord_w_fx)
    average = np.array(coord_a_fx)
    plt.plot(best[:, 0], best[:, 1], label="best", color="green")
    plt.plot(worst[:, 0], worst[:, 1], label="worst", color="red")
    plt.plot(average[:, 0], average[:, 1], label="average", color="blue")
    plt.legend()
    plt.title("Evolution Graphics f(x)")
    plt.xlabel("Generations")
    plt.ylabel("f(x)")
    plt.show()


def get_coords(coords):
    x = [item[0] for item in coords]
    y = [item[1] for item in coords]
    return x, y


def generate_generation_graphic(gen_data):
    for i in range(len(gen_data)):
        coords = []
        coords2 = []
        if opc == 1:
            coords = gen_data[i][np.argmin(np.array(gen_data[i])[:, 1])]
            coords2 = gen_data[i][np.argmax(np.array(gen_data[i])[:, 1])]
        elif opc == 2:
            coords = gen_data[i][np.argmax(np.array(gen_data[i])[:, 1])]
            coords2 = gen_data[i][np.argmin(np.array(gen_data[i])[:, 1])]
        plt.cla()
        x, y = get_coords(gen_data[i])
        plt.scatter(x, y, c="black")
        plt.scatter(coords[0], coords[1], c="green", label="best", zorder=1)
        plt.scatter(coords2[0], coords2[1], c="red", label="worst", zorder=1)

         # Agrega la función evaluada a la gráfica
        x_symbol = symbols('x')
        func = lambdify(x_symbol, formula_text.get(), 'numpy')
        x_vals = np.linspace(float(min_x_text.get()), float(max_x_text.get()), 100000)
        y_vals = func(x_vals)
        plt.plot(x_vals, y_vals, label='Function', linestyle='--', color='blue')

        plt.title(f"Generation {i + 1}")
        plt.legend()
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.savefig(f"./images/generation{i + 1}.png")



def generate_evolution_video():
    images_directory = "./images/"
    images_files = sorted(os.listdir(images_directory))
    images = []
    for image in images_files:
        image_root = os.path.join(images_directory, image)
        images.append(imageio.imread(image_root))
    video_output = "./videos/generation.mp4"
    imageio.mimsave(video_output, images, fps=1)


def show_message(coord_b_fx):
    best_element = None
    for element in coord_b_fx:
        if best_element is None or (opc and element[1] > best_element[1]) or \
                (not opc and element[1] < best_element[1]):
            best_element = element
    msg = f'the best generation is: \n Gen: {best_element[0]} \n f(x): {best_element[1]} '

    messagebox.showinfo("information", msg)


def start():
    check_data()
    print("starting...")
    size = int(initial_pob_text.get())
    bits = get_bits()
    gen = get_initial_data(bits, size)

    # here starts optimization
    coord_b_fx = []
    coord_w_fx = []
    coord_a_fx = []
    gen_data = []
    coord_b_fx, coord_w_fx, coord_a_fx, gen_data = optimization(gen, bits)  # this returns the collection of coords,

    # get info message
    show_message(coord_b_fx)

    # evolution graphic
    generate_evolution_graphic(coord_b_fx, coord_w_fx, coord_a_fx)

    # generation graphic
    generate_generation_graphic(gen_data)

    # create video
    generate_evolution_video()


def clean():
    print("cleaning...")


app = customtkinter.CTk()
app.geometry("430x800")
app.title("IA C1 A 1 Genetic Algorithms 01")
app.resizable(False, False)

mFrame1 = customtkinter.CTkFrame(master=app, width=450, height=700)

masterFrame1 = customtkinter.CTkFrame(master=mFrame1, width=430, height=70, fg_color="transparent")

frame = customtkinter.CTkFrame(master=masterFrame1, width=430, height=20, fg_color="transparent")
customtkinter.CTkLabel(master=frame, text="Fórmula", width=430, ).pack(fill="x", expand=True)
frame.pack(side="top", fill="x", expand=True)

frame1 = customtkinter.CTkFrame(master=masterFrame1, width=300, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame1, text="f(x)", width=100).pack(side="left")
formula_text = customtkinter.CTkEntry(master=frame1, width=200)
formula_text.pack()
frame1.pack(padx=10, pady=5, side="left")

frame2 = customtkinter.CTkFrame(master=masterFrame1, width=130, height=70, fg_color="transparent")
minBttn = customtkinter.CTkButton(master=frame2, text="mínimo", command=lambda: set_opc(1)).pack(pady=5)
maxBttn = customtkinter.CTkButton(master=frame2, text="máximo", command=lambda: set_opc(2)).pack(pady=5)
frame2.pack(padx=10, pady=10, side="left")

masterFrame1.pack(fill="x", padx=10, pady=10)

masterFrame1_1 = customtkinter.CTkFrame(master=mFrame1, width=430, height=70, fg_color="transparent")
frame1_1 = customtkinter.CTkFrame(master=masterFrame1_1, width=430, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame1_1, text="Resolución", width=430).pack(fill="x", expand=True)
frame1_1.pack(side="top", fill="x", expand=True)

frame1_2 = customtkinter.CTkFrame(master=masterFrame1_1, width=430, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame1_2, text="Resolución", width=215).pack(side="left")
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
customtkinter.CTkLabel(master=frame5, text="Máxima", width=100).pack(side="left")
max_pob_text = customtkinter.CTkEntry(master=frame5, width=100)
max_pob_text.pack()
frame5.pack(padx=10, pady=5, side="left")

masterFrame2.pack(fill="x", padx=10, pady=10)

masterFrame3 = customtkinter.CTkFrame(master=mFrame1, width=430, height=70, fg_color="transparent")

frame6 = customtkinter.CTkFrame(master=masterFrame3, width=430, height=70, fg_color="transparent")
customtkinter.CTkLabel(master=frame6, text="Mutación", width=430, ).pack(fill="x", expand=True)
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

button = customtkinter.CTkButton(master=mFrame1, text="Start Genetic Algorithm", command=start, width=200)
button.pack(padx=10, pady=20)
# button = customtkinter.CTkButton(master=mFrame1, text="Clean Genetic Algorithm", command=clean, width=200)
# button.pack(padx=10, pady=20)

mFrame1.pack(side="left", fill="y")

app.mainloop()
