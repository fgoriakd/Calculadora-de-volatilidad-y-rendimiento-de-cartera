# ==============================================================================
# 0. INTERFAZ GRÁFICA PARA CONFIGURACIÓN DE PARÁMETROS
# ==============================================================================
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Diccionario global para guardar los inputs de la interfaz
params = {}

def seleccionar_archivo():
    ruta = filedialog.askopenfilename(
        title="Selecciona tu archivo de Excel CARTERA",
        filetypes=[("Archivos de Excel", "*.xlsx *.xls")]
    )
    if ruta:
        lbl_archivo.config(text=os.path.basename(ruta))
        params['ruta_archivo'] = ruta

def ejecutar_programa():
    # Validación de archivo seleccionado
    if 'ruta_archivo' not in params:
        messagebox.showerror("Error", "Por favor, selecciona un archivo de Excel.")
        return
    
    try:
        # Guardar inputs en el diccionario de parámetros
        params['skiprows'] = int(entry_skiprows.get())
        params['nrows'] = int(entry_nrows.get())
        params['col_tickers'] = int(entry_col_tickers.get())
        params['col_weights'] = int(entry_col_weights.get())
        params['start'] = entry_start.get()
        params['end'] = entry_end.get()
        params['rf'] = float(entry_rf.get())
        params['benchmark'] = entry_benchmark.get().strip()
        
        # Cerrar la interfaz para continuar con el script
        root.destroy()
    except ValueError:
        messagebox.showerror("Error", "Por favor, verifica que las filas, columnas y la RF sean valores numéricos válidos.")

# --- Construcción de la Ventana Principal ---
root = tk.Tk()
root.title("Configurador de Portfolio - Analítica Financiera")
root.geometry("450x480")
root.resizable(False, False)

# Estilo para ordenamiento visual
style = ttk.Style()
style.theme_use('clam')

# 1. Sección Archivo
frame_file = ttk.LabelFrame(root, text=" 1. Archivo de Origen ", padding=10)
frame_file.pack(fill="x", padx=15, pady=5)

btn_buscar = ttk.Button(frame_file, text="Seleccionar Excel", command=seleccionar_archivo)
btn_buscar.pack(side="left", padx=5)
lbl_archivo = ttk.Label(frame_file, text="Ningún archivo seleccionado", foreground="gray")
lbl_archivo.pack(side="left", padx=5)

# 2. Sección Estructura Excel
frame_excel = ttk.LabelFrame(root, text=" 2. Mapeo del Excel (Vectores) ", padding=10)
frame_excel.pack(fill="x", padx=15, pady=5)

ttk.Label(frame_excel, text="Fila comienzo de vectores (0=1,1=2)").grid(row=0, column=0, sticky="w", pady=2)
entry_skiprows = ttk.Entry(frame_excel, width=8)
entry_skiprows.insert(0, "1")
entry_skiprows.grid(row=0, column=1, pady=2)

ttk.Label(frame_excel, text="Cantidad de activos:").grid(row=1, column=0, sticky="w", pady=2)
entry_nrows = ttk.Entry(frame_excel, width=8)
entry_nrows.insert(0, "21")
entry_nrows.grid(row=1, column=1, pady=2)

ttk.Label(frame_excel, text="Columna Tickers (0=A, 1=B...):").grid(row=2, column=0, sticky="w", pady=2)
entry_col_tickers = ttk.Entry(frame_excel, width=8)
entry_col_tickers.insert(0, "1")
entry_col_tickers.grid(row=2, column=1, pady=2)

ttk.Label(frame_excel, text="Columna Weights (0=A, 1=B...):").grid(row=3, column=0, sticky="w", pady=2)
entry_col_weights = ttk.Entry(frame_excel, width=8)
entry_col_weights.insert(0, "5")
entry_col_weights.grid(row=3, column=1, pady=2)

# 3. Sección Parámetros Financieros
frame_fin = ttk.LabelFrame(root, text=" 3. Configuración del Análisis ", padding=10)
frame_fin.pack(fill="x", padx=15, pady=5)

