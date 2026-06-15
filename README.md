# Calculadora-de-volatilidad-y-rendimiento-de-cartera
Importante: para que funcione el script tu Excel debe llamarse "CARTERA.XLSX" y los tickers deben estar tal cual aparecen en la página de Yahoo Finance. Si precisas los valores de los activos que cotizan en Argentina, se le agrega el sufijo .BA, por ejemplo, NVDA.BA, ALUA.BA, etc.
Cuando se le da arranque al programa tarda un poco menos de 10 segundos y se abrirá una ventana en la que debes seleccionar la hoja de calculos correspondiente con los tickers y respectivos weights del portfolio. 
Primero se mapea donde se encuentran tus vectores:
En "fila comienzo de vectores" pones en que fila comienzan tus vectores. Si los vectores estan, por ejemplo en B2:B22 y F2:F22, tenes que poner 1. Si arrancan de la fila A, pones 0, si arrancan de la 2 pones 3.
El mismo razonamiento se aplica para las columnas. Si tu vector de tickers está en la columna A, pones 0. Si esta en la B, pones 1.
Una vez se da click a "Procesar portfolio" se va a abrir una ventana con el gráfico correspondiente y el análisis completo del programa. Existe un pequeño botón debajo que permite guardar la imagen de la ventana en formato PNG.
Desde releases se puede bajar el .exe de este programa
