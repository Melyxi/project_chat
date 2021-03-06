import click
from socket import *
import datetime, time
import json
from project_chat.client_soket import ClientSocket
from project_chat.serializer import Serializer, SerializerServer
from project_chat.client import Client
import log.client_log_config
import logging

logger = logging.getLogger('client')

@click.command()
@click.option('--add', default='localhost', help='ip')
@click.option('--port', default=7777, help='port')
def main(add, port):
    with socket(AF_INET, SOCK_STREAM) as s:  # Создать сокет TCP
        s.connect((add, port))
        logger.info("connect socket")
        client_sock = ClientSocket(s)
        while True:
            account_name = input("Введите имя: ")
            client = Client(client_sock, account_name, Serializer()) # передаем сокет, имя, серилизатор
            password = input("Введите пароль: ")
            client.authenticate(password) # проходим аунтификацию вводим пароль

            try:
                data = s.recv(640)
                logger.info(f'Сообщение от сервера {dict_server}')
            except BaseException as e:
                logger.exception(f"Error! {e}")

            dict_server = SerializerServer(data).serializer_code
            code = SerializerServer(data).serializer_code_authenticate
            print('Сообщение от сервера: ', dict_server, ', длиной ', len(data), ' байт')

            while code == 200:
                logger.info(f"connect client {account_name}")
                msg = input("Введите сообщение: ")
                to_user = "#room"
                try:
                    client.message(msg=msg, to_user=to_user)  # вводим сообщение
                    logger.info(f"Сообщение отправлено, пользователем: {account_name}, кому: {to_user}")
                except BaseException as e:
                    logger.exception(f"Сообщение не отправлено")
                data = s.recv(640)

                try:
                    dict_server = SerializerServer(data).serializer_code
                    logger.info(f'Сообщение от сервера {dict_server}')
                except BaseException as e:
                    logger.exception(f"Error! {e}")

                print('Сообщение от сервера: ', dict_server, ', длиной ', len(data), ' байт')

                if msg == 'quit':
                    logger.info(f"пользователь: {account_name}, вышел")
                    break


if __name__ == '__main__':
    main()

# client
# Программа клиента, запрашивающего текущее время
#
# import click
# from socket import *
# import datetime, time
# import json
#
#
# def client_message(name):
#     msg = input("Введите сообщение: ")
#
#     data = {
#         "action": "msg",
#         "time": datetime.datetime.now().timestamp(),
#         "to": "#room_name",
#         "from": name,
#         "message": msg
#     }
#     return json.dumps(data)
#
#
# def login():
#     username = input('Введите имя: ')
#     password = input('Введите пароль: ')
#     data = {
#         "action": "authenticate",
#         "time": datetime.datetime.now().timestamp(),
#         "user": {
#             "account_name": username,
#             "password": password
#         }
#     }
#     return data
#
#
# def convert(data):
#     recv_str = data.decode('utf-8')
#     recv_msg = json.loads(recv_str)
#     return recv_msg
#
#
# ENCODING = 'utf-8'
#
#
# @click.command()
# @click.option('--add', default='localhost', help='ip')
# @click.option('--port', default=7777, help='port')
# def send_message(add, port):
#     with socket(AF_INET, SOCK_STREAM) as s:  # Создать сокет TCP
#         s.connect((add, port))  # Соединиться с сервером
#         while True:
#             msg = login()  # логинемся
#             log = json.dumps(msg)
#             s.send(log.encode(ENCODING))
#             data = s.recv(10000)
#             # print(data)
#             recv_msg = convert(data)
#             # print(recv_msg)
#             name = msg["user"]["account_name"]
#             # print(name)
#             print('Сообщение от сервера: ', recv_msg, ', длиной ', len(data), ' байт')
#             while recv_msg["response"] == 200:
#                 message = client_message(name)
#                 # print(message)
#                 s.send(message.encode(ENCODING))
#                 data = s.recv(10000)
#                 recv_message = convert(data)
#                 print('Сообщение от сервера: ', recv_message, ', длиной ', len(data), ' байт')
#                 if json.loads(message)['message'] == 'quit':
#                     break  # выходим на логировние
#
#
# if __name__ == '__main__':
#     send_message()
