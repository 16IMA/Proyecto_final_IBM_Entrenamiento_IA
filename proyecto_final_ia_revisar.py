# -*- coding: utf-8 -*-
Proyecto final IA .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1k8z_fSnRcUMY-SblOjrvmyGfDQyORqHF


# **Detección de fraudes con tarjetas de crédito**

Enlace al dataset: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

### Importa las bibliotecas necesarias

from google.colab import drive
drive.mount('/content/drive')

# Importa la bibliotecas necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

import warnings
warnings.filterwarnings("ignore")

### Importa y organiza el dataset"""

# Organizar los datos en un dataframe
data = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/creditcard.csv")
print("Puede consultar las primeras 10 filas del dataset a continuación:")
data.head(10)

### Limpia los datos

a. Valores perdidos

#Escribe tu código aquí
datos_nulos = data.isnull().sum()
print(f"La cantidad de datos nulos en cada columna del dataset es de:\n {datos_nulos}")


b. Datos duplicados

#Escribe tu código aquí
datos_duplicados = data.duplicated().sum()
print(f"La cantidad de datos duplicados en el dataset es de: {datos_duplicados}")
data_no_duplicates = data.drop_duplicates()


### Analiza los datos

Pregunta 1: ¿Cuál es el porcentaje de transacciones fraudulentas en el dataset?

# Calcula el porcentaje de transacciones fraudulentas
transacciones_fraudulentas = data_no_duplicates['Class'].sum()
transacciones = data_no_duplicates['Class'].count()
# Muestra el porcentaje de transacciones fraudulentas
porcentaje_transacciones_fraudulentas = (transacciones_fraudulentas / transacciones) * 100
print(f"El porcentaje de transacciones fraudulentas en el dataset es de: {round(porcentaje_transacciones_fraudulentas, 3)}%")

Pregunta 2: ¿Cuál es el importe medio de las transacciones fraudulentas?

# Calcula el importe medio de las transacciones fraudulentas
transacciones_fraudulentas = data_no_duplicates[data_no_duplicates['Class'] == 1]
importe_medio_transacciones_fraudulentas = transacciones_fraudulentas['Amount'].mean()

# Muestra el importe medio de las transacciones fraudulentas
print(f"El importe medio de las transacciones faudulentas es de : {round(importe_medio_transacciones_fraudulentas, 2)}")

### Visualiza los datos

Pregunta 1: ¿Cuántas transacciones fraudulentas hay en comparación con las no fraudulentas? (Utiliza un gráfico de barras)

# Cuenta el número de transacciones fraudulentas y no fraudulentes

class_data = data_no_duplicates['Class']
transacciones_fraudulentas = class_data == 1
transacciones_no_fraudulentas = class_data == 0
cantidad_transacciones_fraudulentas = transacciones_fraudulentas.sum()
cantidad_transacciones_no_fraudulentas = transacciones_no_fraudulentas.sum()
print(f"La cantidad de transacciones fraudulentas en el dataset es de: {cantidad_transacciones_fraudulentas}")
print(f"La cantidad de transacciones no fraudulentas en el dataset es de: {cantidad_transacciones_no_fraudulentas}")

# Crea un gráfico de barras para mostrar la distribución de las transacciones fraudulentas y no fraudulentas
plt.figure(figsize=(15, 8))
grafico_transacciones = plt.bar(['Transacciones Fraudulentas', 'Transacciones No Fraudulentas'], [cantidad_transacciones_fraudulentas, cantidad_transacciones_no_fraudulentas], color=['red','blue'])
plt.title("Gráfico de transacciones fraudulentas y no fraudulentas")
plt.xlabel("Tipo de transacción")
plt.ylabel("Cantidad de transacciones")
plt.ylim(1, 1000000)
plt.yscale('log')
plt.yticks([1, 10, 100, 1000, 10000, 100000, 1000000],
           ['1', '10', '100', '1k', '10k', '100k', '1M'])
plt.text(0, cantidad_transacciones_fraudulentas, str(cantidad_transacciones_fraudulentas), ha='center', va='bottom')
plt.text(1, cantidad_transacciones_no_fraudulentas, str(cantidad_transacciones_no_fraudulentas), ha='center', va='bottom')

# Muestra la distribución de las traducciones fraudulentas con respecto de las no fraudulentas

plt.show()

Pregunta 2: ¿Cuál es la distribución de los importes de las transacciones fraudulentas? (Utiliza un histograma)

# Separa los datos de transacciones fraudulentas
transacciones_fraudulentas = data_no_duplicates[data_no_duplicates['Class'] == 1]
importes_transacciones_fraudulentas = transacciones_fraudulentas['Amount']

# Crea un histograma para mostrar la distribución de los importes de las transacciones fraudulentas

plt.figure(figsize=(15, 8))
distribucion_importes_transacciones_fraudulentas = sns.histplot(transacciones_fraudulentas.Amount, bins=100, color='red', alpha=0.2, kde = True, line_kws={'linewidth': 1, 'label':'Patrón de distribución de las trasacciones fraudulentas (KDE)'})
distribucion_importes_transacciones_fraudulentas.set(title = 'Distribución de los importes de las transacciones fraudulentas')
plt.title('Distribución de los importes de las transacciones fraudulentas')
plt.xlabel('Importe')
plt.ylabel('Frecuencia')
plt.xlim(0, 2200)
plt.xticks([0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200],
           ["0", "200", "400", "600", "800", "1000", "1200", "1400", "1600", "1800", "2000", "2200"])
plt.ylim(0, 300)
plt.legend(title='Leyenda')
plt.grid(True)


# Muestra la distribución de los importes de las transacciones fraudulentas

plt.show()


## Desarrollo y evaluación de modelos

### Separa del dataset

# Separa los datos de entrenamiento y evaluación

train_dataframe = data_no_duplicates
X = train_dataframe.drop(columns=["Class"])
y = train_dataframe["Class"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Tamaño de los datos de entrenamiento es de {X_train.shape[0]} filas y {X_train.shape[1]} columnas.")
print(f"Tamaño de los datos de evaluación es de {X_test.shape[0]} filas y {X_test.shape[1]} columnas.")

### Crea y evalúa los modelos

#Escribe tu código aquí
model = RandomForestClassifier(max_depth=150, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
clf_report=classification_report(y_test, y_pred)
print(f"Reporte de clasificación:\n {clf_report}")
accuracy = accuracy_score(y_test, y_pred)
print(f"Exactitud del modelo: {round(accuracy * 100, 2)}%")