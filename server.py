# server

# Программа сервера времени
from socket import *
import time
import click
from contextlib import closing
import json
import os

def code(code):
    with open(os.path.join(os.getcwd(), 'code.json'), encoding='utf-8') as f:
        msg = json.load(f)
        msg = msg[code]
    return json.dumps(msg)


def server_data():
    data = {

        "response": 200,
        "alert": "Сообщение принято"
    }
    return json.dumps(data)


def quit():
    data = {
        "action": "quit"
    }
    return json.dumps(data)


def convert(data):
    recv_str = data.decode('utf-8')
    recv_msg = json.loads(recv_str)
    return recv_msg

#os.path.join(os.getcwd(), 'auth.json')
def open_auth(url):
    with open(url) as f:
        auth = json.load(f)
        return auth

ENCODING = 'utf-8'

def authenticate(recv_msg, data_auth):
    if 'action' in recv_msg and recv_msg['action'] == "authenticate":

        for id in data_auth:
            print(recv_msg)
            if data_auth[id]["account_name"] == recv_msg['user']["account_name"] and data_auth[id]["password"] == \
                    recv_msg['user']["password"]:

                return '200'

        return '402'

    return '403'



@click.command()
@click.option('--a', default='', help='ip')
@click.option('--p', default=7777, help='port')
def server_message(a, p):
    with socket(AF_INET, SOCK_STREAM) as s:  # Создает сокет TCP
        s.bind((a, p))  # Присваивает порт 8800
        s.listen(5)  # Переходит в режим ожидания запросов;
        # одновременно обслуживает не более
        # 5 запросов.
        while True:
            client, addr = s.accept()  # Принять запрос на соединение
            with closing(client) as cl:
                while True:
                    data = cl.recv(640)
                    recv_message = convert(data)
                    print('Сообщение: ', recv_message, ', было отправлено клиентом: ', addr, 'количество байтов', len(data))
                    recv_msg = json.loads(data)
                    url = os.path.join(os.getcwd(), 'auth.json')
                    data_auth = open_auth(url)
                    auth = authenticate(recv_msg, data_auth)

                    if auth == '200':
                        msg = code('200')  # это сообщение не идет к клиенту, после второй аунтификации
                        #print(msg.encode(ENCODING))
                        cl.send(msg.encode(ENCODING))  # во второй раз не отправляет сообщение
                        while True:
                            data = cl.recv(640)
                            recv_message = convert(data)
                            #print(type(recv_message))
                            #print(recv_message)

                            print('Сообщение: ', recv_message, ', было отправлено клиентом: ', addr, 'количество байтов', len(data))
                            massage = server_data()
                            #print(recv_message)
                            if recv_message['message'] == 'quit':
                                #print(recv_message['message'])
                                massage = quit()
                                cl.send(massage.encode(ENCODING))
                                break
                            else:
                                cl.send(massage.encode(ENCODING))

                    elif auth == '402':
                        msg = code('402')
                        cl.send(msg.encode(ENCODING))

                    elif auth == '403':
                        msg = code('403')
                        cl.send(msg.encode(ENCODING))




if __name__ == '__main__':
    server_message()
