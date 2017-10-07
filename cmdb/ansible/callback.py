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
@File: callback.py
@Time: 9/9/17 11:52 PM
"""
from ansible.plugins.callback import CallbackBase
import time


# class CommandResultCallback(CallbackBase):
#     """
#     command result callback
#     """
#     def __init__(self, display=None):
#         self.result_query = dict(contacted={}, dark={})
#         super(CommandResultCallback, self).__init__(display)
#
#     def gather_result(self, typ, res):
#         now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
#         obj = res.task_name + now
#         print(obj)
#         self.result_query[typ][res._host.name] = {obj: {}}
#         self.result_query[typ][res._host.name][obj]["cmd"] = res._result.get("cmd")
#         self.result_query[typ][res._host.name][obj]["stderr"] = res._result.get("stderr")
#         self.result_query[typ][res._host.name][obj]["stdout"] = res._result.get("stdout")
#         self.result_query[typ][res._host.name][obj]["rc"] = res._result.get("rc")
#         self.result_query[typ][res._host.name][obj]["result"] = res._result
#         print(self.result_query)
#         # self.result_query[typ][res._host.name] = {}
#         # self.result_query[typ][res._host.name]["cmd"] = res._result.get("cmd")
#         # self.result_query[typ][res._host.name]["stderr"] = res._result.get("stderr")
#         # self.result_query[typ][res._host.name]["stdout"] = res._result.get("stdout")
#         # self.result_query[typ][res._host.name]["rc"] = res._result.get("rc")
#         # self.result_query[typ][res._host.name]["result"] = res._result
#
#     def v2_runner_on_ok(self, result):
#         self.gather_result("contacted", result)
#
#     def v2_runner_on_failed(self, result, ignore_errors=False):
#         self.gather_result("dark", result)
#
#     def v2_runner_on_unreachable(self, result):
#         self.gather_result("dark", result)
#
#     def v2_runner_on_skipped(self, result):
#         self.gather_result("dark", result)
#

class AdHocResultCallback(CallbackBase):
    """
    AdHoc result callback
    """
    def __init__(self, display=None):
        self.result_query = dict(contacted={}, dark={})
        super(AdHocResultCallback, self).__init__(display)

    def gather_result(self, typ, res):

        now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        obj = res.task_name + "_" + str(res._result.get("cmd")) + "_" + now
        # print(obj)
        if res._host.name not in self.result_query[typ].keys():
            self.result_query[typ][res._host.name] = {}
        self.result_query[typ][res._host.name][obj] = {}
        # self.result_query[typ][res._host.name][obj]["cmd"] = res._result.get("cmd")
        # self.result_query[typ][res._host.name][obj]["stderr"] = res._result.get("stderr")
        # self.result_query[typ][res._host.name][obj]["stdout"] = res._result.get("stdout")
        # self.result_query[typ][res._host.name][obj]["rc"] = res._result.get("rc")
        self.result_query[typ][res._host.name][obj]["result"] = res._result
        # print(self.result_query)

    def v2_runner_on_ok(self, result):
        self.gather_result("contacted", result)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.gather_result("dark", result)

    def v2_runner_on_unreachable(self, result):
        self.gather_result("dark", result)

    def v2_runner_on_skipped(self, result):
        self.gather_result("dark", result)

    def v2_playbook_on_task_start(self, task, is_conditional):
        pass

    def v2_playbook_on_play_start(self, play):
        pass


class PlayBookResultCallback(CallbackBase):
    """
    playbook result callback
    """
    CALLBACK_VERSION = 2.2
    CALLBACK_TYPE = "stdout"
    CALLBACK_NAME = "Dict"

    def __init__(self, display=None):
        super(PlayBookResultCallback, self).__init__(display)
        self.results = []
        self.output = ""
        self.item_results = {}

    def _new_play(self, play):
        return {
            "play": {
                "name": play.name,
                "id": str(play._uuid)
            },
            "tasks": []
        }

    def _new_task(self, task):
        return {
            "task": {
                "name": task.get_name(),
            },
            "hosts": {}
        }

    def v2_playbook_on_no_hosts_matched(self):
        self.output = "skipping: No match hosts."

    def v2_playbook_on_no_hosts_remaining(self):
        pass

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.results[-1]["tasks"].append(self._new_task(task))

    def v2_playbook_on_play_start(self, play):
        self.results.append(self._new_play(play))

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        summary = {}
        for host in hosts:
            s = stats.summarize(host)
            summary[host] = s

        if self.output:
            pass
        else:
            self.output = {
                "plays": self.results,
                "stats": summary
            }

    def gather_result(self, res):
        if res._task.loop and "results" in res._result and res._host.name in self.item_results:
            res._result.update({"results": self.item_results[res._host.name]})
            del self.item_results[res._host.name]

        self.results[-1]["tasks"][-1]["hosts"][res._host.name] = res._result

    def v2_runner_on_ok(self, result):
        if "ansible_facts" in result._result:
            del result._result["ansible_facts"]
        self.gather_result(result)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.gather_result(result)

    def v2_runner_on_unreachable(self, result):
        self.gather_result(result)

    def v2_runner_on_skipped(self, result):
        self.gather_result(result)

    def gather_item_result(self, result):
        self.item_results.setdefault(result._host.name, []).append(result._result)

    def v2_runner_item_on_ok(self, result):
        self.gather_item_result(result)

    def v2_runner_item_on_failed(self, result):
        self.gather_item_result(result)

    def v2_runner_item_on_skipped(self, result):
        self.gather_item_result(result)

