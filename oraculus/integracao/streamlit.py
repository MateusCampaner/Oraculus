import streamlit as st
import pandas as pd
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")


def gerar_matriz_confusao(request):

    qtdTeste = request.POST.get('qtdTeste')
    qtdVizinhos = request.POST.get('qtdVizinhos')
    algoritmo = request.POST.get('algoritmo')
    pesos = request.POST.get('pesos')

    qtdTeste = float(qtdTeste.replace(',', '.'))
    qtdVizinhos = int(qtdVizinhos)

    # Leitura do csv
    df=pd.read_csv('../../crop.csv')
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

    from sklearn.metrics import confusion_matrix
    mat=confusion_matrix(y_test,knn.predict(X_test_scaled))
    df_cm = pd.DataFrame(mat, list(targets.values()), list(targets.values()))
    sns.set(font_scale=1.0) 
    plt.figure(figsize = (12,12))
    sns.heatmap(df_cm, annot=True, annot_kws={"size": 10},cmap="terrain")

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(pd.DataFrame(mat, list(targets.values()), list(targets.values())), annot=True, annot_kws={"size": 10}, cmap="terrain", ax=ax)
    st.pyplot(fig)

    return fig