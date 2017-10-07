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
@File: inventory.py
@Time: 9/9/17 11:30 PM
"""
from ansible.inventory import Inventory, Host, Group
from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader


class ApyHost(Host):
    def __init__(self, asset):
        self.asset = asset
        self.name = name = asset.get("hostname") or asset.get("ip")
        self.port = port = asset.get("port") or 22
        super(ApyHost, self).__init__(name, port)
        self.set_all_variable()

    def set_all_variable(self):
        asset = self.asset
        self.set_variable("ansible_host", asset["ip"])
        self.set_variable("ansible_port", asset["port"])
        self.set_variable("ansible_user", asset["username"])

        # 添加密码和密钥
        if asset.get("password"):
            self.set_variable("ansible_ssh_pass", asset["password"])
        if asset.get("private_key"):
            self.set_variable("ansible_ssh_private_key_file", asset["private_key"])

        # 添加become支持
        become = asset.get("become", False)
        if become:
            self.set_variable("ansible_become", True)
            self.set_variable("ansible_become_method", become.get("method", "sudo"))
            self.set_variable("ansible_become_user", become.get("user", "root"))
            self.set_variable("ansible_become_pass", become.get("pass", ""))
        else:
            self.set_variable("ansible_become", False)


class ApyInventory(Inventory):
    """提供生成Ansible Inventory对象方法"""

    def __init__(self, host_list=None):
        if not host_list:
            host_list = []
        assert isinstance(host_list, list)
        self.host_list = host_list
        # print(self.host_list)
        self.loader = DataLoader()
        self.variable_manager = VariableManager()
        super(ApyInventory, self).__init__(self.loader, self.variable_manager, host_list=host_list)

    def parse_inventory(self, host_list):
        """
        动态构建Ansible Inventory
        :param host_list: [
                {
                    "name": "asset_name",
                    "ip": <ip>,
                    ......
                }
            ]
        :return: Ansible的inventory对象
        """
        ungrouped = Group("ungrouped")
        all_groups = Group("all")
        all_groups.add_child_group(ungrouped)
        self.groups = dict(all_groups=all_groups, ungrouped=ungrouped)

        for asset in host_list:
            host = ApyHost(asset=asset)
            asset_groups = asset.get("groups")
            if asset_groups:
                for group_name in asset_groups:
                    if group_name not in self.groups:
                        group = Group(group_name)
                        self.groups[group_name] = group
                    else:
                        group = self.groups[group_name]
                    group.add_host(host)
            else:
                ungrouped.add_host(host)
            all_groups.add_host(host)


