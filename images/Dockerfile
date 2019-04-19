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

ARG CENTOS_VERSION=7.4
FROM clusterdock/topology_nodebase:centos${CENTOS_VERSION}

ARG SCRIPTS_DIRECTORY=/tmp/greenplum-scripts
ADD scripts ${SCRIPTS_DIRECTORY}

ADD scripts/gpinitsystem_config_template /home/gpadmin/
ADD scripts/prepare.sh /home/gpadmin/
ADD scripts/config /home/gpadmin/.ssh/

# Build arguments.
ARG GREENPLUM_DATABASE_RPM_URL

ARG GREENPLUM_DATABASE_INSTALL_SCRIPT=install_greenplum.sh
ADD ${GREENPLUM_DATABASE_INSTALL_SCRIPT} /tmp
RUN . /tmp/${GREENPLUM_DATABASE_INSTALL_SCRIPT} ${GREENPLUM_DATABASE_RPM_URL}

