import tkinter as tk
import tkinter.messagebox


screenRoot = tk.Tk()
screenRoot.title("AI.C1.A1 Genetic Algorithms")
screenRoot.geometry("400x600")

def guardar_datos():
    campos = [
        formula.get(),
        i_poblation.get(),
        max_poblation.get(),
        ind_mut_prob.get(),
        ind_gen_mut_prob.get(),
        min_range.get(),
        max_range.get(),
        iteraciones.get(),
        fitness.get(),
    ]

    if any(campo == "" for campo in campos):
        tk.messagebox.showwarning("Error", "Por favor, complete todos los campos.")
        return

    # Guarda los datos en un archivo o base de datos
    with open("datos.txt", "w") as f:
        f.writelines(campo + "\n" for campo in campos)

    tk.messagebox.showinfo("Éxito", "Datos guardados correctamente.")


frame1 = tk.Frame(screenRoot).pack(pady=5)
tk.Label(frame1, text="formula").pack()
tk.Label(frame1, text="f(x)").pack()
formula = tk.Entry(frame1)
formula.pack()
line = tk.Frame(screenRoot, height=2, bd=1, relief=tk.SUNKEN)
line.pack(fill=tk.X, padx=10, pady=5)

frame2 = tk.Frame(screenRoot).pack()
tk.Label(frame2,text="Tamaño de la población").pack()
tk.Label(frame2,text="Inicial").pack()
i_poblation=tk.Entry(frame2)
i_poblation.pack()
tk.Label(frame2,text="Maxima").pack()
max_poblation=tk.Entry(frame2)
max_poblation.pack()
line = tk.Frame(screenRoot, height=2, bd=1, relief=tk.SUNKEN)
line.pack(fill=tk.X, padx=10, pady=5)

frame3 = tk.Frame(screenRoot).pack()
tk.Label(frame3,text="Probabilidades de mutación").pack()
tk.Label(frame2,text="Por individo").pack()
ind_mut_prob=tk.Entry(frame2)
ind_mut_prob.pack()
tk.Label(frame2,text="Por gen").pack()
ind_gen_mut_prob=tk.Entry(frame2)
ind_gen_mut_prob.pack()
line = tk.Frame(screenRoot, height=2, bd=1, relief=tk.SUNKEN)
line.pack(fill=tk.X, padx=10, pady=5)

frame4 = tk.Frame(screenRoot).pack()
tk.Label(frame4,text="Rango de posibles soluciones").pack
tk.Label(frame4,text="minimo").pack()
min_range=tk.Entry(frame4)
min_range.pack()
tk.Label(frame4,text="maximo").pack()
max_range=tk.Entry(frame4)
max_range.pack()
line = tk.Frame(screenRoot, height=2, bd=1, relief=tk.SUNKEN)
line.pack(fill=tk.X, padx=10, pady=5)

frame5 = tk.Frame(screenRoot).pack()
tk.Label(frame5,text="Criterios de finalización")
tk.Label(frame5,text="iteraciones").pack()
iteraciones=tk.Entry(frame5)
iteraciones.pack()
tk.Label(frame5,text="% fitness").pack()
fitness = tk.Entry(frame5)
fitness.pack()

# Botón de guardar
boton_guardar = tk.Button(screenRoot, text="Guardar", command=guardar_datos)
boton_guardar.pack()

screenRoot.mainloop()


