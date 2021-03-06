import logging

# add filemode="w" to overwrite

logger = logging.getLogger("client")

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
# create the logging file handler

fh = logging.FileHandler("log/client.log", encoding='utf-8')

fh.setFormatter(formatter)

fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)


# Добавляем в логгер новый обработчик событий и устанавливаем уровень логгирования
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)