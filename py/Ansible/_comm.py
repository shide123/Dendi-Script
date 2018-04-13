# -*- coding:utf-8 -*-

# myRunner
from collections import namedtuple

import shutil

import sys
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from gtk.keysyms import C


class My_Runner(object):
    def __init__(self, resource):
        self.resource = resource
        self.options = None
        self.loader = None
        self.passwords = None
        self.results_callback = None
        self.inventory = None
        self.variable_manager = None
        self.__initializeData()
        self.result_raw = {}

    def __initializeData(self):
        Options = namedtuple('Options',
                             ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check',
                              'diff'])
        self.loader = DataLoader()
        self.options = Options(connection='local', module_path=['/usr/lib/python2.7/site-packages/ansible/modules/commands'], forks=100, become=None,
                               become_method=None,
                               become_user=None, check=False,
                               diff=False)
        self.passwords = dict(vault_pass='secret')
        self.inventory = InventoryManager(loader=self.loader, sources=self.resource)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.callback = None

    def run(self, host_list, module, module_args):
        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=[
                dict(action=dict(module=module, args=module_args), register='shell_out'),
            ]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        self.callback = ResultCallback()
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=self.callback,
                # Use our custom callback instead of the ``default`` callback plugin
            )
            result = tqm.run(play)

        finally:
            if tqm is not None:
                tqm.cleanup()
                # Remove ansible tmpdir
             #shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def get_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            self.results_raw['success'][host] = result._result

        for host, result in self.callback.host_failed.items():
            self.results_raw['failed'][host] = result._result

        for host, result in self.callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result['msg']

            # print "Ansible执行结果集:%s"%self.results_raw
        return self.results_raw


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.host_failed[result._host.get_name()] = result

    def v2_runner_on_ok(self, result):
        # host = result._host.get_name()
        # self.runner_on_ok(host, result._result)
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_unreachable(self, result):
        # host = result._host.get_name()
        # self.runner_on_unreachable(host, result._result)
        self.host_unreachable[result._host.get_name()] = result


if __name__ == '__main__':
    host_list = sys.argv[1]
    module = sys.argv[2]
    module_args = sys.argv[3]
    ansible = My_Runner('/etc/ansible/hosts')
    # 获取服务器磁盘信息
    ansible.run(host_list=host_list, module=module, module_args=module_args)
    # 结果
    result = ansible.get_result()
    # 成功
    succ = result['success']
    # 失败
    failed = result['failed']
    # 不可到达
    unreachable = result['unreachable']
    print result
    
