import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Modelo Epidemiológico SIR
class PoblacionSIR:
    def __init__(self, S, I, R, beta, gamma, N):
        self.S = S  # Susceptibles
        self.I = I  # Infectados
        self.R = R  # Recuperados
        self.beta = beta  # Tasa de infección
        self.gamma = gamma  # Tasa de recuperación
        self.N = N  # Población total
        self.t = 0  # Tiempo actual

    def __call__(self):
        return {'S': self.S, 'I': self.I, 'R': self.R}

    def paso_tiempo(self, dt=0.1):
        """
        Resolver las ecuaciones diferenciales SIR usando el método de Euler.
        """
        nuevo_infectados = self.beta * self.S * self.I / self.N
        nuevos_recuperados = self.gamma * self.I

        dS = -nuevo_infectados * dt
        dI = (nuevo_infectados - nuevos_recuperados) * dt
        dR = nuevos_recuperados * dt

        self.S += dS
        self.I += dI
        self.R += dR
        self.t += dt

    def __str__(self):
        return f"Tiempo: {self.t:.2f}, S: {self.S:.2f}, I: {self.I:.2f}, R: {self.R:.2f}"


class SimuladorSIR:
    def __init__(self, poblacion, tiempo_simulacion, dt=0.1):
        self.poblacion = poblacion
        self.tiempo_simulacion = tiempo_simulacion
        self.dt = dt
        self.resultados = {'t': [], 'S': [], 'I': [], 'R': []}

    def ejecutar_simulacion(self):
        """
        Simular la propagación de la enfermedad en el tiempo.
        """
        tiempo_actual = 0
        while tiempo_actual < self.tiempo_simulacion:
            self.poblacion.paso_tiempo(self.dt)
            self.resultados['t'].append(self.poblacion.t)
            self.resultados['S'].append(self.poblacion.S)
            self.resultados['I'].append(self.poblacion.I)
            self.resultados['R'].append(self.poblacion.R)
            tiempo_actual += self.dt

    def obtener_resultados(self):
        return self.resultados


def graficar_sir(resultados):
    """
    Función para graficar los resultados del modelo SIR.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(resultados['t'], resultados['S'], label='Susceptibles', color='b')
    plt.plot(resultados['t'], resultados['I'], label='Infectados', color='r')
    plt.plot(resultados['t'], resultados['R'], label='Recuperados', color='g')
    plt.xlabel('Tiempo')
    plt.ylabel('Población')
    plt.title('Modelo Epidemiológico SIR')
    plt.legend()
    plt.grid(True)
    plt.show()


def animar_sir(resultados):
    """
    Crear una animación que muestre la evolución de los grupos poblacionales en el tiempo.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, max(resultados['t']))
    ax.set_ylim(0, max(resultados['S'] + resultados['I'] + resultados['R']))
    
    linea_S, = ax.plot([], [], label='Susceptibles', color='b')
    linea_I, = ax.plot([], [], label='Infectados', color='r')
    linea_R, = ax.plot([], [], label='Recuperados', color='g')

    def actualizar(frame):
        linea_S.set_data(resultados['t'][:frame], resultados['S'][:frame])
        linea_I.set_data(resultados['t'][:frame], resultados['I'][:frame])
        linea_R.set_data(resultados['t'][:frame], resultados['R'][:frame])
        return linea_S, linea_I, linea_R

    animacion = FuncAnimation(fig, actualizar, frames=len(resultados['t']), interval=100)
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Población')
    ax.set_title('Evolución de la epidemia con el modelo SIR')
    ax.legend()
    ax.grid(True)
    
    plt.show()


# Parámetros iniciales
N = 1000  # Población total
I0 = 1  # Infectados iniciales
R0 = 0  # Recuperados iniciales
S0 = N - I0 - R0  # Susceptibles iniciales
beta = 0.3  # Tasa de infección
gamma = 0.1  # Tasa de recuperación
tiempo_simulacion = 160  # Días

# Crear la población SIR inicial
poblacion = PoblacionSIR(S0, I0, R0, beta, gamma, N)

# Ejecutar la simulación
simulador = SimuladorSIR(poblacion, tiempo_simulacion)
simulador.ejecutar_simulacion()

# Graficar resultados
resultados = simulador.obtener_resultados()
graficar_sir(resultados)
animar_sir(resultados)
