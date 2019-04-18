## Configuring

`aws configure --project testuser`

## Running

`pipenv run "python snapper_ec2/snapper_ec2.py <command> <subcommand> <--project=PROJECT>""`

*command* instances, volumes, snapshots
*subcommand* is list, start, reboot, or stop
*project* is optional
