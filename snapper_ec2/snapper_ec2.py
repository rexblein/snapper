import boto3

if __name__ == '__main__':
    session = boto3.Session(profile_name='testuser', region_name='us-east-1')
    ec2 = session.resource('ec2')

    for i in ec2.instances.all():
        print(i)
