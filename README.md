# Monitoramento de Legislações do SUS

### Fonte dos Dados

Queries fornecidas pela equipe da @basedosdados! Segue o resumo:

> Esta tabela contém todo o conteúdo textual da Seção 1 (atos normativos, leis, decretos, resoluções, portarias etc) do Diário Oficial da União. A data mais antiga presente na tabela é do dia 12 de abril de 2019. As edições ordinárias do DOU são publicadas tipicamente uma vez por dia, perto das 4h da manhã. Entretanto, esses horários não são rígidos e podem variar, e as seções, ou partes delas, podem ser publicadas em horários diferentes. Além disso, é possível que sejam publicadas edições extras, geralmente uma ou duas, ao longo do dia. Por esse motivo, esta tabela é atualizada uma vez por dia com as matérias do dia anterior, ou seja, constam aqui as matérias mais recentes.

Para mais detalhes consulte o seguinte [link](https://basedosdados.org/dataset/0bd844d9-454a-4c47-83e2-fc15df4f5ed7?table=ac8b5008-1f7e-4ec5-a32c-043baec80cc9).

### Scripts

#### [Coleta de Informações Diárias](dou.py) (WebScrapping)

- Limpeza das consultas presente no HTML utilizado na página
- Dados muito resumidos

#### [Coleta](legisus.py) (Google Bigquery)

```
select * from `basedosdados.br_imprensa_nacional_dou.secao_1` 
where orgao like "%Ministério da Saúde%"
and data_publicacao between date("{dt.strftime('%Y-%m-%d')}") and date("{dt.strftime('%Y-%m-%d')}")
```

#### [Análise dos Dados](analise.py)

- Remoção de stopwords (nltk) e termos muito repetitivos
- Tag-amento de assuntos
- Identificação do Maranhão
- Identificação do Grupo FNS
