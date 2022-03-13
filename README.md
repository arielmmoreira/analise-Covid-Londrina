# O Projeto
O objetivo principal do projeto é fazer uma análise de dados da situação do covid na cidade de Londrina, PR. Trabalharemos com os dados atualizados e históricos, desde o começo da pandemia.

## Etapas

### 1ª Etapa
Como objetivo secundário, e primeira etapa do projeto, queremos melhorar a visualização dos dados. Para isso, fazemos um scrapping do site que contém todos os registros de casos.

https://geo.londrina.pr.gov.br/portal/apps/opsdashboard/index.html#/d2d6fcd7cb5248a0bebb8c90e2a4a482

Não encontramos nenhum registro de arquivo ou tabela com essas informações, por isso a necessidade do scrapping. Nessa etapa estamos criando um arquivo csv para ser a nossa base.

#### Estrutura da tabela
As informações que constam no dashboard disponibilizado pela prefeitura são divididos em dois painéis: evolução dos casos e recuperados/óbitos

Os tipos de dados que constam e recuperamos dos painéis são os mesmos:
* data completa (dd-mm-yyyy)
* casos confirmados

O que muda é apenas a informação sobre o tipo de registro: confirmados, recuperados e óbitos

Queremos separar a data por dia, mês e ano, para possíveis análises futuras usando esses filtros. Para isso, usamos o seguinte regex:

        month = re.search("\s[a-zA-Z]{3}", cases[i]).group().strip(" ").lower()
        day = re.search("\s[0-9]{2}", cases[i]).group().strip(" ")
        year = re.search("\s[0-9]{4}\s", cases[i]).group().strip(" ")
        

Além dessas novas informações, acrescentamos:
* id
* novos casos
* novos recuperados
* novos óbitos
* dia da semana
* media movel confirmados
* media movel obitos

O painel covid disponibilizado pela prefeitura não traz a informações dos novos casos e óbitos por dia, apenas o acumulado. Por isso criamos um novo campo para registrar essas informações.

A média móvel, tanto de casos como de óbitos, é referente a 7 dias. Temos um array que guarda informação dos últimos sete dias, desde o começo.
Para a primeira informação de média móvel precisamos esperar 7 dias. Ao chegar nesse número, a cada dia deletamos do array o primeiro registro guardado e adicionamos o registro do dia atual, fazendo a nova média

        cases_last_seven_days = []
        period = 7
        cases_last_seven_days.append(daily_cases)
        if len(cases_last_seven_days) == period:
            moving_avg_cases = round(sum(cases_last_seven_days) / period, 2)
            cases_last_seven_days.pop(0)
            


### Próximas etapas
Em planejamento