from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import time
import os
import sys

baseURL = 'https://getnada.com/api/v1'

class NewsLetterMessage:

    def __init__(self, title, message, color):
        self.title = title
        self.message = message
        self.color = color
        self.url = os.environ.get('DISCORD_WEBHOOK')
        print(f'URL: {self.url}')
        if ',' in self.url:
            self.url = self.url.split(',')

    def send(self):
        if self.url is list:
            for link in self.url:
                webhook = DiscordWebhook(url=link, username="Filipe Deschamps Newsletter")
                embed = DiscordEmbed(
                    title=self.title,
                    description=f'{self.message[0:1].upper()}{self.message[1:len(self.message)]}',
                    color=self.color
                )
                webhook.add_embed(embed)
                webhook.execute()
        else:
            webhook = DiscordWebhook(url=self.url, username="Filipe Deschamps Newsletter")
            embed = DiscordEmbed(
                title=self.title,
                description=f'{self.message[0:1].upper()}{self.message[1:len(self.message)]}',
                color=self.color
            )
            webhook.add_embed(embed)
            webhook.execute()

def getlastMessage():
    msg = None
    mail = os.environ.get('MAIL_ADDRESS')
    print(f'Mail: {mail}')
    response = requests.get(f'{baseURL}/inboxes/{mail}')
    data = json.loads(response.text)
    for d in data['msgs']:
        if d['fe'] == 'newsletter@filipedeschamps.com.br':
            if 'Today' in d['rf']:
                msg = d
    return msg

def getMessages(id):
    response = requests.get(f'{baseURL}/messages/html/{id}')
    soup = BeautifulSoup(response.text, features="html.parser")
    text = soup.text.replace('\r', '').replace('  ', '').replace('\n\n', '')
    list = text.split(':\n') if len(text.split(':\n')) > 1 else text.split(': \n')
    tmp = []
    for l in list[1:len(list)]:
        tmp.append(l.split(".\n"))
        print(l.split(".\n"))
    list = tmp
    tmp = []
    message = {}
    for i in list[0]:
        message['title'] = i.split(': ')[0]
        message['content'] = i.split(': ')[1].split('\r\n')[0]
        tmp.append(message)
        message = {}
    return tmp

n = len(sys.argv)
if n == 0:
    print('Informe o email e Discord WebHook Link')
else:
    os.environ['MAIL_ADDRESS'] = sys.argv[1]
    os.environ['DISCORD_WEBHOOK'] = sys.argv[2]
    for f in sys.argv:
        print(f)

    if getlastMessage() is not None:
        for m in getMessages(getlastMessage()['uid']):
            NewsLetterMessage(m['title'], m['content'], '242424').send()
            time.sleep(1)
    else:
        NewsLetterMessage('teste', 'teste', '242424').send()
        print('Nenhuma noticia encontrada')
