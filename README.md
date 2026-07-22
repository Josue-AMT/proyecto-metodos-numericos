# 🧮 Aplicación Interactiva de Métodos Numéricos

Proyecto final para la materia **Matemáticas Aplicadas para la Computación**. Esta aplicación web permite ejecutar e interactuar con tres métodos numéricos fundamentales, visualizando los pasos y resultados de manera dinámica.

## 🚀 Características

La aplicación incluye tres métodos numéricos implementados en pestañas separadas:

### 1. 🧩 Método de Gauss-Jordan (Sistemas de Ecuaciones Lineales)
- Resuelve sistemas de ecuaciones lineales mostrando cada transformación de la matriz aumentada
- Utiliza **fracciones exactas** para evitar errores de redondeo
- Permite configurar el número de variables/ecuaciones (2 a 6)
- Muestra el desarrollo matemático iterativo paso a paso
- Detecta e informa sobre sistemas sin solución única

### 2. 📈 Interpolación de Newton (Diferencias Divididas)
- Encuentra el polinomio interpolador utilizando el método de diferencias divididas
- Permite ingresar hasta 10 puntos conocidos
- Calcula el valor estimado para cualquier punto X
- Muestra la matriz completa de diferencias divididas
- Visualiza el desarrollo de la evaluación del polinomio

### 3. 📉 Método de Euler (Ecuaciones Diferenciales Ordinarias)
- Aproxima numéricamente soluciones de EDOs de primer orden
- Permite definir la función f(x,y) personalizada
- Configurable: condiciones iniciales, valor objetivo y tamaño del paso
- Muestra tabla descriptiva de todas las iteraciones
- Incluye gráfico de la trayectoria de aproximación

## 📋 Requisitos

- Python 3.x
- Las siguientes dependencias (ver `requirements.txt`):
  - streamlit
  - pandas
  - numpy

## 🔧 Instalación

1. Clona este repositorio o descarga los archivos

2. Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

Para iniciar la aplicación web, ejecuta el siguiente comando:

```bash
streamlit run proyecto_final_web.py
```

La aplicación se abrirá automáticamente en tu navegador web predeterminado (generalmente en `http://localhost:8501`).

## 📖 Uso

### Gauss-Jordan
1. Selecciona el número de variables/ecuaciones
2. Modifica los valores de la matriz aumentada [A | B] directamente en la tabla
3. Haz clic en "Resolver Sistema y Ver Pasos"
4. Observa el desarrollo paso a paso con fracciones exactas
5. Consulta la solución exacta al final

### Interpolación de Newton
1. Define la cantidad de puntos conocidos
2. Ingresa las coordenadas (X, Y) en la tabla
3. Especifica el valor de X a evaluar
4. Haz clic en "Calcular Interpolación"
5. Revisa el resultado estimado y explora la matriz de diferencias divididas

### Método de Euler
1. Ingresa la función f(x,y) usando sintaxis de Python (ej: `x/y`, `3*x + 2*y`)
2. Define las condiciones iniciales (x0, y0)
3. Especifica el valor objetivo xf y el tamaño del paso h
4. Haz clic en "Ejecutar Simulación"
5. Analiza la tabla de iteraciones y el gráfico de trayectoria

## 📁 Estructura del Proyecto

```
├── proyecto_final_web.py    # Archivo principal de la aplicación Streamlit
├── requirements.txt         # Dependencias del proyecto
└── README.md               # Este archivo
```

## 👨‍💻 Autor

Proyecto desarrollado para la materia **Matemáticas Aplicadas para la Computación**

## 📄 Licencia

Este proyecto es parte de un trabajo académico.
