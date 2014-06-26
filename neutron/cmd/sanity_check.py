# Copyright (c) 2014 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
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

import sys

from neutron.cmd.sanity import checks
from neutron.common import config
from neutron.openstack.common import log as logging
from oslo.config import cfg


LOG = logging.getLogger(__name__)
cfg.CONF.import_group('AGENT', 'neutron.plugins.openvswitch.common.config')
cfg.CONF.import_group('OVS', 'neutron.plugins.openvswitch.common.config')


class BoolOptCallback(cfg.BoolOpt):
    def __init__(self, name, callback, **kwargs):
        self.callback = callback
        super(BoolOptCallback, self).__init__(name, **kwargs)


def check_ovs_vxlan():
    result = checks.vxlan_supported(root_helper=cfg.CONF.AGENT.root_helper)
    if not result:
        LOG.error(_('Check for Open vSwitch VXLAN support failed. '
                    'Please ensure that the version of openvswitch '
                    'being used has VXLAN support.'))
    return result


def check_ovs_patch():
    result = checks.patch_supported(root_helper=cfg.CONF.AGENT.root_helper)
    if not result:
        LOG.error(_('Check for Open vSwitch patch port support failed. '
                    'Please ensure that the version of openvswitch '
                    'being used has patch port support or disable features '
                    'requiring patch ports (gre/vxlan, etc.).'))
    return result


# Define CLI opts to test specific features, with a calback for the test
OPTS = [
    BoolOptCallback('ovs_vxlan', check_ovs_vxlan, default=False,
                    help=_('Check for vxlan support')),
    BoolOptCallback('ovs_patch', check_ovs_patch, default=False,
                    help=_('Check for patch port support')),
]


def enable_tests_from_config():
    """If a test can depend on configuration, use this function to set the
    appropriate CLI option to enable that test. It will then be possible to
    run all necessary tests, just by passing in the appropriate configs.
    """

    if 'vxlan' in cfg.CONF.AGENT.tunnel_types:
        cfg.CONF.set_override('ovs_vxlan', True)
    if cfg.CONF.AGENT.tunnel_types:
        cfg.CONF.set_override('ovs_patch', True)
    if not cfg.CONF.OVS.use_veth_interconnection:
        cfg.CONF.set_override('ovs_patch', True)


def all_tests_passed():
    res = True
    for opt in OPTS:
        if cfg.CONF.get(opt.name):
            res &= opt.callback()
    return res


def main():
    cfg.CONF.register_cli_opts(OPTS)
    cfg.CONF.set_override('use_stderr', True)
    config.setup_logging(cfg.CONF)
    config.init(sys.argv[1:], default_config_files=[])

    if cfg.CONF.config_file:
        enable_tests_from_config()

    return 0 if all_tests_passed() else 1
