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
from runner import AdHocRunner


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
        for k, v in info["dark"].items():
            hostname = k
            self.result[hostname] = {}
            for k1, v1 in v.items():
                self.result[hostname]["result"] = v1.get("result")
        for k, v in info["contacted"].items():
            hostname = k
            # print(hostname)
            self.result[hostname] = {}
            for k1, v1 in v.items():
                # print(k1, v1)
                facts = v1.get("result").get("ansible_facts")
                self.handle_cmdb_data(facts, hostname)
        tmp = self.result
        return json.dumps(tmp)

    def handle_cmdb_data(self, data, hostname):
        # print(hostname, data)
        self.result[hostname]["disks"] = self.handle_disks(data)
        self.result[hostname]["networks"] = self.handle_network(data)
        self.result[hostname]["mounts"] = self.handle_mounts(data)
        self.result[hostname]["hardware"] = self.handle_hardware(data)
        self.result[hostname]["system"] = self.handle_system(data)
        # return self.result
#        return tmp

    @staticmethod
    def handle_disks(data):
        disks = []
        for disk, value in data.get("ansible_devices", None).items():
            if disk[0:2] in ["sd", "hd", "ss", "vd"]:
                dk = {disk: {
                    "model": value.get("model"), "size": value.get("size"), "vendor": value.get("vendor"),
                    "host": value.get("host"),
                }}
                disks.append(dk)
        return disks

    @staticmethod
    def handle_network(data):
        network = []
        default = data.get("ansible_default_ipv4")
        network.append({"default": {"gateway": default.get("gateway"), "interface": default.get("interface")}})
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
            network.append(nw)
        return network

    @staticmethod
    def handle_mounts(data):
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
        return mounts

    @staticmethod
    def handle_hardware(data):
        hardware = []
        tmp = "ansible_product"
        product = {"product": {
            "name": data.get(tmp+"_name"), "serial": data.get(tmp+"_serial"), "uuid": data.get(tmp+"_uuid"),
            "version": data.get(tmp+"_version"), "machine": data.get("ansible_machine"),
        }}
        tmp = "ansible_processor"
        processor = {"processor": {
            "type": data.get(tmp)[-1], "cores": data.get(tmp+"_cores"), "count": data.get(tmp+"_count"),
            "vcpus": data.get(tmp+"_vcpus"),
        }}
        hardware.append(product)
        hardware.append(processor)
        return hardware

    @staticmethod
    def handle_system(data):
        system = []
        tmp = {
            "swap_total": str(data.get("ansible_swaptotal_mb")) + "MB",
            "swap_free": str(data.get("ansible_swapfree_mb")) + "MB",
            "mem_total": str(data.get("ansible_memtotal_mb")) + "MB",
            "mem_free": str(data.get("ansible_memfree_mb")) + "MB",
            "vendor": data.get("ansible_system_vendor"),
            "node": data.get("ansible_nodename"), "bits": data.get("ansible_userspace_bits"),
            "kernel": data.get("ansible_kernel"), "os": data.get("ansible_system"),
            "distribution": data.get("ansible_distribution") + " " + data.get("ansible_distribution_version") +
                            " (%s)" % data.get("ansible_distribution_release")
        }
        system.append(tmp)
        return system


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
    print(json.loads(result))

if __name__ == "__main__":
    test()
