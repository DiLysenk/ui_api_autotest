import socket
import random
from http import HTTPStatus


def parse_http_response(text_response):
    lines = text_response.split('\n')

    status_raw = lines[0]
    lines = lines[1:]

    message, status_code, protocol = status_raw.split(' ')

    empty_index = 1
    headers = {}
    for index, line in enumerate(lines):
        line = line.strip()
        line = line.strip('\r')
        if line == '':
            empty_index = index
            break
        print(line)
        k, _, v = line.partition(':')
        headers.setdefault(k.strip(), v.strip())
    content = ''.join(lines[empty_index + 1])
    return status_code, headers, content


HOST = "127.0.0.1"  # задаём url
# PORT = random.randint(10000, 20000)  # задаём порт
PORT = 10001
address_port = (HOST, PORT)  #


def create_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(address_port)  # биндим порт

        print(f'open address and port: curl {HOST}:{PORT}')  # сообщение об адресе и порте


        s.listen()  # слушаем порт и адрес создаётся процесс ss -nltp
        connect, address = s.accept()  # создание сокета для

        print(connect, address)


        s.close()

        print('сервер работает print')


create_socket()


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind(address_port)  # биндим порт
#
#     print(f'open address and port -- curl {HOST}:{PORT}')  # сообщение о адресе и порте
#
#     s.listen()  # слушаем порт и адрес
#     connect, address = s.accept()  # создание сокета для подключения
#
#     data = connect.recv(4096)
#
#     request_method = data.decode('utf-8').split()[0]
#     headers = data.decode('utf-8').split('\r\n')[8:]
#     headers_pretty = ''
#     for i in headers:
#         headers_pretty = headers_pretty + i + '\n'
#
#     if b"status=404" in data:
#         status_valuse = HTTPStatus.NOT_FOUND.value
#         status_phrase = HTTPStatus.NOT_FOUND.phrase
#     elif b"status=200" in data:
#         status_valuse = HTTPStatus.OK.value
#         status_phrase = HTTPStatus.OK.phrase
#     else:
#         status_valuse = HTTPStatus.OK.value
#         status_phrase = HTTPStatus.OK.phrase
#
#     status_code, headers, content = parse_http_response(data.decode())
#
#     massage = f"HTTP/1.1 200 OK\n Content-Length: 100\n Connection: close\n Content-Type: text/html\n\n <h1>Status Code {status_code} Headers: {headers}, " \
#               f"Content {content}</h1>".encode("utf-8")
#
#     connect.send(massage)
#
#
#
