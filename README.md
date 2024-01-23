# Oraculus

Projeto desenvolvido por Mateus Eduardo Campaner durante a matéria de Estágio II no Centro Universitário Filadélfia

Descrição do Sistema

O Oraculus é um sistema cujo objetivo principal é realizar a predição da me lhor colheita com base em análises de solo, inserindo dados de Nitrogênio, Fósforo, Potássio, Temperatura, Umidade, pH e Chuva, após enviados o sistema retornará a melhor colheita com base nos dados inseridos, além de trazer outras informações es tatísticas, o usuário também poderá salvar a análise para consultas futuras, além de ter a possibilidade de tirar um relatório em formato pdf para utilização.

O sistema também conta com a possibilidade de configurar o algoritmo KNN utilizado, sendo possível alterar a proporção de teste / treino, número de vizinhos, o algoritmo a ser usado para computar os dados dos vizinhos e a função de peso a ser utilizada na predição, após treinamento do algoritmo com todas essas informações o sistema retorna a acurácia do modelo treinado, e também conta com o salvamento do algoritmo para ser utilizando nas análises. 

Os dados de análise e de modelo treinado salvos, ficam disponiveis no sis tema na seção de acessar dados, para que o usuário possa consultá-los quando pre cisar, nas análises o usuário além de consultar os dados da análise poderá extrair um relatório contendo as informações da colheita prevista. 
Para os modelos treinados o usuário poderá também acessar um dashboard para obter mais informações sobre o modelo treinado. 

Além disso o sistema conta com uma área de recomendação de colheitas onde o usuário poderá escolher uma das colheitas disponíveis e mostrar dados esta tísticos como média, valores mínimos, valores máximos e desvio padrão dos dados de Nitrogênio, Fósforo, Potássio, Temperatura, Umidade, pH e Chuva da colheita es colhida, além de poder extrair um relatório pdf sobre os dados obtidos.

Instruções para rodar o projeto:

No terminal digite:

pip install django
pip install streamlit
pip install stremlit-extras

Crie um superusuario:

python manage.py createsuperuser

Altere as configurações do banco de dados no arquivo:

settings.py a partir da linha 76

Acesse o caminho Oraculus/oraculus e rode o projeto com:

python manage.py runserver

Avra um outro terminal e acesse o caminho Oraculus/oraculus/integracao e rode o streamlit com:

streamlit run streamlit.py 

