import yaml

from subiquitycore.models.network import NetworkModel
from subiquitycore.tests import SubiTestCase, populate_dir
from probert.network import Link


class TestNetworkModelParseNetplanConfigs(SubiTestCase):
    """Test the NetworkModel.parse_netplan_configs."""

    def test_cloud_init_written_netplan(self):
        tmpd = self.tmp_dir()
        netcfg = {
            'network': {
                'version': 2,
                'ethernets': {
                    'ens3': {'dchp4': True,
                             'match': {'macaddress': "52:54:00:47:1b:76"},
                             'set-name': 'ens3'}}}}
        link_data = {
            "addresses": [
                {"source": "dhcp", "family": 2,
                 "address": "192.168.122.81/24", "scope": "global"},
            ],
            "udev_data": {
                "DEVPATH": "/devices/pci0000:00/0000:00:03.0/virtio0/net/ens3",
                "ID_BUS": "pci",
                "ID_MODEL_FROM_DATABASE": "Virtio network device",
                "ID_MODEL_ID": "0x1000",
                "ID_NET_DRIVER": "virtio_net",
                "ID_NET_LINK_FILE": "/lib/systemd/network/99-default.link",
                "ID_NET_NAME_MAC": "enx525400471b76",
                "ID_NET_NAME_PATH": "enp0s3",
                "ID_NET_NAME_SLOT": "ens3",
                "ID_PATH": "pci-0000:00:03.0",
                "ID_PATH_TAG": "pci-0000_00_03_0",
                "ID_PCI_CLASS_FROM_DATABASE": "Network controller",
                "ID_PCI_SUBCLASS_FROM_DATABASE": "Ethernet controller",
                "ID_VENDOR_FROM_DATABASE": "Red Hat, Inc.",
                "ID_VENDOR_ID": "0x1af4",
                "IFINDEX": "2",
                "INTERFACE": "ens3",
                "SUBSYSTEM": "net",
                "SYSTEMD_ALIAS": "/sys/subsystem/net/devices/ens3",
                "TAGS": ":systemd:",
                "USEC_INITIALIZED": "1622488",
                "attrs": {
                    "addr_assign_type": "0",
                    "addr_len": "6",
                    "address": "52:54:00:47:1b:76",
                    "broadcast": "ff:ff:ff:ff:ff:ff",
                    "carrier": "1",
                    "carrier_changes": "2",
                    "dev_id": "0x0",
                    "dev_port": "0",
                    "device": None,
                    "dormant": "0",
                    "duplex": "unknown",
                    "flags": "0x1003",
                    "gro_flush_timeout": "0",
                    "ifalias": "",
                    "ifindex": "2",
                    "iflink": "2",
                    "link_mode": "0",
                    "mtu": "1500",
                    "name_assign_type": "4",
                    "netdev_group": "0",
                    "operstate": "up",
                    "phys_port_id": None,
                    "phys_port_name": None,
                    "phys_switch_id": None,
                    "proto_down": "0",
                    "speed": "-1",
                    "subsystem": "net",
                    "tx_queue_len": "1000",
                    "type": "1",
                    "uevent": "INTERFACE=ens3\nIFINDEX=2"
                }
            },
            "type": "eth",
            "netlink_data": {"ifindex": 2, "flags": 69699, "arptype": 1,
                             "family": 0, "name": "ens3"},
            "bond": {"is_master": False, "is_slave": False, "slaves": [],
                     "mode": None},
            "bridge": {"is_bridge": False, "is_port": False, "interfaces": [],
                       "options": {}},
            }

        populate_dir(
            tmpd, {'/etc/netplan/50-cloud-init.yaml': yaml.dump(netcfg)})
        link = Link.from_saved_data(link_data)
        link = Link.from_probe_data(link_data['netlink_data'],
                                    link_data['udev_data'])
        nm = NetworkModel()
        nm.parse_netplan_configs(tmpd)
        print(nm.config.config_for_device(link))
        raise Exception("BOO")

# vi: ts=4 expandtab
