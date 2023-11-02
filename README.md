# fii-investiments

Primeiramente deve ser feito o build da imagem que irá executar o serviço:

```
docker build -t fii-incomes . 
```

Após criar a imagem que será executada no docker basta rodar:

```
docker run -p 5000:5000 fii-incomes
```

O aplicativo funciona da seguinte maneira, primeiramente ele utilizará o site https://fiis.com.br/resumo/ para obter os rendimentos diários dos fundos mobiliários cadastrados na B3. Em sequência, caso o arquivo do dia não consiga ser baixado usando o *selenium* um arquivo de backup com cotas desatualizadas será utilizado, este localizado em database/dividend_bckp. Finalmente, após iniciar o site localizado em: localhost:5000, basta inserir as informações e receber alguns resumos sobre desempenhos provaveis do seu fundo tendo como base a cotação atual.