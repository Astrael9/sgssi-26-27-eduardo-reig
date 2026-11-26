# Laboratorio: Google Colab

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar usuario `lsi` si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.
- Cuenta Google utilizada para servidor Google Cloud.

## Google Colab

### Introducción

[Google Colab](https://colab.research.google.com) es un entorno de desarrollo basado en [Jupyter Notebooks](https://jupyter.org) que permite ejecutar código Python en la nube sin instalar software adicional.

En este laboratorio aprenderemos a:

- Crear y ejecutar notebooks en Google Colab.
- Utilizar celdas de código y texto Markdown.
- Cargar y analizar datos.
- Entrenar un modelo sencillo de Machine Learning.
- Evaluar su rendimiento.
- Identificar algunos riesgos de seguridad relacionados con modelos de Machine Learning.

Trabajaremos con herramientas y conjuntos de datos públicos. No subas información personal, datos sensibles ni credenciales a Google Colab.

### Crear un notebook en Colab

Accede a [Colab](https://colab.research.google.com) con la misma cuenta de Google con la que creaste el servidor de Google Cloud. Crea un nuevo notebook (File; New Notebook) y renómbralo a `ml-sec.ipynb`.

Ejecuta la siguiente celda:

```python
print("Hi Colab World")
```

Añade una celda de texto.

> ¿Qué diferencia existe entre una celda de código y una celda de texto?  
*Las celdas de código son ejecutables, mientras que las de texto solo renderizan el texto con un formato*

> ¿Qué ocurre si ejecutas varias veces la misma celda?  
*Que se devuelve varias veces el resultado esperado*

### Conocer el entorno de ejecución

Ejecuta:

```python
import platform

print(platform.platform())
print(platform.python_version())
```

Comprueba la memoria disponible:

```python
!free -h
```

Comprueba el contenido del directorio actual:

```python
!ls
```

> ¿Dónde se ejecuta realmente el código?  
*En una máquina virtual Linux en los servidores de Google*

> ¿Qué diferencia existe entre tu ordenador local y el entorno de ejecución de Colab?  
*El entorno de ejecución de Colab es remoto, y no tengo acceso físico a él, además de que se trata de una máquina virtual, que comparte los recursros de una máquina física con otras máquians virtuales. Mi ordenador local se trata de una sola máquina física que utiliza sus propios recursos hardware*

### Trabajar con datos

Importa las librerías necesarias:

```python
import pandas as pd
```

Carga un conjunto de datos público:

```python
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"

df = pd.read_csv(url)

df.head()
```

Obtén información general:

```python
df.info()
```

Obtén estadísticas descriptivas:

```python
df.describe()
```

> ¿Cuántas filas y columnas contiene el conjunto de datos?  
*Contiene 5 columnas y 150 filas de información*

> ¿Qué representa cada columna?  
*Las columnas represntan medidas acerca de la longitud y anchura del sépalo de las flores muestreadas, la longitud y anchura de sus pétalos y la especie de flor*

### Visualizar los datos

Instala y utiliza bibliotecas de visualización:

```python
import seaborn as sns
import matplotlib.pyplot as plt
```

Visualiza las relaciones entre variables:

```python
sns.pairplot(df, hue="species")
plt.show()
```

> ¿Se distinguen visualmente las diferentes especies?  
*Sí, porque cada especie tiene asociado un color distinto*

> ¿Qué variables parecen más útiles para clasificarlas?  
*Aquellas cuyas distribuciones son más distintas, que en este caso se trata de la anchura del pétalo y su longitud*

### Entrenar un modelo de Machine Learning

Importa las herramientas necesarias:

```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
```

Separa datos y etiquetas:

```python
X = df.drop("species", axis=1)
y = df["species"]
```

Divide entrenamiento y prueba:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)
```

Crea y entrena el modelo:

```python
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
```

Realiza predicciones:

```python
predictions = model.predict(X_test)
```

Calcula la precisión:

```python
accuracy_score(y_test, predictions)
```

> ¿Qué significa la precisión obtenida?  
*Indica la proporción de predicciones correctas que ha realizado el modelo sobre el conjunto de prueba (X_test, y_test) respecto al total de muestras evaluadas. Una precisión de `1.0` indica que ha acertado todo*

> ¿Es suficiente una precisión elevada para confiar plenamente en el modelo?  
*No. Una precisión alta puede verse afectada por sobreajuste (overfitting), desbalanceo de clases, datos de prueba poco representativos, fuga de datos (data leakage) o vulnerabilidad ante entradas manipuladas o anómalas en producción.*

### Interpretar el modelo

Visualiza el árbol de decisión:

```python
from sklearn.tree import plot_tree

plt.figure(figsize=(12,8))

plot_tree(
    model,
    feature_names=X.columns,
    class_names=model.classes_,
    filled=True
)

plt.show()
```

> ¿Qué variables aparecen cerca de la raíz del árbol?  
*La anchura y lóngitud de pétalo, que son aquellas cuyas distribuciones para cada especie se diferencian más. Tiene sentido porque son las variables con las que más rápidamente se puede distinguir la especie*

> ¿Por qué puede ser útil entender cómo toma decisiones un modelo?  
*Por conocer los factores en los que se basa a la hora de decidir y poder detectar sesgos o atajos en las decisiones derivados de una muestra sesgada o incompleta*

### Guardar el notebook en GitHub

Selecciona: File; Save a copy in GitHub

O descarga el notebook: File; Download; Download .ipynb

Sube el notebook a tu repositorio de GitHub.

> ¿Qué ventajas tiene almacenar el notebook bajo control de versiones?  
*Permite llevar un historial de cambios, volver a versiones anteriores si algo falla,tener respaldo ante pérdidas del entorno y colaborar de forma ordenada*

### Seguridad en Machine Learning

Los modelos de Machine Learning también presentan riesgos de seguridad. En esta sección analizaremos algunos ejemplos.

#### Envenenamiento de datos (Data Poisoning)

Un atacante modifica parte de los datos de entrenamiento para alterar el comportamiento del modelo.

Ejecuta:

```python
df_poisoned = df.copy()

df_poisoned.loc[0:10, "species"] = "setosa"
```

Observa las primeras filas:

```python
df_poisoned.head(15)
```

> ¿Qué efecto puede tener modificar etiquetas de entrenamiento?  
*Pues alterar la realidad de los datos y por tanto entrenar al modelo con datos incorrectos*

> ¿Por qué es importante verificar el origen y calidad de los datos?  
*Porque la precisión del modelo predictivo depende totalmente de la calidad de los datos con los que se ha entrenado. No podemos ir uno por uno verificando que los datos sean auténticos, por lo que hemos de poder confiar en su fuente*

#### Modelos con sesgos

Calcula cuántas muestras existen de cada clase:

```python
df["species"].value_counts()
```

> ¿Qué problemas podrían aparecer si una clase estuviera muy poco representada? ¿Cómo afectaría esto a la calidad de las predicciones?  
*Sucedería que las distribuciones estadísticas de la muestra serían poco precisas en comparación con las de la realidad, lo que supone que el modelo sea menos preciso también, no solo para detectar los elementos de esa clase, sino también para detectar los elementos de otras clases*


