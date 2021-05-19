# Chalange from Byebank

<h3>Sobre as Rotas</h3>

* Existe endpoints para cada processo do projeto.

* Os usuários cadastros tem autenticação por token.

* Você pode acessar os endpoints somente se o usuário estiver autenticado.

* Um plugin do chrome simples para validar a authenticação, é o [ModHeader](https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj). Mas fique avontade para usar qualquer outro.

<h3>Como Ficou Estruturado</h3>

* Criei Modalidade e Ativo como classes separadas, mas relacionados de muitos para muitos.

* Na modalidade devesse cadastrar os 3 dados exigido, como Renda Fixa, Renda Variável e Cripto.

* Em Ativo você pode escolher o nome, e selecionar uma das 3 modalidades registradas anteriormente.

* Em aplicação você precisa apenas inserir o valor que deseja aplicar e em qual o ativo. A data é altomaticamente registrada(data atual), assim que o usuário faz aplicação. A quantidade eu deixei como primarykey, como os valores de aplicação são imutáveis, este valor não altera.

* O resgate realizei de forma semelhante a aplicação.
     
* Testes feitos para Modalidade, Ativo, Aplicação e Resgate. No total foram 25 testes.

<h3>O Que Ficou Faltando</h3>

* Estruturar melhor a quantidade, para fazer a somatória somente no ativo em que foi aplicado, e não ficar como o id.

* Fazer a somatória do valor em caixa de cada aplicação feita em ativos.

* Dimuir o valor em ativos, assim que realizar uma retirada de um valor em ativo que investiu.