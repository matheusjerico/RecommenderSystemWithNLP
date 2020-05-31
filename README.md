## Sistema de Recomendação utilizando Processamento de Linguagem Natural
---

## Considerações Gerais

Como funciona a solução:

* O sistema está encapsulado em container(s) Docker;
* O arquivo SOLUTION.md possui a arquitetura do projeto e os passos futuros para colocar o projeto em Produção.


## O Problema

O projeto consiste em recomendar documentos similares utilizando o algoritmo de ["quem viu isso, também viu..."](https://en.wikipedia.org/wiki/Collaborative_filtering).

>Exemplo: se o usuário **A** viu os documentos 1, 2 e 3; o **B** viu 1, 2 e 5; e o **C** viu 1, 2 e 4, a API deve dizer que o documento 1 é similar ao 2.

Para o cálculo de similaridade entre os documentos, foi utilizado a técnica de TD-IDF e similaridade de cosseno.

## A API

API HTTP com as seguintes interfaces:

### POST `/<url>/view`:

  Esse interface será chamada cada vez que um usuário ver um documento. Recebendo o parâmetro `user` no **body** do request.

>Exemplo de uso: `$ curl -X POST -d "user=user1" http://localhost:8080/www.globoplay.com/v/1234567/view/`

### GET `/<url>/similar`:

Essa interface deve retornar no formato json uma lista com os dez documentos mais similares em ordem decrescente.

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
    }
]
```

### DELETE `/`:

Remove todos os dados da base.

>Exemplo de uso: `$ curl -X "DELETE" http://localhost:8080/`


## Como utilizar

### Inicialização

Para utilizar a aplicação, utilize o Makefile:
```
make setup  # build da(s) imagem(ns) docker
make test   # executa os testes da aplicação
make run    # inicializa aplicação
```

## Detalhamento da Solução
O arquivo ```SOLUTION.MD``` apresenta o detalhamento da solução do projeto.
