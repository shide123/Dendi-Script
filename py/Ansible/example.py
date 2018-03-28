from ansible.plugins.callback import CallbackBase
import json
from collections import namedtuple
import os
import sys
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.playbook.play import Play
from ansible.inventory.group import Group
from ansible.inventory.manager import InventoryManager


exec_result = ""

class ResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result

def exec_ansible(module, args, host):
    Options = namedtuple('Options',
                         ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check',
                          'diff'])
    # initialize needed objects
    loader = DataLoader()
    options = Options(connection='ssh', module_path='/usr/share/ansible', forks=100,
                      become=None, become_method=None, become_user=None, check=False, diff=False)
    passwords = dict(vault_pass='secret')

    # Instantiate our ResultCallback for handling results as they come in
    results_callback = ResultsCollector()

    # create inventory and pass to var manager
    inventory = InventoryManager(loader=loader, sources=['/etc/ansible/hosts'])
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # create play with tasks
    play_source = dict(
        name="Ansible Play",
        hosts=host,
        gather_facts='no',
        tasks=[
            dict(action=dict(module=module, args=args), register='shell_out'),
        ]
    )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    # actually run it
    tqm = None
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords,
            stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
        )
        result = tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()

if __name__ == '__main__':
    exec_ansible(module='shell', args='date', host='test')
