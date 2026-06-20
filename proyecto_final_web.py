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
    "📈 2. Interpolación de Newton", 
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

# --- PESTAÑA 2: NEWTON ---
with tab2:
    st.header("Interpolación Numérica de Newton")
    st.write("Encuentra el polinomio interpolador utilizando el método de Diferencias Divididas de Newton.")
    
    m = st.number_input("Cantidad de puntos conocidos:", min_value=2, max_value=10, value=4, step=1, key="newton_m")
    
    st.subheader("Tabla de Coordenadas Conocidas")
    default_pts = np.zeros((m, 2))
    if m == 4:
        default_pts = np.array([
            [0.0, -1.0],
            [1.0, 6.0],
            [2.0, 31.0],
            [3.0, 18.0]
        ])
    df_pts = pd.DataFrame(default_pts, columns=["Coordenada X", "Coordenada Y (f(x))"])
    edited_pts = st.data_editor(df_pts, use_container_width=True, key="editor_pts_newton")
    
    xp = st.number_input("Valor de 'X' a evaluar/interpolar:", value=4.0)
    
    if st.button("Calcular Interpolación", type="primary"):
        pts_matrix = edited_pts.to_numpy(dtype=float).copy()
        x_vals = pts_matrix[:, 0]
        y_vals = pts_matrix[:, 1]
        
        # Algoritmo de Diferencias Divididas
        n_p = len(x_vals)
        coef = np.zeros([n_p, n_p])
        coef[:, 0] = y_vals # La primera columna son las Y originales
        
        for j in range(1, n_p):
            for i in range(n_p - j):
                coef[i][j] = (coef[i+1][j-1] - coef[i][j-1]) / (x_vals[i+j] - x_vals[i])
                
        # Evaluación del Polinomio en xp
        yp = coef[0, 0]
        xterm = 1.0
        detalles = [f"Coeficiente b_0 = {coef[0,0]:.4f}"]
        
        for i in range(1, n_p):
            xterm *= (xp - x_vals[i-1])
            term = coef[0, i] * xterm
            yp += term
            detalles.append(f"Término {i} añadido: b_{i} * (x-x0)... = {term:.4f}")
            
        st.success(f"¡Cálculo completado mediante Diferencias Divididas!")
        st.metric(label=f"Resultado estimado y({xp})", value=f"{yp:.4f}") # Te dará -89.00
        
        with st.expander("Ver matriz de diferencias y desarrollo"):
            st.markdown("**Matriz de Diferencias Divididas (Diagonal principal = coeficientes):**")
            # Mostrar la matriz bonita
            cols_name = ["f(x)"] + [f"Orden {i}" for i in range(1, n_p)]
            st.dataframe(pd.DataFrame(coef, columns=cols_name))
            
            st.markdown("**Desarrollo de la evaluación:**")
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
