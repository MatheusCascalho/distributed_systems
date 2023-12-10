import sys
from dataclasses import dataclass, field
from typing import List, Any
from enum import IntEnum
import json
from socket import (
    htons,
    inet_pton,
    AF_INET,
    AF_INET6,
    AddressFamily,
    ntohs,
    socket,
    SOCK_STREAM,
    gethostbyname,
    SHUT_RDWR
)
from struct import pack, unpack


@dataclass
class ConnectionSettings:
    host_port: str
    analysis: int
    host: str = field(init=False)
    port: int = field(init=False)
    address_family: AddressFamily = field(init=False)
    binary_format: Any = field(init=False)

    def __post_init__(self):
        try:
            self.hostname, self.port = self.host_port.split(":")
            if self.port == 0:
                raise Exception(f"Valor da porta deve ser diferente de 0")
            self.port = htons(int(self.port))  # host to network short

            # Descobrindo a família IP do hostname
            self.hostname = gethostbyname(self.hostname)
            self.binary_format = inet_pton(AF_INET, self.hostname)
            self.address_family = AF_INET
        except OSError:
            try:
                self.binary_format = inet_pton(AF_INET6, self.hostname)
                self.address_family = AF_INET6
            except OSError as error:
                raise error

    def __str__(self):
        if self.address_family == AF_INET:
            version = 4
        else:
            version = 6
        port = ntohs(self.port)
        presentation = f"{self.hostname}:{port}, IPv{version}"
        return presentation

    def get_port(self):
        port = ntohs(self.port)
        return port

    __repr__ = __str__


@dataclass
class Response:
    head: str
    status: int
    message: str

    def message_json(self):
        try:
            data = json.loads(self.message)
            return data
        except:
            raise Exception("Mensagem de retorno não é do tipo JSON")


def http_get(
        path: str,
        settings: ConnectionSettings,
        timeout: int = 5
) -> Response:
    """

    :rtype: object
    """
    skt = socket(AF_INET, SOCK_STREAM)
    skt.connect((settings.hostname, settings.get_port()))
    skt.settimeout(timeout)
    message = f"GET /{path} HTTP/1.1\nHost: {settings.hostname}\n\n"
    skt.send(message.encode())

    data = ''
    buf = 'blank'
    BUFSIZE = 1024
    while len(buf) > 0:
        try:
            buf = skt.recv(BUFSIZE).decode()
            data += buf
        except:
            skt.close()
            break
    data = data.split("\n")
    if len(data) > 0 and len(data[0]) > 0:
        offset = len("HTTP /1.0")
        status = int(data[0][offset:offset+3])
        response = Response(head='\n'.join(data[:5]), status=status, message=''.join(data[5:]))
    else:
        response = Response(head="", status=500, message="empty response")
    # skt.shutdown(SHUT_RDWR)
    skt.close()
    return response


if __name__ == "__main__":
    url = 'http://localhost:9000/send_to_env/cascalho'
    cs = ConnectionSettings(
        host_port="0.0.0.0:5000",
        analysis=1
    )
    # sock = socket(AF_INET, SOCK_STREAM)
    # sock.connect((cs.hostname, cs.get_port()))
    data = http_get(
        path='/api/game/1285',
        skt=None,
        settings=cs
    )
    # sock = socket(AF_INET, SOCK_STREAM)
    # sock.connect((cs.hostname, cs.get_port()))
    data = http_get(
        path='/api/game/44',
        skt=None,
        settings=cs
    )
    from pprint import pprint
    pprint(data.message_json())