ttk.Label(frame_fin, text="Fecha Inicio (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", pady=2)
entry_start = ttk.Entry(frame_fin, width=12)
entry_start.insert(0, "2025-06-10")
entry_start.grid(row=0, column=1, pady=2)

ttk.Label(frame_fin, text="Fecha Fin (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", pady=2)
entry_end = ttk.Entry(frame_fin, width=12)
entry_end.insert(0, "2026-06-10")
entry_end.grid(row=1, column=1, pady=2)

ttk.Label(frame_fin, text="Benchmark Ticker Yahoo:").grid(row=2, column=0, sticky="w", pady=2)
entry_benchmark = ttk.Entry(frame_fin, width=12)
entry_benchmark.insert(0, "SPY.BA")
entry_benchmark.grid(row=2, column=1, pady=2)

ttk.Label(frame_fin, text="Tasa Libre Riesgo (RF - ej: 0.04):").grid(row=3, column=0, sticky="w", pady=2)
entry_rf = ttk.Entry(frame_fin, width=12)
entry_rf.insert(0, "0.04")
entry_rf.grid(row=3, column=1, pady=2)

# Botón de Procesamiento
btn_ejecutar = ttk.Button(root, text="🚀 Procesar Portfolio", command=ejecutar_programa)
btn_ejecutar.pack(pady=15)

# Forzar a que la ventana se quede esperando los inputs
root.mainloop()

# Si la ventana se cierra sin haber guardado los parámetros mínimos, frena la ejecución
if 'ruta_archivo' not in params:
    print("[INFO] Ejecución cancelada por el usuario.")
    exit()

# ==============================================================================
# 1. PROCESAMIENTO DEL EXCEL DINÁMICO
# ==============================================================================
ultimo_excel = params['ruta_archivo']

df_cartera = pd.read_excel(
    ultimo_excel,
    skiprows=params['skiprows'],
    nrows=params['nrows'],
    header=None
)

tickers = df_cartera[params['col_tickers']].tolist()
weights = df_cartera[params['col_weights']].tolist()

# Limpieza de nulos o espacios en blanco
tickers = [str(t).strip() for t in tickers if pd.notna(t)]
weights = [float(w) for w in weights if pd.notna(w)]

print("\n--- Vectores cargados con éxito ---")
print("Tickers:", tickers)
print("Weights:", weights)

# ==============================================================================
# 2. CONFIGURACIÓN DE PARÁMETROS Y DESCARGA DE DATOS
# ==============================================================================
start = params['start']
end = params['end']
risk_free_rate = params['rf']
benchmark = params['benchmark']

tickers_descarga = list(set(tickers + [benchmark]))

print(f"\n[INFO] Descargando precios históricos desde {start} hasta {end}...")
data_download = yf.download(
    tickers_descarga,
    start=start,
    end=end,
    auto_adjust=True,
    progress=False
)

prices_all = data_download['Close'].dropna()
prices_assets = prices_all[tickers]
prices_benchmark = prices_all[benchmark]

# ==============================================================================
# 3. CÁLCULO DE RETORNOS Y MÉTRICAS DEL PORTAFOLIO
# ==============================================================================
returns = prices_assets.pct_change().dropna()

weights_series = pd.Series(weights, index=tickers)
weights_aligned = weights_series.loc[returns.columns].values

portfolio_returns = returns.dot(weights_aligned)
trading_days = 252

cumulative_return = (1 + portfolio_returns).prod() - 1
annual_return = (1 + cumulative_return)**(trading_days / len(portfolio_returns)) - 1
annual_volatility = portfolio_returns.std() * np.sqrt(trading_days)
sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility

benchmark_returns_diarios = prices_benchmark.loc[portfolio_returns.index].pct_change().dropna()
tracking_error = (portfolio_returns - benchmark_returns_diarios).std() * np.sqrt(trading_days)

