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

#!/usr/bin/env bash

# This script installs Greenplum database and sets up environment.

set -e
set -x

# Check for mandatory build argument
GREENPLUM_DATABASE_RPM_URL="$1"

if [ -z "${GREENPLUM_DATABASE_RPM_URL}" ]; then
     echo "Build argument GREENPLUM_DATABASE_RPM_URL needs to be set and non-empty."
     exit
fi

yum -y update
yum -y install bash iproute less net-tools passwd
yum clean all

HOME_DIRECTORY=/home/gpadmin/
wget -P ${HOME_DIRECTORY} ${GREENPLUM_DATABASE_RPM_URL}

mkdir /var/run/sshd
chmod 755 ${SCRIPTS_DIRECTORY}/start.sh
${SCRIPTS_DIRECTORY}/start.sh gpadmin pivotal
mkdir -p ${HOME_DIRECTORY}/.ssh

ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''
ssh-keygen  -f ${HOME_DIRECTORY}/.ssh/id_rsa -N ""
cp ${HOME_DIRECTORY}/.ssh/id_rsa.pub ${HOME_DIRECTORY}/.ssh/authorized_keys
chmod 0400 ${HOME_DIRECTORY}/.ssh/authorized_keys
chmod 0400 ${HOME_DIRECTORY}/.ssh/config

chmod 755 ${HOME_DIRECTORY}/prepare.sh
rpm -i ${HOME_DIRECTORY}/greenplum-db.rpm
rm -f ${HOME_DIRECTORY}/greenplum-db.rpm

mkdir -p ${HOME_DIRECTORY}/master ${HOME_DIRECTORY}/data  ${HOME_DIRECTORY}/mirror
chown -R gpadmin:gpadmin ${HOME_DIRECTORY}
chown -R gpadmin:gpadmin ${HOME_DIRECTORY}/master
chown -R gpadmin:gpadmin ${HOME_DIRECTORY}/data
chown -R gpadmin:gpadmin ${HOME_DIRECTORY}/mirror
chown -R gpadmin:gpadmin ${HOME_DIRECTORY}/.ssh

