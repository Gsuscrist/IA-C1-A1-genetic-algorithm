import tkinter as tk

screenRoot = tk.Tk()
screenRoot.title("AI.C1.A1 Genetic Algorithms")
screenRoot.geometry("400x600")

frame1 = tk.Frame(screenRoot).pack()
tk.Label(frame1, text="f(x)").pack()
formula = tk.Entry(frame1).pack()
line = tk.Frame(screenRoot, height=2, bd=1, relief=tk.SUNKEN)
line.pack(fill=tk.X, padx=10, pady=5)

frame2 = tk.Frame(screenRoot).pack()
tk.Label(frame2,text="Tamaño de la población").pack()
tk.Label(frame2,text="Inicial").pack()
i_poblation=tk.Entry(frame2).pack()
tk.Label(frame2,text="Maxima").pack()
max_poblation=tk.Entry(frame2).pack()
line = tk.Frame(screenRoot, height=2, bd=1, relief=tk.SUNKEN)
line.pack(fill=tk.X, padx=10, pady=5)

frame3 = tk.Frame(screenRoot).pack()
tk.Label(frame3,text="Probabilidades de mutación").pack()
tk.Label(frame2,text="Por individo").pack()
ind_mut_prob=tk.Entry(frame2).pack()
tk.Label(frame2,text="Por gen").pack()
ind_gen_mut_prob=tk.Entry(frame2).pack()
line = tk.Frame(screenRoot, height=2, bd=1, relief=tk.SUNKEN)
line.pack(fill=tk.X, padx=10, pady=5)

frame4 = tk.Frame(screenRoot).pack()
tk.Label(frame4,text="Rango de posibles soluciones").pack
tk.Label(frame4,text="minimo").pack()
min_range=tk.Entry(frame4).pack()
tk.Label(frame4,text="maximo").pack()
max_range=tk.Entry(frame4).pack()
line = tk.Frame(screenRoot, height=2, bd=1, relief=tk.SUNKEN)
line.pack(fill=tk.X, padx=10, pady=5)

frame5 = tk.Frame(screenRoot).pack()
tk.Label(frame5,text="Criterios de finalización")
tk.Label(frame5,text="iteraciones").pack()
iteraciones=tk.Entry(frame5).pack()
tk.Label(frame5,text="% fitness").pack()
fitness = tk.Entry(frame5).pack()

screenRoot.mainloop()


