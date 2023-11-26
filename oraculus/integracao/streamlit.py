import streamlit as st
import pandas as pd
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_extras.colored_header import colored_header
import webbrowser
import numpy as np

import streamlit as st
import sys
import streamlit_extras as ste

# Obter os parâmetros da URL
params = st.experimental_get_query_params()

# Acessar os parâmetros específicos
modelo_id = params.get('id', [''])[0]
usuario = params.get('user', [''])[0]
data_analise = params.get('data', [''])[0]
acuracia = params.get('acuracia', [''])[0]
qtdTeste = params.get('qtdTeste', [''])[0]
qtdVizinhos = params.get('qtdVizinhos', [''])[0]
algoritmo = params.get('algoritmo', [''])[0]
pesos = params.get('pesos', [''])[0]

qtdVizinhos = int(qtdVizinhos)
qtdTeste = float(qtdTeste.replace(',', '.'))
acuracia = float(acuracia.replace(',', '.'))

# Leitura do csv
df=pd.read_csv('../crop.csv')
df.head()

# Preparo da IA para entender os dados
c=df.label.astype('category')
targets = dict(enumerate(c.cat.categories))
df['target']=c.cat.codes
y=df.target
X=df[['N','P','K','temperature','humidity','ph','rainfall']]

# Preparar as escalas ph e rainfall
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

X_train, X_test, y_train, y_test = train_test_split(X, y,random_state=1, test_size=qtdTeste)

scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Aplicar o modelo KNN
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=qtdVizinhos, algorithm=algoritmo, weights=pesos)
knn.fit(X_train_scaled, y_train)
knn.score(X_test_scaled, y_test)


st.set_page_config(page_title=f"Oraculus Dashboard {modelo_id}", page_icon="../static/img/logo-oraculus.png", layout="wide")

st.sidebar.header(f"Modelo {modelo_id}")
st.sidebar.write(f'Usuário: {usuario}')
st.sidebar.write(f'Data de Análise: {data_analise}')

colored_header(
label="",
description="",
color_name="orange-70",
)

st.title(f"Modelo {modelo_id}")

colored_header(
label="",
description="",
color_name="orange-70",
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(label="Acurácia", value = acuracia)
col2.metric(label="Qtd Teste / Treino", value=qtdTeste)
col3.metric(label="Qtd Vizinhos", value=qtdVizinhos)
col4.metric(label="Algoritmo", value=algoritmo)
col5.metric(label="Pesos", value=pesos)

colored_header(
label="",
description="",
color_name="orange-70",
)

st.title("Matriz de Confusão")

from sklearn.metrics import confusion_matrix
mat=confusion_matrix(y_test,knn.predict(X_test_scaled))
df_cm = pd.DataFrame(mat, list(targets.values()), list(targets.values()))
sns.set(font_scale=1.0) 
plt.figure(figsize = (20, 20))
sns.heatmap(df_cm, annot=True, annot_kws={"size": 15},cmap="terrain")

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(pd.DataFrame(mat, list(targets.values()), list(targets.values())), annot=True, annot_kws={"size": 10}, cmap="terrain", ax=ax)
st.pyplot(fig)


def voltar(url):
    webbrowser.open(url)

url = f'http://127.0.0.1:8000/visualizar_modelo/{modelo_id}/'

if st.sidebar.button('Voltar'):
    voltar(url)


  


    


    