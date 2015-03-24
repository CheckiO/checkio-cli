import os
import sys
import logging

from tornado.tcpserver import TCPServer

from .packet import InPacket, OutPacket, PacketStructureError

PY3 = sys.version_info[0] == 3


class ClientDataInterface(object):

    USER_DATA = {}
    ROUTING = {
        InPacket.METHOD_SELECT: 'handler_select',
        InPacket.METHOD_STDOUT: 'handler_stdout',
        InPacket.METHOD_STDERR: 'handler_stderr',
        InPacket.METHOD_RESULT: 'handler_result',
        InPacket.METHOD_ERROR: 'handler_error',
        InPacket.METHOD_STATUS: 'handler_status',
        InPacket.METHOD_SET: 'handler_set',
    }

    def __init__(self, stream):
        self._stream = stream

    def dispatch(self, method, data, request_id):
        handler = getattr(self, self.ROUTING[method])
        handler(data, request_id)

    def handler_select(self, data, request_id):
        result = {}
        for item in data:
            if item not in self.USER_DATA.keys():
                continue
            result[item] = self.USER_DATA[item]
        self._stream.write_select_result(result, request_id)

    def handler_stdout(self, line, request_id):
        logging.info("checkio-cli server:: stdout: {}".format(line))

    def handler_stderr(self, line, request_id):
        logging.info("checkio-cli server:: stderr: {}".format(line))

    def handler_result(self, data, request_id):
        logging.info("checkio-cli server:: result: {}".format(data))

    def handler_error(self, data, request_id):
        logging.info("checkio-cli server:: error: {}".format(data))

    def handler_status(self, data, request_id):
        logging.info("checkio-cli server:: status: {}".format(data))

    def handler_set(self, data, request_id):
        logging.info("checkio-cli server:: set: {}".format(data))


class TCPConsoleServer(TCPServer):

    PORT = 7878

    data_interface = ClientDataInterface

    def handle_stream(self, stream, address):
        StreamReader(stream, address, self)


class StreamReader(object):

    terminator = b'\n' if PY3 else '\n'

    def __init__(self, stream, address, server):
        self.stream = stream
        self.address = address
        self.server = server
        self._is_connection_closed = False
        self._controller = self.server.data_interface(self)
        self.stream.set_close_callback(self._on_client_connection_close)
        self._read_data()

    def _on_client_connection_close(self):
        self._is_connection_closed = True
        logging.info("checkio-cli server:: Client disconnected {} ".format(self.address))

    def _read_data(self):
        self.stream.read_until(self.terminator, self._on_data)

    def _on_data(self, data):
        if PY3:
            data = data.decode('utf-8')
        logging.debug("checkio-cli server:: received: {}".format(data))
        if data is None:
            logging.error("Client sent an empty data: {}".format(self.address), exc_info=True)
        else:
            try:
                packet = InPacket.decode(data)
            except PacketStructureError as e:
                logging.error(e, exc_info=True)
            else:
                self._controller.dispatch(**packet.get_all_data())
        self._read_data()

    def write(self, method, data=None, request_id=None, callback=None):
        if self.stream.closed():
            raise Exception('Connection is closed')

        message = OutPacket(method, data, request_id).encode()
        try:
            self.stream.write(message + self.terminator, callback=callback)
            logging.debug("checkio-cli server:: write {}".format(message))
        except Exception as e:
            logging.error(e, exc_info=True)

    def write_select_result(self, result, request_id):
        self.write(OutPacket.METHOD_SELECT_RESULT, result, request_id=request_id)


def start(input_file, io_loop=None):
    import_file(input_file)
    server = TCPConsoleServer(io_loop=io_loop)
    logging.info("Running tcp server")
    server.listen(TCPConsoleServer.PORT)


def import_file(full_path_to_module):
    GLOBAL_DATA = {'__file__': full_path_to_module}
    exec(compile(open(full_path_to_module).read(), '<MYCODE>', 'exec'), GLOBAL_DATA)
    for attr in GLOBAL_DATA:
        if attr.startswith('__'):
            continue
        ClientDataInterface.USER_DATA[attr] = GLOBAL_DATA[attr]
