#!/usr/bin/env python

from templatedict import TemplateDict

td = TemplateDict()
td['server_name'] = 's1 ${arch} $arch'
td['instance'] = "${server_name}_instance"
td['arch'] = "64"
print td.substitute() # {'instance': 's1 64 64_instance', 'arch': '64', 'server_name': 's1 64 64'}
