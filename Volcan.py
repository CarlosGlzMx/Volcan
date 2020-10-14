#Importar las librerías a usar
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

#Definicion de variables iniciales, usando la gravedad de la Tierra y nuestra investigación sobre rocas volcánicas
gravedad = 9.81
cf = 0.5
densidadRoca = 3100
deltaT = .1

#Obtención de datos personalizados
altitud = int(input("Qué altitud tiene el volcán del que lanzarás los proyetiles? "))
Vo = int(input("Dame la velocidad inicial para arrojar los objetos (m/s): "))

while True:
    AnguloGrados = int(input("Dame el ángulo con el que serán arrojados (grados): "))
    if AnguloGrados <= 90 and AnguloGrados >= 0:
        break
    else:
        print("Dame un ángulo válido de lanzamiento entre 0 y 90")

m1 = int(input("Dame la masa del objeto 1 (kg): "))
m2 = int(input("Dame la masa del objeto 2 (kg): "))
m3 = int(input("Dame la masa del objeto 3 (kg): "))

#Activa o desactiva la fricción según la elección del usuario
while True:
    respuestaF = input("Quieres considerar la fricción del aire? (si o no) ")
    if respuestaF.lower() == "no" or respuestaF.lower() == "n":
        cf = 0
        break
    elif respuestaF.lower() == "si" or respuestaF.lower() == "s":
        break
    else:
        print("Favor de responder si o no")

#Cálculo de valores iniciales
Angulo = AnguloGrados * (math.pi/180)
Vox = Vo * math.cos(Angulo)
Voy = Vo * math.sin(Angulo)

#Cálculo de las areas de contacto teniendo densidad y masa
def DensidadYMasaAArea (masa):
    volumen = masa / densidadRoca
    radio = ((3 * volumen) / (4 * math.pi)) ** (1 / 3)
    areaContacto = 2 * math.pi * (radio ** 2)
    return areaContacto

AreaC1 = DensidadYMasaAArea(m1)
AreaC2 = DensidadYMasaAArea(m2)
AreaC3 = DensidadYMasaAArea(m3)

#Cálculo con fórmula de la densidad del aire
densidadAire = -7.83 * (10 ** -5) * altitud + 1.225

#Calculo de la variable temporal b
b1 = .5 * densidadAire * AreaC1 * cf
b2 = .5 * densidadAire * AreaC2 * cf
b3 = .5 * densidadAire * AreaC3 * cf

#Realiza el metodo numerico Verlet para todos los valores iniciales posibles
def verlet(Vox, Voy, b, masa, gravedad, deltaT):
    listaY = []
    listaX = []
    listaVX = []
    listaVY = []
    aceleracionCeroX = -b * Vox / masa
    aceleracionCeroY = - b * Voy / masa - gravedad
    anteriorX = (0 - Vox * deltaT + 0.5 * aceleracionCeroX * (deltaT ** 2))
    anteriorY = (0 - Voy * deltaT + 0.5 * aceleracionCeroY * (deltaT ** 2)) + altitud
    x = 0
    y = altitud
    t = 0
    listaX.append(x)
    listaY.append(y)
    listaVX.append(Vox)
    listaVY.append(Voy)
    #Busca todos los valores solo cuando y es positiva o 0
    while y >= 0:
        t = t + deltaT
        velocidadX = Vox * math.exp(-b * t / masa)
        listaVX.append(velocidadX)
        #Cambia la orientación de la fuerza de fricción en Y
        if(Voy * math.exp(-b * t / masa) - gravedad * t > 0):
            velocidadY = Voy * math.exp(-b * t / masa) - gravedad * t
        elif(Voy * math.exp(-b * t / masa) - gravedad * t == 0):
            velocidadY = 0
        else:
            velocidadY = Voy * math.exp(b * t / masa) - gravedad * t
        listaVY.append(velocidadY)
        #Aplica el metodo de Verlet para la posición
        siguienteX = (2 - b / masa * deltaT) * x - (1 - b * deltaT / masa) * anteriorX
        anteriorX = x
        x = siguienteX 
        siguienteY = (2 - b / masa * deltaT) * y -(1 - b * deltaT / masa) * anteriorY - gravedad * deltaT ** 2 
        anteriorY = y
        y = siguienteY
        listaY.append(siguienteY)
        listaX.append(siguienteX)
    return listaX, listaY, listaVX, listaVY

