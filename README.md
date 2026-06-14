# Calculadora-de-volatilidad-y-rendimiento-de-cartera
Importante: para que funcione el script tu Excel debe llamarse "CARTERA.XLSX"
Cuando se le da arranque al programa tarda un poco menos de 10 segundos y al final del script te da un boton
para que subas un archivo de Excel. Vos al script lo modificas dependiendo en que celdas tenes tu vector de
Tickers y weights (ir a 1. POCESAMIENTO DEL EXCEL). En el sector 2. CONFIGURACION DE PARAMETROS... podes elegir
la fecha de comienzo y fin de evaluacion de tu portfolio, asi tambien como el ticker del benchmark con el que lo
queres comparar, y el valor de la RF con la que desees calcular el Ratio de Sharpe.

Instrucciones:
1- Asegurarse que la composición de tu cartera esté dentro de un Excel llamado "CARTERA.xlsx". Dentro de este Excel, debe haber una columna de 
tickers (si queres ver el rendimiento con el que cotizan en Argentina tenes que agregarles el sufijo .BA, ej: NVDA.BA, BYMA.BA, etc),  y una 
columna de weights. Ambos deben estar a la misma altura. Por ejemplo, el ticker AAPL.BA en la celda B2 y su weight en la celda F2, por ejemplo.

2- Elección de filas a usar 
  ir a 1. PROCESAMIENTO DEL EXCEL y modificar las variables "skiprows" y "nrows" dependiendo de en que fila se encuentran nuestros
  vectores de Tickers y Weights. Skiprows saltea la fila donde se encuentran por ejemplo, los encabezados. Entonces si tu primer weight lo tenes
  por ejemplo en B2, skiprows=1 saltea la fila 1 y hace que el calculo comience desde la fila 2. nrows sirve para decirle al programa cuántas
  filas por debajo de la principal utilizar. Si nuestro porfolio tiene 21 activos cuyos tickers estan en las celdas (B2:B22), nrows=21.

3- Elección de columnas a usar
  Aun dentro del bloque de código 1, vas a encontrar las variables "tickers" y "weights" como tickers = df_cartera[1].tolist() y weights = df_cartera[5].tolist().
  Los numeros que se encuentran dentro de la función representan las columnas donde se encuentran los vectores de tickers y weights respectivamente.
  Si en tu Excel tus tickers se encuentran en la columna "A", el numero en df_cartera[(numero)].tolist() es 0. Si están en la columna B, =1, y así sucesivamente.
  Con el número dentro de la otra función es lo mismo. En este caso es 5 porque en el Excel de prueba el vector de weights está en la columna F.

4- Elección de fecha a analizar
  ir a 2. CONFIGURACIÓN DE PARÁMETROS Y DESCARGA DE DATOS (YAHOO FINANCE). A la función "start" se le pone la fecha que querés comenzar a analizar en formato
  estadounidense, o sea, AÑO-MES-DIA. Lo propio con la fecha de fin de análisis, en la función "end"

5- Elección de tasa libre de riesgo promedio y bechmark considerados para analizar el Ratio de Sharpe y tracking error del portfolio
  Se modifica el valor dentro de la variable "risk_free_rate". El valor no debe estar en porcentaje. Ej: 4% ==> 0.04.
  El benchmark elegido se lo escribe entre comillas ('') a la variable "benchmark". 
