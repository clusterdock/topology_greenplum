# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import tempfile

from clusterdock.models import Cluster, Node

DEFAULT_NAMESPACE = 'clusterdock'
DEFAULT_GREENPLUM_USERNAME = 'gpadmin'
DEFAULT_GREENPLUM_PASSWORD = 'pivotal'

GREENPLUM_SQL_CLIENT_CONNECTION_PORT = 5432
GREENPLUM_SSH_HOST_PORT = 5222
GREENPLUM_SSH_CONTAINER_PORT = 22
GREENPLUM_GPSS_LISTENER_PORT = 5000
GREENPLUM_GPFDIST_SERVICE_PORT = 5001

CONFIG_JSON = """{
   "listenaddress": {
       "Host": "",
       "Port": 5000
   },
   "gpfdist": {
       "Host": "",
       "Port": 5001
   }
}
"""
CONFIG_JSON_FILE_PATH = '/home/gpadmin/config.json'
HOST_FILE_PATH = '/home/gpadmin/hostfile'

logger = logging.getLogger('clusterdock.{}'.format(__name__))


def main(args):
    node_image = '{}/{}/clusterdock:greenplum{}'.format(args.registry,
                                                        args.namespace or DEFAULT_NAMESPACE,
                                                        args.greenplum_version)

    temp_dir_name = tempfile.mkdtemp()
    logger.debug('Created temporary directory %s', temp_dir_name)
    volumes = [{'/sys/fs/cgroup': '/sys/fs/cgroup'}, {temp_dir_name: '/run'}]

    if args.predictable:
        ports = [{GREENPLUM_SQL_CLIENT_CONNECTION_PORT: GREENPLUM_SQL_CLIENT_CONNECTION_PORT},
                 {GREENPLUM_SSH_HOST_PORT: GREENPLUM_SSH_CONTAINER_PORT},
                 {GREENPLUM_GPSS_LISTENER_PORT: GREENPLUM_GPSS_LISTENER_PORT},
                 {GREENPLUM_GPFDIST_SERVICE_PORT: GREENPLUM_GPFDIST_SERVICE_PORT}]
    else:
        ports = [GREENPLUM_SQL_CLIENT_CONNECTION_PORT,
                 GREENPLUM_SSH_CONTAINER_PORT,
                 GREENPLUM_GPSS_LISTENER_PORT,
                 GREENPLUM_GPFDIST_SERVICE_PORT]
    primary_node = Node(hostname=args.primary_node[0],
                        group='primary',
                        image=node_image,
                        name='greenplum_{}'.format(args.greenplum_version),
                        ports=ports,
                        volumes=volumes)

    secondary_nodes = [Node(hostname=hostname,
                            group='secondary',
                            image=node_image,
                            volumes=volumes)
                       for hostname in args.secondary_nodes]

    nodes = [primary_node] + secondary_nodes
    cluster = Cluster(*nodes)
    cluster.primary_node = primary_node
    cluster.start(args.network, pull_images=args.always_pull)

    primary_node.put_file(HOST_FILE_PATH, '\n'.join(args.secondary_nodes))
    primary_node.put_file(CONFIG_JSON_FILE_PATH, CONFIG_JSON)

    commands = ['source /usr/local/greenplum-db/greenplum_path.sh',
                'chmod 755 /home/gpadmin/prepare.sh',
                '/home/gpadmin/prepare.sh -s {} -n 1'.format(len(args.secondary_nodes)),
                'gpinitsystem -a -c /home/gpadmin/gpinitsystem_config']
    primary_node.execute(' && '.join(commands), user='gpadmin')

    commands = ['source /usr/local/greenplum-db/greenplum_path.sh',
                "echo 'host all all 0.0.0.0/0 trust' >> /home/gpadmin/master/gpseg-1/pg_hba.conf",
                'export MASTER_DATA_DIRECTORY=/home/gpadmin/master/gpseg-1',
                '/usr/local/greenplum-db/bin/gpstop -u',
                'sudo ln -s /usr/local/greenplum-db-5.12.0/lib/libpq.so.5 /usr/lib64/libpq.so.5',
                'sudo ln -s /usr/local/greenplum-db-5.12.0/lib/libssl.so.1.0.0 /usr/lib64/libssl.so.1.0.0',
                'sudo ln -s /usr/local/greenplum-db-5.12.0/lib/libcrypto.so.1.0.0 /usr/lib64/libcrypto.so.1.0.0',
                'sudo ln -s /usr/local/greenplum-db-5.12.0/lib/libcom_err.so.3 /usr/lib64/libcom_err.so.3',
                '/usr/local/greenplum-db/bin/createdb some_db',
                "/usr/local/greenplum-db/bin/psql -d some_db -c 'CREATE EXTENSION  gpss;'"]
    primary_node.execute(' && '.join(commands), user='gpadmin')

    # Start gpss in detached mode since gpss waits indefinitely for client job requests.
    primary_node.execute('/usr/local/greenplum-db/bin/gpss /home/gpadmin/config.json', user='gpadmin', detach=True)
