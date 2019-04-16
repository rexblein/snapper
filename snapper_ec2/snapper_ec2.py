import boto3
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
    "List volumes"

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
        i.stop()

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
        i.start()

    return

@instances.command('snapshot', help="Create snapshots of all volumes")
@click.option('--project', default=None, help='Only snapshots for project')
def create_snapshots(project):
    "Create snapshots for EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print("Creating snapshots off {0}".format(v_id))
            v.create_snapshot(Descriptions="Created by snapper_ec2")
            
    return

if __name__ == '__main__':
    #print(list_instances())
    cli()
