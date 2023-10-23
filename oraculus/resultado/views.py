from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from analise.models import Analise
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@login_required
def resultado(request):
    return render(request, "resultado.html")

def get_analises(request):
    analises = Analise.objects.all()
    return render(request, 'resultado.html', {'analises': analises})

def gerar_matriz_confusao(request):
        # Leitura do csv
    df=pd.read_csv('crop.csv')
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

    X_train, X_test, y_train, y_test = train_test_split(X, y,random_state=1, test_size=0.25)

    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    X_test_scaled = scaler.transform(X_test)

    # Aplicar o modelo KNN
    from sklearn.neighbors import KNeighborsClassifier
    qtdNeighbors = n_neighbors=5
    algoritmo = 'ball_tree'
    pesos = 'uniform'
    knn = KNeighborsClassifier(qtdNeighbors, algorithm=algoritmo, weights=pesos)
    knn.fit(X_train_scaled, y_train)
    knn.score(X_test_scaled, y_test)

    from sklearn.metrics import confusion_matrix
    mat=confusion_matrix(y_test,knn.predict(X_test_scaled))
    df_cm = pd.DataFrame(mat, list(targets.values()), list(targets.values()))
    sns.set(font_scale=1.0) # for label size
    plt.figure(figsize = (12,8))
    sns.heatmap(df_cm, annot=True, annot_kws={"size": 10},cmap="terrain")
