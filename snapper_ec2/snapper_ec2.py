import boto3
import click

session = boto3.Session(profile_name='testuser', region_name='us-east-1')
ec2 = session.resource('ec2')

@click.command()
def list_instances():
    all_instances_str = ''
    for i in ec2.instances.all():
        i_str = ', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
        ))
        all_instances_str += i_str.strip() + '\n'

    print(all_instances_str)
    return all_instances_str

if __name__ == '__main__':
    list_instances()