#Llama la función para cada objeto y guarda los datos en un array de numpy
listaX1, listaY1, listaVX1, listaVY1 = verlet(Vox, Voy, b1, m1, gravedad, deltaT)
x1 = np.array(listaX1)
y1 = np.array(listaY1)
vx1 = np.array(listaVX1)
vy1 = np.array(listaVY1)

listaX2, listaY2, listaVX2, listaVY2 = verlet(Vox, Voy, b2, m2, gravedad, deltaT)
x2 = np.array(listaX2)
y2 = np.array(listaY2)
vx2 = np.array(listaVX2)
vy2 = np.array(listaVY2)

listaX3, listaY3, listaVX3, listaVY3 = verlet(Vox, Voy, b3, m3, gravedad, deltaT)
x3 = np.array(listaX3)
y3 = np.array(listaY3)
vx3 = np.array(listaVX3)
vy3 = np.array(listaVY3)

#Crea un lienzo fig1 con ejes ax para la gráfica de matplotlib
fig1, ax = plt.subplots()

#Agrega 3 lineas formadas por coordenadas x y y
line1, = ax.plot(x1, y1, color='k', label="1: " + str(m1) + "kg")
line2, = ax.plot(x2, y2, color='sienna', label="2: " + str(m2) + "kg")
line3, = ax.plot(x3, y3, color='firebrick', label="3: " + str(m3) + "kg")

#Crea los textos de posición y velocidad
texto1 = ax.text(0.05, 0.95, "", horizontalalignment = "left", verticalalignment="top",transform=ax.transAxes)
texto2 = ax.text(0.05, 0.85, "", horizontalalignment = "left", verticalalignment="top",transform=ax.transAxes)
texto3 = ax.text(0.05, 0.75, "", horizontalalignment = "left", verticalalignment="top",transform=ax.transAxes)

#Encuentra que tiro llega más lejos en x para pooder graficar todos los tiros con su rango completo
if (len(x1)>=len(x2) and len(x1)>=len(x3)):
    rangoMax = len(x1)
    tiroMax = x1
    altMax = y1
elif (len(x2)>=len(x1) and len(x2)>=len(x3)):
    rangoMax = len(x2)
    tiroMax = x2
    altMax = y2
else:
    rangoMax = len(x3)
    tiroMax = x3
    altMax = y3

#Encuentra la altura máxima de cualquier gráfica para que los ejes de la figura se ajusten
alturaGraficaMax = np.max(altMax)

#Cálcula la rapidez final con las componentes finales de la velocidad
RapidezFinalUno = ((listaVX1[-1]) ** 2 + (listaVY1[-1]) ** 2) ** 0.5
RapidezFinalDos = ((listaVX2[-1]) ** 2 + (listaVY2[-1]) ** 2) ** 0.5
RapidezFinalTres = ((listaVX3[-1]) ** 2 + (listaVY3[-1]) ** 2) ** 0.5

