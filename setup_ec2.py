import boto3
import os
import argparse

# Configurações gerais
REGION = 'us-east-1'
vpc_id = 'vpc-0c9b255128195b2b3'
security_group_id = 'sg-0e0a217a7398631a5'
ebs_size = 8
instance_type = 't4g.micro'
min_count = 1
max_count = 1
instance_name = 'Git-deplyoment-CI/CD'
instance_tags = [
    {'Key': 'Environment', 'Value': 'production'},
    {'Key': 'Owner', 'Value': 'Norman'},
    {'Key': 'Team', 'Value': 'DevOps'}
]

# Script de inicialização (user-data)
USER_DATA = '''#!/bin/bash
sudo apt update -y
sudo apt install -y apache2 docker.io
sudo systemctl start apache2
sudo systemctl enable apache2
sudo systemctl start docker
sudo systemctl enable docker
echo "<h1>Instância configurada com sucesso!</h1>" > /var/www/html/index.html
'''

# Configurar argumentos de linha de comando
parser = argparse.ArgumentParser(description='Criar uma instância EC2 com preconfiguração.')
parser.add_argument('--aws-access-key-id', help='AWS Access Key ID')
parser.add_argument('--aws-secret-access-key', help='AWS Secret Access Key')
parser.add_argument('--aws-session-token', help='AWS Session Token')
args = parser.parse_args()

# Configurar cliente boto3 com credenciais temporárias
aws_access_key_id = args.aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = args.aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token = args.aws_session_token or os.getenv('AWS_SESSION_TOKEN')

if not all([aws_access_key_id, aws_secret_access_key, aws_session_token]):
    raise ValueError("Credenciais da AWS não fornecidas. Certifique-se de passar via argumentos ou variáveis de ambiente.")

ec2 = boto3.client(
    'ec2',
    region_name=REGION,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

# Buscar dinamicamente o ID da AMI para Ubuntu 22.04 com os critérios especificados
def get_ami_id():
    ec2_client = boto3.client('ec2', region_name=REGION)
    response = ec2_client.describe_images(
        Filters=[
            {'Name': 'name', 'Values': ['ubuntu-minimal/images/hvm-ssd/ubuntu-jammy-22.04-arm64-minimal-20240701']},
            {'Name': 'architecture', 'Values': ['arm64']},
            {'Name': 'owner-alias', 'Values': ['amazon']}
        ]
    )
    if response['Images']:
        return response['Images'][0]['ImageId']
    else:
        raise ValueError("AMI não encontrada com os critérios especificados.")

AMI_ID = get_ami_id()

try:
    # Criar a instância EC2
    instance_params = {
        'ImageId': AMI_ID,
        'InstanceType': instance_type,
        'MinCount': min_count,
        'MaxCount': max_count,
        'BlockDeviceMappings': [
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'VolumeSize': ebs_size,
                    'VolumeType': 'gp3',
                    'DeleteOnTermination': True
                }
            }
        ],
        'UserData': USER_DATA,
        'IamInstanceProfile': {
            'Arn': 'arn:aws:iam::905418073202:instance-profile/ROLE-SSM'
        },
        'TagSpecifications': [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': instance_name},
                    *instance_tags
                ]
            }
        ],
        'NetworkInterfaces': [
            {
                'AssociatePublicIpAddress': True,
                'DeviceIndex': 0,
                'SubnetId': ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['Subnets'][0]['SubnetId'],
                'Groups': [security_group_id]
            }
        ]
    }

    response = ec2.run_instances(**instance_params)
except Exception as e:
    print(f"Erro ao criar a instância EC2: {e}")
    exit(1)  # Interrompe o processo se ocorrer um erro

