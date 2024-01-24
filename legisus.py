
from basedosdados import read_sql, download
from datetime import datetime, timedelta

date = datetime.now()

dt = date - timedelta(1)

df = read_sql(
	query = f'''
	select * from `basedosdados.br_imprensa_nacional_dou.secao_1` 
	where orgao like "%Ministério da Saúde%"
	and data_publicacao between date("{dt.strftime('%Y-%m-%d')}") and date("{dt.strftime('%Y-%m-%d')}")
	''',
	billing_project_id = 'Legisus'
)

print(dt)

df.to_json(f'''coleta/{dt.strftime('%d%m%Y')}.json''', orient = 'records', indent = 2)
