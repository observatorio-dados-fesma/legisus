
from requests import get
from re import findall
from json import loads, dump
from datetime import datetime, timedelta

class Dou(object):	
	
	def get_data_dou_saude(self, date: str):
	
		'''format date: %d-%m-%Y'''

		try:

			url = f'https://www.in.gov.br/leiturajornal?org=Minist%C3%A9rio%20da%20Sa%C3%BAde&data={date}#daypicker'
		
			data = get(url).text
		
			print(data)

			text_data = findall(r'<script id="params" type="application/json">\n\t(.*?)\n', data)[0]

			return loads(text_data)

		except:

			return []
	
	def tidy_data(self, date):

		ontem_x = datetime.now() - timedelta(1)
		ontem_x = ontem_x.strftime('%d/%m/%Y')

		data = self.get_data_dou_saude(date = date)['jsonArray']

		if len(data) < 1:

			return [{
				'pubName': 'DO1',
				'urlTitle': 'Sem Leis Publicadas Hoje',
				'numberPage': '116',
				'subTitulo': '',
				'titulo': '',
				'title': 'Sem Leis Publicadas Hoje',
				'pubDate': f'{ontem_x}',
				'content': 'Sem Leis Publicadas Hoje',
				'editionNumber': '159',
				'hierarchyLevelSize': 2,
				'artType': 'Sem Leis Publicadas Hoje',
				'pubOrder': 'DO100046:00001:00000:00000:00000:00000:00000:00000:00000:00000:00054:00009',
				'hierarchyList': ['Minist\u00e9rio da Sa\u00fade'],
				'hierarchyStr': 'Minist\u00e9rio da Sa\u00fade/Gabinete da Ministra'
			}]

		else:

			data = [i for i in data if i['hierarchyList'][0] == 'Ministério da Saúde']
	
			data = [{k: v for k,v in i.items() if k != 'hierarchyList'} for i in data]

			return data

	def save_data_yesterday(self, date: str):

		with open(f'S:/05. FUNDO ESTADUAL DE SAÚDE/06. ANO 2024/1. Controle Financeiro/1. Recurso Federal/01. Painel Legislação do SUS/diario_ontem.json', 'w') as file:
		
			dump(self.tidy_data(date = date), file, indent = 2)

	def save_data_today(self, date: str):

		with open(f'S:/05. FUNDO ESTADUAL DE SAÚDE/06. ANO 2024/1. Controle Financeiro/1. Recurso Federal/01. Painel Legislação do SUS/diario_dia.json', 'w') as file:
		
			dump(self.tidy_data(date = date), file, indent = 2)

if __name__ == '__main__':

	dou = Dou()
	
	hoje = datetime.now().strftime('%d-%m-%Y')
	
	ontem = datetime.now() - timedelta(1)
	ontem = ontem.strftime('%d-%m-%Y')
	
	dou.save_data_today(date = hoje)
	dou.save_data_yesterday(date = ontem)