#Actualiza las tres gráficas
def update(num, x1, y1, vx1, vy1, line1, x2, y2, vx2, vy2, line2, x3, y3, vx3, vy3, line3):
    texto1.set_text("")
    #Actualiza la gráfica con un contador solo hasta que se acaben los datos en y
    if len(y1) > num:
        line1.set_data(x1[:num], y1[:num])
        texto1.set_text("1.Posición: (" + str(round(x1[num],2)) + "," + str(round(y1[num],2)) + \
            ") \n1.Velocidad: (" + str(round(vx1[num],2)) + "," + str(round(vy1[num],2))+")")
    #Cuando se acaban los numeros, se imprime el resumen del vuelo, se hace lo mismo para las otros tiros
    else:
        texto1.set_text("Resumen 1: Xmax: " + str(round(x1[-1],2)) + "m Ymax: " + str(round(max(y1),2)) + "m" + \
            "\nVel. de impacto: " + str(round(RapidezFinalUno,2)) + "m/s = " + str(round(RapidezFinalUno*3.6,2)) + "km/h.")
    if len(y2) > num:
        line2.set_data(x2[:num], y2[:num])
        texto2.set_text(("2.Posición: (" + str (round(x2[num],2)) + "," + str(round(y2[num],2)) + \
            ") \n2.Velocidad: (" + str(round(vx2[num],2)) + "," + str(round(vy2[num],2))+")"))
    else:
        texto2.set_text("Resumen 2: Xmax: " + str(round(x2[-1],2)) + "m Ymax: " + str(round(max(y2),2)) + "m" + \
            "\nVel. de impacto: " + str(round(RapidezFinalDos,2)) + "m/s = " + str(round(RapidezFinalDos*3.6,2)) + "km/h.")
    if len(y3) > num:
        line3.set_data(x3[:num], y3[:num])
        texto3.set_text(("3.Posición: (" + str(round(x3[num],2)) + "," + str(round(y3[num],2)) + \
            ") \n3.Velocidad: (" + str(round(vx3[num],3)) + "," + str(round(vy3[num],3))+")"))
    else:
        texto3.set_text("Resumen 3: Xmax: " + str(round(x3[-1],2)) + "m Ymax: " + str(round(max(y3),2)) + "m" + \
            "\nVel. de impacto: " + str(round(RapidezFinalTres,2)) + "m/s = " + str(round(RapidezFinalTres*3.6,2)) + "km/h.")
    #Ajusta los ejes para que siempre sean un poco más grandes que los tiros
    line1.axes.axis([0, tiroMax[-1]*1.1 , 0, alturaGraficaMax*1.6])
    return line1, line2, line3, texto1, texto2, texto3

#Crea la animación con las gráficas de arriba
ani = animation.FuncAnimation(fig1, update, rangoMax+1, fargs=[x1, y1, vx1, vy1, line1, x2, y2, vx2, vy2, \
    line2, x3, y3, vx3, vy3, line3], interval=5, blit=True, repeat=False)

#Aplica diseño a la gráfica
plt.title("Tiro parabólico de un volcán")
plt.ylabel("Altura")
plt.xlabel("Distancia")
ax.legend()

#Muestra los valores finales en consola
print()
print("La velocidad de impacto de proyectil 1 fue: " + str(RapidezFinalUno) + " m/s")
print("O bien, de " + str(RapidezFinalUno * 3.6) + " km/h")
print("La distancia máxima recorrida por el proyectil 1: " + str(listaX1[-1]) + " m")
print("La altura máxima que alcanzó el proyectil 1 fue: " + str(np.max(listaY1)) + " m")
print()
print("La velocidad de impacto de proyectil 2 fue: " + str(RapidezFinalDos) + " m/s")
print("O bien, de " + str(RapidezFinalDos * 3.6) + " km/h")
print("La distancia máxima recorrida por el proyectil 2: " + str(listaX2[-1]) + " m")
print("La altura máxima que alcanzó el proyectil 2 fue: " + str(np.max(listaY2)) + " m")
print()
print("La velocidad de impacto de proyectil 3 fue: " + str(RapidezFinalTres) + " m/s")
print("O bien, de " + str(RapidezFinalTres * 3.6) + " km/h")
print("La distancia máxima recorrida por el proyectil 3: " + str(listaX3[-1]) + " m")
print("La altura máxima que alcanzó el proyectil 3 fue: " + str(np.max(listaY3)) + " m")

#Muestra la gráfica generada
plt.show()