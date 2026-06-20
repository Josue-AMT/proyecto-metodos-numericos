import streamlit as st
import numpy as np
import pandas as pd
import math

st.set_page_config(
    page_title="Proyecto Final - Métodos Numéricos",
    page_icon="🧮",
    layout="wide"
)

st.title("🧮 Aplicación Interactiva de Métodos Numéricos")
st.markdown("### Materia: Matemáticas Aplicadas para la Computación (Proyecto Final)")
st.write("Esta plataforma web permite ejecutar e interactuar con los tres métodos numéricos seleccionados para el proyecto, visualizando los pasos y resultados de manera dinámica.")

tab1, tab2, tab3 = st.tabs([
    "🧩 1. Gauss-Jordan (Sistemas)", 
    "📈 2. Interpolación de Lagrange", 
    "📉 3. Método de Euler (EDO)",
])

with tab1:
    st.header("Método de Eliminación de Gauss-Jordan")
    st.write("Resuelve un sistema de ecuaciones lineales de la forma $Ax = B$ transformando la matriz aumentada en una matriz identidad.")
    
    n = st.number_input("Número de variables / ecuaciones:", min_value=2, max_value=5, value=3, step=1, key="gj_n")
    
    st.subheader("Matriz Aumentada [A | B]")
    st.info("Modifica los valores directamente en la tabla tipo Excel de abajo (la última columna representa el vector de resultados B):")
    
    default_matrix = np.zeros((n, n + 1))
    if n == 3:
        default_matrix = np.array([
            [1.0, 2.0, 3.0, 5.0],
            [-3.0, -2.0, -1.0, 7.0],
            [4.0, 1.0, -1.0, -5.0]
        ])
        
    column_names = [f"x{i+1}" for i in range(n)] + ["Resultado (B)"]
    df_matrix = pd.DataFrame(default_matrix, columns=column_names)
    
    edited_df = st.data_editor(df_matrix, use_container_width=True)
    
    if st.button("Resolver Sistema", type="primary"):
        a = edited_df.to_numpy(dtype=float).copy()
        error = False
        
        for i in range(n):
            if a[i][i] == 0.0:
                for k in range(i + 1, n):
                    if a[k][i] != 0.0:
                        a[[i, k]] = a[[k, i]]
                        break
                else:
                    st.error("Error: Se detectó un pivote igual a cero. El sistema puede no tener solución única.")
                    error = True
                    break
            
            # Eliminación
            for j in range(n):
                if i != j:
                    ratio = a[j][i] / a[i][i]
                    a[j] = a[j] - ratio * a[i]
                    
        if not error:
            for i in range(n):
                a[i] = a[i] / a[i][i]
                
            st.success("¡Sistema resuelto con éxito!")
            st.subheader("💡 Solución:")
            
            col_results = st.columns(n)
            for i in range(n):
                col_results[i].metric(label=f"Variable x_{i+1}", value=f"{a[i][n]:.4f}")
                
            st.markdown("**Matriz Identidad Aumentada Resultante:**")
            st.dataframe(pd.DataFrame(a, columns=column_names))

with tab2:
    st.header("Interpolación Numérica de Lagrange")
    st.write("Encuentra el valor aproximado de una función polinomial en un punto objetivo dado un conjunto de coordenadas conocidas $(x, y)$.")
    
    m = st.number_input("Cantidad de puntos conocidos:", min_value=2, max_value=10, value=4, step=1, key="lag_m")
    
    st.subheader("Tabla de Coordenadas Conocidas")
    default_pts = np.zeros((m, 2))
    if m == 4:
        default_pts = np.array([
            [0.0, -1.0],
            [1.0, 6.0],
            [2.0, 31.0],
            [3.0, 18.0]
        ])
    df_pts = pd.DataFrame(default_pts, columns=["Coordenada X", "Coordenada Y"])
    edited_pts = st.data_editor(df_pts, use_container_width=True, key="editor_pts")
    
    xp = st.number_input("Valor de 'X' a evaluar/interpolar:", value=4.0)
    
    if st.button("Calcular Interpolación", type="primary"):
        pts_matrix = edited_pts.to_numpy(dtype=float)
        x_vals = pts_matrix[:, 0]
        y_vals = pts_matrix[:, 1]
        
        yp = 0.0
        detalles = []
        
        for i in range(m):
            p = 1.0
            terminos_texto = []
            for j in range(m):
                if i != j:
                    p *= (xp - x_vals[j]) / (x_vals[i] - x_vals[j])
            yp += p * y_vals[i]
            detalles.append(f"Polinomio L_{i}({xp}) × y_{i} = {p:.4f} × {y_vals[i]} = {p * y_vals[i]:.4f}")
            
        st.success(f"¡Cálculo completado!")
        st.metric(label=f"Resultado estimado y({xp})", value=f"{yp:.4f}")
        
        with st.expander("Ver desarrollo paso a paso"):
            for d in detalles:
                st.write(d)

with tab3:
    st.header("Método de Euler para Ecuaciones Diferenciales")
    st.write("Aproxima numéricamente la solución de una ecuación diferencial ordinaria (EDO) de primer orden de la forma $\frac{dy}{dx} = f(x, y)$.")
    
    col1, col2 = st.columns(2)
    with col1:
        expr = st.text_input("Función f(x,y) [Usa sintaxis Python, ej: x/y, 3*x + 2*y]:", value="x/y")
        x0 = st.number_input("Condición inicial x0:", value=-3.0)
        y0 = st.number_input("Condición inicial y0:", value=4.0)
    with col2:
        xf = st.number_input("Valor objetivo xf a evaluar:", value=-2.0)
        h = st.number_input("Tamaño del paso (h):", value=0.5, min_value=0.001, max_value=2.0)
        
    if st.button("Ejecutar Simulación", type="primary"):
        try:
            steps = int(abs((xf - x0) / h))
            x = x0
            y = y0
            
            iteraciones = [{
                "Iteración": 0,
                "x": x,
                "y": y,
                "f(x,y)": eval(expr, {"__builtins__": None, "math": math}, {"x": x, "y": y})
            }]
            
            for i in range(1, steps + 1):
                f_val = eval(expr, {"__builtins__": None, "math": math}, {"x": x, "y": y})
                y = y + h * f_val
                if xf > x0:
                    x = x + h
                else:
                    x = x - h
                
                try:
                    f_val_next = eval(expr, {"__builtins__": None, "math": math}, {"x": x, "y": y})
                except:
                    f_val_next = 0.0
                    
                iteraciones.append({
                    "Iteración": i,
                    "x": round(x, 4),
                    "y": round(y, 4),
                    "f(x,y)": round(f_val_next, 4)
                })
                
            df_results = pd.DataFrame(iteraciones)
            st.success(f"¡Simulación completada! El valor estimado de y({xf}) es aproximadamente {y:.4f}")
            
            st.subheader("Tabla Descriptiva de Iteraciones")
            st.dataframe(df_results, use_container_width=True)
            
            st.subheader("📈 Gráfico de la Trayectoria de Aproximación")
            st.line_chart(data=df_results, x="x", y="y")
            
        except Exception as e:
            st.error(f"Error en la expresión matemática o en los datos: {e}")
