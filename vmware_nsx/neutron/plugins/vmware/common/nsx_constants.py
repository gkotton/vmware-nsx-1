# Copyright 2015 VMware, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# Admin statuses
ADMIN_STATE_UP = "UP"
ADMIN_STATE_DOWN = "DOWN"

ADMIN_STATUSES = [ADMIN_STATE_UP, ADMIN_STATE_DOWN]

# Port attachment types
ATTACHMENT_VIF = "VIF"
ATTACHMENT_LR = "LOGICALROUTER"

ATTACHMENT_TYPES = [ATTACHMENT_VIF, ATTACHMENT_LR]

# Replication modes
MTEP = "MTEP"
SOURCE = "SOURCE"

REPLICATION_MODES = [MTEP, SOURCE]

# Router type
ROUTER_TYPE_TIER0 = "TIER0"
ROUTER_TYPE_TIER1 = "TIER1"

ROUTER_TYPES = [ROUTER_TYPE_TIER0, ROUTER_TYPE_TIER1]
