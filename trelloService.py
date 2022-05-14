import requests

class TrelloService:
    def __init__(self, url, token, key):
        self.__url = url
        self.__token = token
        self.__key = key

    def get_labels(self, board_id):
        response = requests.get(self.__url + 'boards/' + board_id + '/labels?key=' + self.__key + '&token=' + self.__token)
        body = response.json()
        labels = []
        count = 0

        for item in body:
            count += 1
            label_id = item['id']
            name = item['name']

            labels.append({
                'id': count,
                'label_id': label_id,
                'name': name
            })
        
        return labels

    def get_cards_by_label(self, board_id, label_id):
        response = requests.get(self.__url + 'boards/' + board_id + '/cards?key=' + self.__key + '&token=' + self.__token)
        body = response.json()
        cards = []

        for item in body:
            labels = item['labels']

            for label in labels:
                if label['id'] == label_id:
                    cards.append(item)
                
        return cards

    def get_field_item(self, card_id):
        response = requests.get(self.__url + 'cards/' + card_id + '/customFieldItems?key=' + self.__key + '&token=' + self.__token)
        body = response.json()

        fields = {}

        for item in body:
            field = self.get_custom_field(item['idCustomField'])
            value = '' 

            if field['type'] == 'list':
                for option in field['options']:
                    if option['id'] == item['idValue']:
                        value = option['value']['text']

            elif field['type'] == 'date':
                value = item['value']['date']

            fields[field['name']] = value

        return fields

    def get_custom_field(self, field_id):
        response = requests.get(self.__url + 'customFields/' + field_id + '?key=' + self.__key + '&token=' + self.__token)
        return response.json()
        
    def get_members(self, card_id):
        response = requests.get(self.__url + 'cards/' + card_id + '/members?key=' + self.__key + '&token=' + self.__token)
        body = response.json()
        members = ''

        for item in body:
            if not members:
                members = item['fullName']
            else:
                members += ', {}'.format(item['fullName'])
        
        return members

    def get_comment(self, card_id):
        response = requests.get(self.__url + 'cards/' + card_id + '/actions?filter=commentCard&key=' + self.__key + '&token=' + self.__token)
        body = response.json()
        comment = ''

        if len(body) > 0:
            comment = body[0]['data']['text']

        return comment