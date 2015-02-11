import os
import sys
import logging

from tornado.escape import json_encode, json_decode
from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer


class ClientDataInterface(object):

    USER_DATA = {}

    @classmethod
    def handle_data(cls, data):
        logging.info("[CONSOLE-SERVER] :: Data recived: {}".format(data))
        method = data.get('method')
        if method == 'get':
            return cls.get(data['data'])
        if method == 'post':
            return cls.post(data['data'])

    @classmethod
    def get(cls, data):
        result = {}
        for item in data:
            if item not in cls.USER_DATA.keys():
                continue
            result.update({
                item: cls.USER_DATA[item]
            })
        return result

    @classmethod
    def post(cls, data):
        logging.info(data)


class TCPConsoleServer(TCPServer):

    PORT = 7878

    data_interface = ClientDataInterface

    def handle_stream(self, stream, address):
        StreamReader(stream, address, self)


class StreamReader(object):

    terminator = b'\n'

    def __init__(self, stream, address, server):
        self.stream = stream
        self.address = address
        self.server = server
        self._is_connection_closed = False
        self.stream.set_close_callback(self._on_client_connection_close)
        self._read_data()

    def _on_client_connection_close(self):
        self._is_connection_closed = True
        logging.info("[checkio-cli TCPServer] :: Client at address "
                     "{} has closed the connection".format(self.address))

    def _read_data(self):
        self.stream.read_until(self.terminator, self._on_data)

    def _on_data(self, data):
        data = data.decode('utf-8')
        if data is None:
            message = dict(err='invalid_data', desc='Client sent an empty data')
            self.send_client_response(message)
        else:
            data = json_decode(data)
            response = self.server.data_interface.handle_data(data)
            if response is not None:
                self.send_client_response(response)
        self._read_data()

    def send_client_response(self, message):
        if self._is_connection_closed:
            return
        if isinstance(message, dict):
            message = json_encode(message)
        try:
            self.stream.write("{}\n".format(message))
        except Exception as e:
            logging.error(e)


def thread_start(input_file, io_loop=None):
    import_file(input_file)
    server = TCPConsoleServer(io_loop=io_loop)
    logging.info("Running tcp server")
    server.listen(TCPConsoleServer.PORT)

    if io_loop is None:
        IOLoop.instance().start()


def import_file(full_path_to_module):
    module_dir, module_file = os.path.split(full_path_to_module)
    module_name, module_ext = os.path.splitext(module_file)
    sys.path.insert(0, module_dir)
    module_obj = __import__(module_name)
    module_obj.__file__ = full_path_to_module
    for attr in dir(module_obj):
        if attr.startswith('__'):
            continue
        ClientDataInterface.USER_DATA[attr] = getattr(module_obj, attr)
