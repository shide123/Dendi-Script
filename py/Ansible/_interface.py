# -*- coding:utf-8 -*-
import json

import time
from pykickstart.commands import logging

from ansible_api import AnsibleAPI


class AnsiInterface(AnsibleAPI):
    def __init__(self, resource, *args, **kwargs):
        super(AnsiInterface, self).__init__(resource, *args, **kwargs)

    @staticmethod
    def deal_result(info, options):
        if options == 'setup':
            hostip = info.get('success').keys()
            for ip in hostip:
                ansible_facts = info['success'][ip]['ansible_facts']
                info['success']['ip'] = ip
                info['success'].pop(ip)
                info['success'].update({'ansible_facts': ansible_facts})
        elif options == 'command':
            hostip = info.get('success').keys()
            for ip in hostip:
                stdout = info['success'][ip]['stdout']
                info['success']['ip'] = ip
                info['success'].update({'stdout': stdout})
                info['success'].pop(ip)
        info_json = json.dumps(info)
        return info_json

    def copy_file(self, host_list, src=None, dest=None):
        """
        copy file
        """
        module_args = "src=%s  dest=%s" % (src, dest)
        self.run(host_list, 'copy', module_args)
        result = self.get_result()
        return self.deal_result(result)

    def exec_command(self, host_list, cmds):
        """
        commands
        """
        self.run(host_list, 'command', cmds)
        result = self.get_result()
        return self.deal_result(result, 'command')

    def exec_script(self, host_list, path):
        """
        在远程主机执行shell命令或者.sh脚本
        """
        self.run(host_list, 'shell', path)
        result = self.get_result()
        return self.deal_result(result)

    def exec_setup(self, host_list):
        """
        在远程主机执行shell命令或者.sh脚本
        """
        self.run(host_list, 'setup', '')
        result = self.get_result()
        return self.deal_result(result, 'setup')


if __name__ == "__main__":
    resource = [{"hostname": "172.16.251.114", "port": "1221", "username": "lishide", "password": "lishide",
                 "ip": '172.16.251.114'}
                ]
    # resource = [{"hostname": "123.103.666.66", "port": "1221", "username": "lishide", "password": "lishide",
    #              "ip": '123.103.666.66'}
    #             ]
    interface = AnsiInterface(resource)

    interface.getHostInfo()
    # print "copy: ", interface.copy_file(['172.20.3.18', '172.20.3.31'], src='/Users/majing/test1.py', dest='/opt')
    # print "commands: ", interface.exec_command(['172.16.251.116'], 'id lishide')
    print "setup: ", interface.exec_setup(['172.16.251.114'])
