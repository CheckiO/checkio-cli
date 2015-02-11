import os
import json
import logging
import socket
import shutil
import tempfile

from io import BytesIO

from past.builtins import basestring
from docker import Client
from docker.utils import kwargs_from_env

from checkio_cli.mission import MissionFilesHandler
from checkio_cli.tcpserver import TCPConsoleServer


class DockerClient():

    PREFIX_IMAGE = 'checkio'
    MEM_LIMIT = '512m'
    CPU_SHARES = '512'  # Default 2014

    def __init__(self, name_image, environment):
        self._client = Client(**kwargs_from_env(assert_hostname=False))
        self.name_image = "{}/{}-{}".format(self.PREFIX_IMAGE, name_image, environment)
        self.environment = environment
        self._container = None

    def run(self):
        self.create_container()
        self.start()

    def create_container(self):
        local_ip = socket.gethostbyname(socket.gethostname())
        command = "{} {}".format(local_ip, TCPConsoleServer.PORT)
        logging.info("Docker args: {}".format(command))
        self._container = self._client.create_container(
            image=self.name_image,
            command=command,
            mem_limit=self.MEM_LIMIT,
            cpu_shares=self.CPU_SHARES
        )

    def start(self):
        self._client.start(container=self._container.get('Id'))

    def stop(self):
        self._client.stop(container=self._container.get('Id'), timeout=2)

    def remove_container(self):
        self._client.remove_container(container=self._container.get('Id'))

    def logs(self, stream=False, logs=False):
        return self._client.attach(container=self.container_id, stream=stream, logs=logs)

    @property
    def container_id(self):
        return self._container.get('Id')

    def cert_kwargs_from_env(self):
        cert_path = os.environ.get('DOCKER_CERT_PATH')
        return {
            'ca_certs': os.path.join(cert_path, 'ca.pem'),
            'client_cert': os.path.join(cert_path, 'cert.pem'),
            'client_key': os.path.join(cert_path, 'key.pem'),
            }

    def build_mission_image(self, path):
        tmp_dir = None
        try:
            tmp_dir = tempfile.mkdtemp()
            mission_source = MissionFilesHandler(self.environment, path, tmp_dir)
            mission_source.schema_parse()
            mission_source.pull_base()
            mission_source.copy_user_files()
            mission_source.make_env_runner()
            mission_source.make_dockerfile()
            self._build(name_image=self.name_image, path=mission_source.path_destination_source)
        finally:
            if tmp_dir is not None:
                shutil.rmtree(tmp_dir)

    def _build(self, name_image, path=None, dockerfile_content=None):
        fileobj = None
        if dockerfile_content is not None:
            fileobj = BytesIO(dockerfile_content.encode('utf-8'))

        logging.info("Before build")
        for line in self._client.build(path=path, fileobj=fileobj, tag=name_image, nocache=True):
            line = self._format_ouput_line(line)
            if line is not None:
                logging.info(line)

    def _format_ouput_line(self, line):
        line_str = line.decode().strip()
        data = json.loads(line_str)
        for key, value in data.items():
            # TODO: if any error - raise exception
            if isinstance(value, basestring):
                value = value.strip()
            if not value:
                return None
            return "{}: {}".format(key, value)


def start(mission, environment, path=None):
    global docker
    docker = DockerClient(mission, environment)
    if path:
        docker.build_mission_image(path)
        logging.info('Image has build')
    logging.info('Run docker:')
    docker.run()

    for line in docker.logs(stream=True, logs=True):
        try:
            logging.info(line)
        except:
            pass
docker = None