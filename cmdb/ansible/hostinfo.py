#!/usr/bin/env python
# -*- encoding: utf-8  -*-
"""
@Version: 1.0
@Author: tianbaorenjie
@License: 
@Contact: tianbaorenjie@163.com
@Site: http://
@Software: PyCharm
@Project: learn
@File: cmdb_info.py
@Time: 9/10/17 2:31 PM
"""
import json
from .runner import AdHocRunner


class HostsInfo:
    """
    use ansible setup module to gather hosts info
    """
    def __init__(self, assets):
        self.runner = AdHocRunner(assets)
        self.result = {}

    def gather_cmdb_info(self):
        cmdb_info_task = (("setup", ""),)
        info = self.runner.run(cmdb_info_task)
        # print(info)
        self.result["dark"] = {}
        self.result["contacted"] = {}
        for k, v in info["dark"].items():
            hostname = k
            self.result["dark"][hostname] = {}
            for k1, v1 in v.items():
                self.result["dark"][hostname]["result"] = v1.get("result")
        for k, v in info["contacted"].items():
            hostname = k
            # print(hostname)
            self.result["contacted"][hostname] = {}
            for k1, v1 in v.items():
                # print(k1, v1)
                facts = v1.get("result").get("ansible_facts")
                self.handle_cmdb_data(facts, hostname)
        tmp = self.result
        return tmp

    def handle_cmdb_data(self, data, hostname):
        # print(hostname, data)
        # self.result["contacted"][hostname]["disks"] = self.handle_disks(data)
        # self.result["contacted"][hostname]["networks"] = self.handle_network(data)
        # self.result["contacted"][hostname]["mounts"] = self.handle_mounts(data)
        # self.result["contacted"][hostname]["hardware"] = self.handle_hardware(data)
        # self.result["contacted"][hostname]["system"] = self.handle_system(data)
        # return self.result["contacted"]
        self.handle_disks(data, hostname)
        self.handle_networks(data, hostname)
        self.handle_mounts(data, hostname)
        self.handle_hardware(data, hostname)
        self.handle_system(data, hostname)

    def handle_disks(self, data, hostname):
        disks = []
        for disk, value in data.get("ansible_devices", None).items():
            if disk[0:2] in ["sd", "hd", "ss", "vd"]:
                dk = {disk: {
                    "model": value.get("model"), "size": value.get("size"), "vendor": value.get("vendor"),
                    "host": value.get("host"),
                }}
                disks.append(dk)
        self.result["contacted"][hostname]["disks"] = disks

    def handle_networks(self, data, hostname):
        networks = []
        default = data.get("ansible_default_ipv4")
        # networks.append({"default": {"gateway": default.get("gateway"), "interface": default.get("interface")}})
        self.result["contacted"][hostname]["gateway"] = default.get("gateway")
        self.result["contacted"][hostname]["macaddr"] = default.get("macaddress")
        nets = data.get("ansible_interfaces")
        for net in nets:
            net = net.replace("-", "_")
            tmp = data.get("ansible_"+net)
            nw = {net: {}}
            if tmp.get("ipv4"):
                nw[net]["ipv4_addr"] = tmp.get("ipv4").get("address")
                nw[net]["ipv4_net"] = tmp.get("ipv4").get("netmask")
            if tmp.get("ipv6"):
                nw[net]["ipv6_addr"] = tmp.get("ipv6")[0].get("address")
                nw[net]["ipv6_pref"] = tmp.get("ipv6")[0].get("prefix")
            nw[net]["interface"] = tmp.get("interfaces")
            nw[net]["macaddr"] = tmp.get("macaddress")
            nw[net]["module"] = tmp.get("module")
            networks.append(nw)
        self.result["contacted"][hostname]["networks"] = networks

    def handle_mounts(self, data, hostname):
        mounts = []
        tmp = data.get("ansible_mounts")

        def calculate_size(size):
            size = int(size)
            size = round(size/1024/1024/1024, 2)
            return str(size) + "GB"

        for value in tmp:
            mount = {value.get("mount"): {
                "device": value.get("device"), "fstype": value.get("fstype"), "size": calculate_size(value.get("size_total")),
                "available": calculate_size(value.get("size_available")),
            }}
            mounts.append(mount)
        self.result["contacted"][hostname]["mounts"] = mounts
        self.result["contacted"][hostname]["mounts_num"] = len(tmp)

    def handle_hardware(self, data, hostname):
        tmp = "ansible_product"
        self.result["contacted"][hostname]["product_name"] = data.get(tmp + "_name")
        self.result["contacted"][hostname]["product_serial"] = data.get(tmp + "_serial")
        self.result["contacted"][hostname]["product_uuid"] = data.get(tmp + "_uuid")
        self.result["contacted"][hostname]["machine"] = data.get("ansible_machine")
        tmp = "ansible_processor"
        self.result["contacted"][hostname]["processor_type"] = data.get(tmp)[-1]
        self.result["contacted"][hostname]["processor_count"] = data.get(tmp + "_count")
        self.result["contacted"][hostname]["processor_core"] = data.get(tmp + "_cores")

    def handle_system(self, data, hostname):
        self.result["contacted"][hostname]["swap_total"] = str(data.get("ansible_swaptotal_mb")) + "MB"
        self.result["contacted"][hostname]["swap_free"] = str(data.get("ansible_swapfree_mb")) + "MB"
        self.result["contacted"][hostname]["mem_total"] = str(data.get("ansible_memtotal_mb")) + "MB"
        self.result["contacted"][hostname]["mem_free"] = str(data.get("ansible_memfree_mb")) + "MB"
        self.result["contacted"][hostname]["vendor"] = data.get("ansible_system_vendor")
        self.result["contacted"][hostname]["node"] = data.get("ansible_nodename")
        self.result["contacted"][hostname]["bits"] = data.get("ansible_userspace_bits")
        self.result["contacted"][hostname]["kernel"] = data.get("ansible_kernel")
        self.result["contacted"][hostname]["os"] = data.get("ansible_system")
        self.result["contacted"][hostname]["distribution"] = data.get("ansible_distribution") + " " + data.get("ansible_distribution_version") + \
                            " (%s)" % data.get("ansible_distribution_release")

def test():
    assets = [
        {
            "hostname": "node1",
            "ip": "192.168.66.100",
            "port": 22,
            "username": "root",
            "password": "RedHat*Linux8"
        },
        {
            "hostname": "ascontrol",
            "ip": "192.168.66.43",
            "port": 22,
            "username": "root",
            "password": "P@ssw0rd"
        },
        {
            "hostname": "pycharm",
            "ip": "192.168.99.250",
            "port": 22,
            "username": "root",
            "password": "Debian*Linux8",
        },
    ]
    info = HostsInfo(assets)
    result = info.gather_cmdb_info()
#    print(result + "\n\n\n\n")
    print(result)

if __name__ == "__main__":
    test()
