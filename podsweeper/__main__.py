# inspired by https://stackoverflow.com/questions/64221992/simple-way-to-delete-existing-pods-from-python/64222735#64222735

import click
from kubernetes import client, config

@click.command()
@click.option('--namespace', required=True)
def main(namespace):
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    pods = v1.list_namespaced_pod(namespace=namespace, watch=False)
    for p in pods.items:
        print("%s\t%s\t%s" % (p.status.pod_ip, p.metadata.namespace, p.metadata.name))

main()
