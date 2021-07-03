# inspired by https://stackoverflow.com/questions/64221992/simple-way-to-delete-existing-pods-from-python/64222735#64222735

import os

import click
from kubernetes import client, config

@click.command()
@click.option('--namespace', required=True)
def main(namespace):
    # getting an error here
    config.load_incluster_config()
    # I think the relevant docs are here, but I am not sure what to do next
    # https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/#accessing-the-api-from-a-pod
    # the file /var/run/secrets/kubernetes.io/serviceaccount/token is not there in the pod

    configuration = client.Configuration()

    with client.ApiClient(configuration) as api_client:
        api_instance = client.CoreV1Api(api_client)

        api_response = api_instance.list_namespaced_pod(namespace=namespace, watch=False)
        for i in api_response.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        # api_response = api_instance.delete_namespaced_pod(name, namespace)

main()