# ==============================================================================
# 4. RESULTADOS EN PANTALLA
# ==============================================================================
print("\n" + "="*40)
print("----- RESULTADOS DEL PORTAFOLIO -----")
print("="*40)
print(f"Desde: {returns.index[0].strftime('%Y-%m-%d')} hasta {returns.index[-1].strftime('%Y-%m-%d')}")
print(f"Rentabilidad acumulada: {cumulative_return:.2%}")
print(f"Rentabilidad anualizada: {annual_return:.2%}")
print(f"Volatilidad anualizada: {annual_volatility:.2%}")
print(f"Ratio de Sharpe: {sharpe_ratio:.2f}")
print("="*40)
print(f"Tracking Error con Benchmark: {tracking_error:.2%}")
print("="*40)

# ==============================================================================
# 5. EVOLUCIÓN COMPRADA VS BENCHMARK (Con pd.concat)
# ==============================================================================
portfolio_value = (1 + portfolio_returns).cumprod()
benchmark_returns = prices_benchmark.loc[portfolio_value.index].pct_change().dropna()
benchmark_value = (1 + benchmark_returns).cumprod()

inicio_portfolio = pd.Series([1.0], index=[portfolio_value.index[0] - pd.Timedelta(days=1)])
inicio_benchmark = pd.Series([1.0], index=[benchmark_value.index[0] - pd.Timedelta(days=1)])

portfolio_value = pd.concat([inicio_portfolio, portfolio_value])
benchmark_value = pd.concat([inicio_benchmark, benchmark_value])

# ==============================================================================
# 6. GRÁFICO COMPARATIVO CON RESULTADOS INTEGRADOS
# ==============================================================================
# Creamos la figura y los ejes. Dejamos un margen derecho más amplio para la tabla de datos
fig, ax = plt.subplots(figsize=(14, 6))
plt.subplots_adjust(right=0.75) 

# Dibujamos las líneas de rendimiento
ax.plot(portfolio_value.index, portfolio_value, label='Mi Portfolio Real (Excel)', linewidth=2, color='#1f77b4')
ax.plot(benchmark_value.index, benchmark_value, label=f'Benchmark ({benchmark})', linestyle='--', alpha=0.8, color='#ff7f0e')

# Títulos y etiquetas del gráfico
ax.set_title('Evolución de $1 invertido: Portfolio Real vs Benchmark', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Fecha', fontsize=11)
ax.set_ylabel('Valor acumulado ($)', fontsize=11)
ax.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='none')
ax.grid(True, linestyle=':', alpha=0.6)

# --- CUADRO DE RESULTADOS (Inyectado directamente en la ventana gráfica) ---
texto_resultados = (
    f"📊 METRICAS DEL PORTFOLIO\n"
    f"{"—"*27}\n"
    f"📅 Período Evaluado:\n"
    f"   {returns.index[0].strftime('%Y-%m-%d')} a {returns.index[-1].strftime('%Y-%m-%d')}\n\n"
    f"📈 Rentabilidad:\n"
    f"   • Acumulada:  {cumulative_return:+.2%}\n"
    f"   • Anualizada: {annual_return:+.2%}\n\n"
    f"📉 Riesgo y Eficiencia:\n"
    f"   • Volatilidad An.: {annual_volatility:.2%}\n"
    f"   • Ratio de Sharpe: {sharpe_ratio:.2f}\n\n"
    f"🎯 Comparación vs índice:\n"
    f"   • Tracking Error:  {tracking_error:.2%}"
)

# Colocamos el cuadro de texto afuera del gráfico (a la derecha) usando coordenadas de la figura
fig.text(
    0.77, 0.45,                 # Posición X, Y en la ventana
    texto_resultados, 
    fontsize=11, 
    family='monospace',         # Fuente monoespaciada para que las columnas queden perfectamente alineadas
    verticalalignment='center',
    bbox=dict(
        boxstyle='round,pad=1', 
        facecolor='#f8f9fa',    # Fondo gris claro institucional
        edgecolor='#ccc0c0',    # Borde sutil
        alpha=1.0
    )
)

# Mostramos la ventana unificada
plt.show()