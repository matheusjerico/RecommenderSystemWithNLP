### Arquitetura da Solução

---

#### 1. Iniciando Aplicação
Quando a aplicação é inicializada, utilizo a biblioteca [BeautifulSoup] para fazer a raspagem das URL's na página inicial da [Globo.com] e guardo as URL's que possuem o *path* com no mínimo duas unidade de "/". Após popular a Base de Dados (MongoDB) que contém as URL's e os Usuários, a aplicação já está disponível para realizar testes.

Implementei um MongoDB utilizando `docker-compose`, no qual salvo todos os registros referentes as URL's, consulto URLs específicas, consulto todas as URLs e delete todos os registros. Configurei com o Container do MongoDB com persistência de volume, para que caso o Container do MongoDB seja finalizado, não perca os documentos registrados.


#### 2. Construção da API
Para construção da API utilizei o *micro-framework* Flask.

Caso o projeto fosse para produção usaria a Google Cloud Platform , utilizando o Kubernetes Engine para deploy da API e Datastore como Base de Dados. Para deploy da API em um Cluster disponível com escalabilidade de Nodes, seguiria os passos:
1) Criação dos repositórios de ambiente (manifestos Kubernetes) e de aplicação (código da aplicação) na Cloud Source Repositories.
2) Criação dos manifestos *Deployment*, *Service*, *Ingress*, *HPA*, *ConfigMap*, *Secret* e adicioná-los no repositório de ambiente.
3) Criação de script de integração contínuoa utilizando a Cloud Build para execução de testes de unidade, build do Container e armazenamento do Conteinar no Container Registry.
4) Criação de *Trigger* na branch master do reposítorio da aplicação para acionamento dos scripts de integração contínua.
5) Criação de scrpt de entrega contínuoa utilizando a Cloud Build para realizar o deploy do manifesto Kubernetes.
6) Criação de *Trigger* na branch master do reposiório de ambiente para acionamento dos scripts de entrega contínuo.

Inicialmente, não adicionaria *Trigger* do repositório da aplicação para o repositório de ambiente, para realizar testes das configurações do Kubernetes com base em uma Imagem fixa da aplicação. 

Caso a aplicação fosse imensamente requisitada, não utilizaria soluções REST. Colocaria um serviço de mensageria (Kafka, Cloud PubSub) entre a minha API e o Cliente. Dessa forma a API consumiria nos tópicos do serviçõ de mensageria. 


#### 3. Algoritmo de Recomendação
Para realizar a recomendação de documentos similares, utilizei técnicas de processamento de linguagem natural (*NLP*), utilizando a biblioteca ```scikit-learn```, e encapsulei a solução utilizando Docker, conforme requisito do projeto.

O algoritmo de recomendação de documentos similares utiliza a técnica estatística TF-IDF, que tem o intuito de indicar a importância de uma palavra em um documento em relação a uma coleção de documentos. Após aplicar a técnica, calculamos a similaridade entre os documentos (URLs) utilizando a função trigonométrica cosseno. 

As funções Jaccard e distância Euclidiana também são utilizadas para cálculo de similaridade entre documentos. Entretanto, para cálculo de similaridade entre documentos que estão modelados em um espaço vetorial esparso, a função trigonométrica cosseno é uma das mais recomendadas e utilizadas.

O cálculo de similaridade utilizando o cosseno é melhor para capturar a semântica de cada documento, a direção que o texto aponta pode ser pensada como seu significado, de modo que textos com significados semelhantes terão grande probabilidade de serem semelhantes. A performace do algoritmo seria infinitamente superior caso analisássemos o conteúdo das páginas WEB. Tendo em vista que apenas o conteúdo das URL é pouca informação.

#### 4. Testes
Utilizei a biblioteca de testes unitárioas [Unittest] para construção dos testes. Testei todas as rotas da aplicação e validei as repostas.

### 5. Funcionamento
A aplicação possui 3 rotas:
- **POST em `/<url>/view/`**:
>Exemplo de uso: `$ curl -X POST -d "user=user1" http://localhost:8080/www.globoplay.com/v/1234567/view/`
  
Quando a rota é acionada e a URL é inserida na base com sucesso, obtemos uma resposta com status `201` e via JSON o conteúdo:

```json
{
  "success": true
}
   ```
- **GET em `/<url>/similar/`**:
>Exemplo de uso: `$ curl -X GET http://localhost:8080/https://g1.globo.com/politica/noticia/2020/05/05/bolsonaro-diz-que-nao-houve-agressao-nenhuma-zero-em-manifestacao-e-grita-cala-a-boca-para-reporteres.ghtml/similar/`

