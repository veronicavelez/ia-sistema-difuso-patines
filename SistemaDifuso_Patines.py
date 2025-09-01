import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import tkinter as tk
import os

# Definición de variables difusas
experiencia = ctrl.Antecedent(np.arange(0, 11, 1), 'experiencia')
frecuencia = ctrl.Antecedent(np.arange(0, 8, 1), 'frecuencia')
presupuesto = ctrl.Antecedent(np.arange(0, 1000001, 10000), 'presupuesto')
patines = ctrl.Consequent(np.arange(0, 3, 1), 'patines')

# Membresías
experiencia['baja'] = fuzz.trimf(experiencia.universe, [0, 0, 5])
experiencia['media'] = fuzz.trimf(experiencia.universe, [0, 5, 10])
experiencia['alta'] = fuzz.trimf(experiencia.universe, [5, 10, 10])

frecuencia['baja'] = fuzz.trimf(frecuencia.universe, [0, 0, 3])
frecuencia['media'] = fuzz.trimf(frecuencia.universe, [1, 3.5, 6])
frecuencia['alta'] = fuzz.trimf(frecuencia.universe, [4, 7, 7])

presupuesto['bajo'] = fuzz.trimf(presupuesto.universe, [0, 0, 400000])
presupuesto['medio'] = fuzz.trimf(presupuesto.universe, [200000, 500000, 800000])
presupuesto['alto'] = fuzz.trimf(presupuesto.universe, [600000, 1000000, 1000000])

patines['recreativos'] = fuzz.trimf(patines.universe, [0, 0, 1])
patines['deportivos'] = fuzz.trimf(patines.universe, [0, 1, 2])
patines['profesionales'] = fuzz.trimf(patines.universe, [1, 2, 2])

# Reglas
reglas = [
    ctrl.Rule(experiencia['baja'] & frecuencia['baja'] & presupuesto['bajo'], patines['recreativos']),
    ctrl.Rule(experiencia['media'] & frecuencia['media'] & presupuesto['medio'], patines['deportivos']),
    ctrl.Rule(experiencia['alta'] & frecuencia['alta'] & presupuesto['alto'], patines['profesionales']),
    ctrl.Rule(experiencia['baja'] & presupuesto['alto'], patines['deportivos']),
    ctrl.Rule(experiencia['alta'] & presupuesto['bajo'], patines['recreativos']),
]

# Sistema de control
sistema_ctrl = ctrl.ControlSystem(reglas)
sistema = ctrl.ControlSystemSimulation(sistema_ctrl)

# Función principal
def recomendar_patines():
    try:
        exp = float(entry_experiencia.get())
        frec = float(entry_frecuencia.get())
        pres = float(entry_presupuesto.get())

        sistema.input['experiencia'] = exp
        sistema.input['frecuencia'] = frec
        sistema.input['presupuesto'] = pres

        sistema.compute()
        resultado = sistema.output['patines']

        if resultado < 0.5:
            tipo = "Recreativos"
        elif resultado < 1.5:
            tipo = "Deportivos"
        else:
            tipo = "Profesionales"

        lbl_resultado.config(text=f"Tipo de patines recomendado: {tipo}", fg="blue")

    except Exception as e:
        lbl_resultado.config(text=f"Error: {str(e)}", fg="red")

def generar_graficas():
    try:
        experiencia.view()
        plt.savefig("entrada_experiencia.png")
        plt.close()

        frecuencia.view()
        plt.savefig("entrada_frecuencia.png")
        plt.close()

        presupuesto.view()
        plt.savefig("entrada_presupuesto.png")
        plt.close()

        patines.view()
        plt.savefig("salida_patines.png")
        plt.close()

        lbl_resultado.config(text="Gráficas generadas correctamente.", fg="green")

    except Exception as e:
        lbl_resultado.config(text=f"Error al generar gráficas: {str(e)}", fg="red")

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Sistema Difuso - Recomendación de Patines POLI")
ventana.geometry("500x450")
ventana.resizable(False, False)

tk.Label(ventana, text="Sistema Difuso: Recomendación de Patines POLI", font=("Helvetica", 14, "bold")).pack(pady=10)
tk.Label(ventana, text="Ingrese la información:").pack()

frame_inputs = tk.Frame(ventana)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Nivel de experiencia (0 a 10):").grid(row=0, column=0, sticky="e")
entry_experiencia = tk.Entry(frame_inputs)
entry_experiencia.grid(row=0, column=1)

tk.Label(frame_inputs, text="Frecuencia de uso (0 a 7):").grid(row=1, column=0, sticky="e")
entry_frecuencia = tk.Entry(frame_inputs)
entry_frecuencia.grid(row=1, column=1)

tk.Label(frame_inputs, text="Presupuesto ($):").grid(row=2, column=0, sticky="e")
entry_presupuesto = tk.Entry(frame_inputs)
entry_presupuesto.grid(row=2, column=1)

tk.Button(ventana, text="Recomendar Patines", command=recomendar_patines).pack(pady=5)
tk.Button(ventana, text="Generar Gráficas de Conjuntos", command=generar_graficas).pack(pady=5)

lbl_resultado = tk.Label(ventana, text="", font=("Helvetica", 12))
lbl_resultado.pack(pady=10)

frame_footer = tk.Frame(ventana)
frame_footer.pack(side="bottom", pady=15)
tk.Label(frame_footer, text="Integrantes: Isabel Medina, Laura Murillo, Veronica Velez L", font=("Arial", 9, "italic")).pack()

ventana.mainloop()
