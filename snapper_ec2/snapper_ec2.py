import boto3
import botocore
import click

session = boto3.Session(profile_name='testuser', region_name='us-east-1')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances  = ec2.instances.all()

    return instances

@click.group()
def cli():
    """snapper_ec2 manages snapshots"""

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None, help="Only snapshots for project (tag Project:<name>)")
def list_snapshots( project ):
    "List snapshots"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                   s.id,
                   v.id,
                   i.id,
                   s.state,
                   s.progress,
                   s.start_time.strftime("%c")
                 )))

    return

@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None, help="Only volumes for project (tag Project:<name>)")
def list_volumes( project ):
    "List volumes"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
               v.id,
               i.id,
               v.state,
               str(v.size) + "GiB",
               v.encrypted and "Encrypted" or "Not Encrypted"
             )))

    return

@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def list_instances( project ):
    "List EC2s"

    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        line =(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>'))))
        print(line)

    return

@instances.command('stop')
@click.option('--project', default=None, help='Only instances for project')
def stop_instances(project):
    "Stop EC2s"

    instances = filter_instances(project)

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances  = ec2.instances.all()

    for i in instances:
        print("Stopping {0}...".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print(" Could not stop {0}.".format(i.id) + str(e))
            continue

    return

@instances.command('start')
@click.option('--project', default=None, help='Only instances for project')
def stop_instances(project):
    "Start EC2s"

    instances = filter_instances(project)

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances  = ec2.instances.all()

    for i in instances:
        print("Starting {0}...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print(" Could not start {0}.".format(i.id) + str(e))
            continue

    return

@instances.command('snapshot', help="Create snapshots of all volumes")
@click.option('--project', default=None, help='Only snapshots for project')
def create_snapshots(project):
    "Create snapshots for EC2 instances"

    instances = filter_instances(project)

    for i in instances:

        print("Stopping {0}... ".format(i.id))
        try:
            i.stop()
        except bitocore.exceptions.ClientError as e:
            print(" Could not stop {0}. ".format(i.id) + str(e))
            continue
        i.wait_until_stopped()
        for v in i.volumes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by snapper_ec2")

        print("Starting {0}... ".format(i.id))

        i.start()
        i.wait_until_running()
    print("Completed task")
    return

if __name__ == '__main__':
    #print(list_instances())
    cli()
