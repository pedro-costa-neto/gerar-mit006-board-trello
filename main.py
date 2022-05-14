from trelloService import TrelloService
from openpyxl.workbook import Workbook
from datetime import datetime
from datetime import timezone
import pandas as pd
import configparser
import os

cfg = configparser.ConfigParser()
cfg.read("config.ini")

URL = cfg.get("INFO_TRELLO", "url")
TOKEN = cfg.get("INFO_TRELLO", "token")
KEY = cfg.get("INFO_TRELLO", "key")
COD_BOARD = cfg.get("INFO_TRELLO", "cod_board")

service = TrelloService(URL, TOKEN, KEY)

# Obter a lista de Labels do board
labels = service.get_labels(COD_BOARD)
for item in labels:
        print('{:0>3}) {}'.format(item['id'], item['name']))

control = True;
label_id = ''
label_name = ''

while control:
    print('Por favor, informe o número da opção: ')
    option = int(input())

    if option > len(labels):
        print('Opção invalida!')

    else:
        control = False
        label_id = labels[option - 1]['label_id']
        label_name = labels[option - 1]['name']


# Obter a lista de cards com a labels especificada
cards = service.get_cards_by_label(COD_BOARD, label_id)
report = {
    'STATUS': [],
    'PROCESSO': [],
    'DESCRIÇÃO': [],
    'DATA PENDENCIA': [],
    'DATA DE ENTREGA': [],
    'DATA CONCLUSÃO': [],
    'RESPONSÁVEL': [],
    'OBSERVAÇÃO': []
}

for item in cards:
    card_id = item['id']
    fields = service.get_field_item(card_id)
    members = service.get_members(card_id)
    comment = service.get_comment(card_id)

    status = ''
    pendingDate = ''
    deliveryDate = ''
    completionDate = ''

    if 'Status' in fields:
        status = fields['Status']
    
    if 'Data Pendencia' in fields:
        pendingDate = fields['Data Pendencia']
        date = datetime.fromisoformat(pendingDate[:-1]).astimezone(timezone.utc)
        pendingDate = date.strftime('%d/%m/%Y')

    if 'Data entrega' in fields:
        deliveryDate = fields['Data entrega']
        date = datetime.fromisoformat(deliveryDate[:-1]).astimezone(timezone.utc)
        deliveryDate = date.strftime('%d/%m/%Y')

    if status == '100% - Concluído':
        completionDate = item['dateLastActivity']
        date = datetime.fromisoformat(completionDate[:-1]).astimezone(timezone.utc)
        completionDate = date.strftime('%d/%m/%Y')

    elif not status:
        status = '0% - Não iniciado'

    report['STATUS'].append(status)
    report['PROCESSO'].append(item['name'])
    report['DESCRIÇÃO'].append(item['desc'])
    report['DATA PENDENCIA'].append(pendingDate)
    report['DATA DE ENTREGA'].append(deliveryDate)
    report['DATA CONCLUSÃO'].append(completionDate)
    report['RESPONSÁVEL'].append(members)
    report['OBSERVAÇÃO'].append(comment)

file = '{}\MIT006 {}.xlsx'.format(os.getcwd(), label_name)

colmuns = ['STATUS', 'PROCESSO', 'DESCRIÇÃO', 'DATA PENDENCIA', 'DATA DE ENTREGA', 'DATA CONCLUSÃO', 'RESPONSÁVEL', 'OBSERVAÇÃO']
dataFrame = pd.DataFrame(report, columns=colmuns)
dataFrame.to_excel(file, index=False, header=True, encoding="utf-8-sig")
