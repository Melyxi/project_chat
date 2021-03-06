import json
import time

from .message import Authenticate, Message


class Serializer:
    def __init__(self, dumps=json.dumps, encoding="utf-8", get_time_fn=time.time):
        self._dumps = dumps
        self._encoding = encoding
        self._get_time_fn = get_time_fn

    def serialize_authenticate(self, msg):
        if isinstance(msg, Authenticate):
            result_dict = {
                "action": "authenticate",
                "time": self._get_time_fn(),
                "user": {"account_name": msg.account_name, "password": msg.password,},
            }
            result_str = self._dumps(result_dict)
            res = result_str.encode(self._encoding)
            while len(res) < 640:
                res += b' '
            return res # Строка в байтах

    def serializer_message(self, msg):
        if isinstance(msg, Message):
            result_dict = {
                "action": "msg",
                "time": self._get_time_fn(),
                "to": msg.to,
                "from": msg.from_user,
                "message": msg.message
            }

            result_str = self._dumps(result_dict)
            res = result_str.encode(self._encoding)
            while len(res) < 640:
                res += b' '
            return res # Строка в байтах


class SerializerServer:
    def __init__(self, byte_string, loads=json.loads, encoding="utf-8"):
        self._loads = loads
        self._encoding = encoding
        self.byte_string = byte_string

    @property
    def serializer_code(self):
        revc_str = self.byte_string.decode(self._encoding)
        data = self._loads(revc_str)

        return data # словарь сообщения от сервера

    @property
    def serializer_code_authenticate(self): # код аунтификации
        #print(self.serializer_code)
        return self.serializer_code['response']

