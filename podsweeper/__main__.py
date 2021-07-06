from datetime import datetime, timezone

import click
from kubernetes import client, config

@click.command()
@click.option('--namespace', required=True, type=str)
@click.option('--field-selector', type=str)
@click.option('--label-selector', type=str)
@click.option('--pod-name-prefix', type=str, help='only select pods whose name starts with this prefix')
@click.option('--expire-in-hours', type=int, help='only select pods that are aged more than this many hours')
def main(namespace, field_selector, label_selector, pod_name_prefix, expire_in_hours):
    config.load_incluster_config()

    kwargs = {'field_selector': field_selector, 'label_selector': label_selector}
    kwargs = {key: value for key, value in kwargs.items() if value is not None}

    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace=namespace, watch=False, **kwargs)

    def age_in_hours(pod):
        """
        For how many hours has this pod been stuck in the last condition?
        Return `None` if unknown.
        """
        try:
            transition_times = sorted([cond.last_transition_time for cond in pod.status.conditions])
            age = datetime.now(timezone.utc) - transition_times[-1]
            return (age.total_seconds() / 60) / 60

        except:
            return None

    def predicate(pod):
        """Decide if we want to delete a pod."""
        try:
            name = pod.metadata.name

            if pod_name_prefix is not None and not name.startswith(pod_name_prefix):
                return False

            if expire_in_hours is None:
                return True

            age = age_in_hours(pod)

            if age is None:
                return False

            return (age > expire_in_hours)

        except:
            # if any of the above assumptions are not quite right, do not delete the pod
            return False

    def show(pod):
        """Human-readable pod info."""
        return '{:} {} {} {:d}h'.format(pod.metadata.namespace,
                                        pod.metadata.name,
                                        pod.status.phase,
                                        int(age_in_hours(pod)))

    for pod in pods.items:
        if predicate(pod):
            print(show(pod))

main()
