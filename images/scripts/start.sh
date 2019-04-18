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

set -e
set -x

__create_user() {
USER=${1:-user}
useradd ${USER}
SSH_USERPASS=${2:-password}
echo -e "$SSH_USERPASS\n$SSH_USERPASS" | (passwd --stdin ${USER})
echo user: ${USER} password: $SSH_USERPASS
echo "${USER} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${USER}
}

# Call all functions
__create_user $1 $2
