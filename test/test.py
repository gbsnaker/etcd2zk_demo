# /usr/bin/env python
#-*- coding: utf-8 -*-


import base64
from json import dumps
import importlib
import json

import etcd3
import k8sclient
import os
import sys

importlib.reload(sys)
import re
from kubernetes import client, config
# config.load_kube_config()

etcd = etcd3.client(
    host='192.168.0.173',
    ca_cert='../ca.pem',
    cert_cert='../kubernetes.pem',
    cert_key='../kubernetes-key.pem',
    port=2379)

print("你好")
"""
class KVMetadata(object):
    def __init__(self, keyvalue, header):
        self.key = keyvalue.key
        self.create_revision = keyvalue.create_revision
        self.mod_revision = keyvalue.mod_revision
        self.version = keyvalue.version
        self.lease_id = keyvalue.lease
        self.response_header = header
"""

items = etcd.get_prefix('/registry/pods/default/zk')
ipmatch = re.compile('172.20.')
# sepmatch = re.compile(b"\n|\t|\r|\x00")
sepmatch = re.compile(b"\n|\t")
for item in items:
    # print(type(item))
    # print(item[1].__dict__)
    # print(item[0].replace(b"\n|\t",b""))
    #print(item[0].decode('latin-1'))
    #tmpstrutf8 = item[0].decode('iso-8859-1').encode('utf-8')
    tmpstrutf8 = item[0].decode('latin-1')
    print(tmpstrutf8)

    #aa = item[0].split()
    # aa = sepmatch.split(item[0])
    # aa = item[0].replace(b"\n",b" ").replace(b"\t",b" ")
    # print(aa)
    # for i in aa:
    #     # print("org %s" %i)
    #     if i:
    #         # print(i)
    #         ipline = i.decode('latin-1')
    #         # try:
    #         #     ipline = i.decode('latin-1')
    #         # except Exception as e:
    #         #     pass
    #         #     # print(e)
    #         # else:
    #         #     ipline = i.decode('latin-1')
    #
    #         print(ipline)
            #     if ipmatch.match(ipline):
            #         #print(type(ipline))
            #         print(ipline)
            #         #line=ipline.strip().replace('B','').strip()
            #         #print(line)


            # jsonified = json.dumps(item, cls=etcd3.client.KVMetadata)
            # print(jsonified)

            # for i in item:
            #     #print(type(i))
            #     print(i)
            #     print(i.split())
            #     aa = i.split()
            #     jsn = ''.join(x.decode('utf-8') for x in aa)
            #     print(jsn)
            # d = json.loads(jsn)
            #     # if isinstance(i,bytes):
            #     #     print(i.decode('utf-8'))
            #
            #     #print(i)
            #     if isinstance(i, etcd3.client.KVMetadata):
            #         print(type(i))

# /registry/pods/default/zk
watch_count = 0
events_iterator, cancel = etcd.watch_prefix("/registry/pods/default")
for event in events_iterator:
    # if isinstance(event, etcd3.events.PutEvent):
    #     print("put event")
    nginxre = re.compile('nginx')
    if isinstance(event, etcd3.events.DeleteEvent):
        key = event.__dict__.get('key').decode("utf-8")
        print(key)
        namespace = key.split('/')[3]
        servicename = key.split('/')[4]
        if nginxre.search(servicename):
            print("start")
            print(servicename)
            print(namespace)