Quando a rota é aceionada e a API obtém sucesso na manipulação de dados e construção das recomendações, obtemos uma resposta com status ```200``` e via JSON as recomendações:
```json
[
    {
        "score": 0.82,
        "url": "https://g1.globo.com/politica/noticia/2020/05/05/bolsonaro-afirma-que-superintende-do-rj-sera-numero-2-da-pf-a-convite-do-novo-diretor-geral.ghtml"
    },
    {
        "score": 0.797,
        "url": "https://g1.globo.com/politica/noticia/2020/05/05/leia-a-integra-do-depoimento-de-sergio-moro-a-policia-federal.ghtml"
    },
    {
        "score": 0.545,
        "url": "https://g1.globo.com/politica/blog/andreia-sadi/post/2020/05/05/alvo-da-ala-ideologica-regina-duarte-vai-conversar-com-bolsonaro.ghtml"
    },
    {
        "score": 0.518,
        "url": "https://g1.globo.com/politica/"
    },
    {
        "score": 0.46,
        "url": "https://g1.globo.com/pb/paraiba/noticia/2020/05/05/justica-da-espanha-mantem-condenacao-de-brasileiro-a-prisao-perpetua-pela-morte-de-tios-e-primos.ghtml"
    },
    {
        "score": 0.423,
        "url": "https://g1.globo.com/pe/pernambuco/noticia/2020/05/05/filho-de-fisioterapeuta-gravida-morta-por-coronavirus-recebe-alta-e-completa-um-mes-de-vida.ghtml"
    },
    {
        "score": 0.411,
        "url": "https://g1.globo.com/pop-arte/musica/noticia/2020/05/05/lives-de-hoje-risadaria-com-fabio-porchat-e-leandro-hassum-anelis-assumpcao-e-mais-transmissoes.ghtml"
    },
    {
        "score": 0.402,
        "url": "https://g1.globo.com/bemestar/coronavirus/noticia/2020/05/05/coronavirus-pode-ser-so-ensaio-de-uma-proxima-grande-pandemia-diz-medico-e-matematico-da-usp.ghtml"
    },
    {
        "score": 0.386,
        "url": "https://g1.globo.com/rj/rio-de-janeiro/noticia/2020/05/05/witzel-diz-que-pessoas-flagradas-em-aglomeracoes-no-rj-serao-levadas-para-delegacias-e-autuadas.ghtml"
    },
    {
        "score": 0.371,
        "url": "https://g1.globo.com/ac/acre/noticia/2020/05/05/prefeito-no-interior-do-ac-leva-a-morte-para-conscientizar-populacao-sobre-riscos-do-coronavirus.ghtml"
    }
]
```

- **DELETE `/`**:
>Exemplo de uso: `$ curl -X DELETE http://localhost:8080/`

Quando a rota é acionada e é feita a remoção dos itens da base de dados, obtemos uma resposta com status `200` e via JSON o conteúdo:

```json
{
  "success": true
}
```

#### 6. Hierarquia de Projeto
O arquivo ```Dockerfile``` é o responsável por construir a aplicação em Container. Utilizei a imagem ```Slim``` do Python pela facilidade de instalar as bibliotecas ```numpy```, ```pandas``` e ```scikit-learn```, tendo em vista que a imagem ```Alpine``` do Python mais esforço para instalar as bibliotecas.

O arquivo ```docker-compose.yaml``` é responsável por executar o Dockerfile para o formato da API ou para Test. Caso fosse requisito do projeto utilizar banco de dados, aqui seria criado o serviço referente ao MongoDB.

Estrutura de diretório e pastas da solução proposta:
```

├── README.md      
├── SOLUTION.md           
├── Makefile               
├── .gitignore         
└── projeto
    ├── __init__.py        
    ├── app.py                     <- Configuração do Flask
    ├── docker-compose.yaml        <- Docker Compose
    ├── Dockerfile                 <- Dockerfile
    ├── requirements.py            <- Bibliotecas utilizadas
    ├── run.py                     <- Inicialização da aplicação
    ├── run.sh                     <- Start da aplicação com Gunicorn
    │
    ├── views         
    │   └── __init__.py
    │   └── views.py               <- Rotas/Actions do projeto
    │
    ├── tests     
    │   └── __init__.py
    │   └── test.py                <- Testes da aplicação
    │
    └── models 
    │   └── __init__.py
    │   └── models.py              <- Metodos da manipulação de dados e nlp
    │   └── database.py              <- Metodos mongodb
    │
    └── logger      
        └── __init__.py
        └── logging_file.py        <-  Configuração de logging
```

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [BeautifulSoup]: <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
   [Globo.com]: <https://www.globo.com>
   [Unittest]: <https://docs.python.org/3/library/unittest.html>