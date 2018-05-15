# /usr/bin/env python
#-*- coding: utf-8 -*-
import re
import logging
import uuid
import time


from etcd3 import Etcd3Client, Lock
from kazoo.client import KazooClient
from kubernetes import client, config, watch
config.load_kube_config()

my_id = uuid.uuid4()
def work():
    print("I get the lock {}".format(str(my_id)))

etc3client = Etcd3Client(
    host='192.168.0.172',
    ca_cert='../ca.pem',
    cert_cert='../kubernetes.pem',
    cert_key='../kubernetes-key.pem',
    port=2379
    )

v1 = client.CoreV1Api()
logging.basicConfig()

#获得zk地址，建立地址映射
ret = v1.list_pod_for_all_namespaces(watch=False)
zk_namespaceh_dict = {}
zkpodname = re.compile('zk.*')
for i in ret.items:
    if not zk_namespaceh_dict.get(i.metadata.namespace):
         zk_namespaceh_dict[i.metadata.namespace] = []
    if zkpodname.match(i.metadata.name):
        tmp = "%s:2181" %(i.status.pod_ip)
        zk_namespaceh_dict[i.metadata.namespace].append(tmp)

nginxpodname = re.compile('nginx.*')
def Delete_Servce_from_zk():
    w = watch.Watch()
    #count =100
    for event in w.stream(v1.list_pod_for_all_namespaces, _request_timeout=500):
        print(event['type'])
        if event['type'] == 'ADDED' and nginxpodname.match(event['object'].metadata.name):
            print(event['object'].metadata.namespace)
            print(event['object'].metadata.name)
            print(event['object'].status.pod_ip)
            zk = KazooClient(hosts="192.168.0.176:2181")
            zk.start()
            zkpath = "/rkhd/server/nginx/hosts/%s" % event['object'].metadata.name
            if not zk.exists(zkpath):
                if event['object'].status.pod_ip:
                    value_string = event['object'].status.pod_ip
                    byes_sring = value_string.encode('utf-8')
                zk.create(zkpath, byes_sring)
            zk.stop()

        if event['type'] == 'DELETED' and nginxpodname.match(event['object'].metadata.name):
            # if event['object']['kind'] == "Pod":  ADDED MODIFIED
            print(event['type'])
            print(event['object'].metadata.namespace)
            #connection zk
            hosts = zk_namespaceh_dict[event['object'].metadata.namespace]
            hosts = ','.join(hosts)
            print(hosts)
            #zk = KazooClient(hosts=hosts)
            zk = KazooClient(hosts="192.168.0.176:2181")
            zk.start()
            zk.ensure_path("/rkhd/server/nginx/hosts")
            #zk.create("/rkhd/server/nginx/hosts", b"-")
            children = zk.get_children("/rkhd/server/nginx/hosts")
            print(children)
            for child in children:
                if child:
                    zk.delete("/rkhd/server/nginx/hosts/%s"%child)
            #zk.delete("/rkhd/server/nginx/hosts", recursive=True)
            #zk.create("/rkhd/server", b"a value")

            zk.stop()

lock = Lock(etcd_client=etc3client, name='/customerlock', ttl=60)
with lock as my_lock:
    Delete_Servce_from_zk()
    lock.is_locked()  # True
    lock.renew(60)
lock.is_locked()  # False