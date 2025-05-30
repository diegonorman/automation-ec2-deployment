import boto3
import os
import argparse

# Configurações da instância EC2
REGION = 'us-east-1'

# Script de inicialização (user-data)
USER_DATA = '''#!/bin/bash
sudo apt update -y
sudo apt install -y apache2
sudo systemctl start apache2
sudo systemctl enable apache2
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

# Create a security group named 'web-git' with ports 80 and 443 open to 0.0.0.0/0
def create_security_group():
    try:
        response = ec2.create_security_group(
            GroupName='web-git',
            Description='Security group for web access on ports 80 and 443'
        )
        security_group_id = response['GroupId']

        # Add inbound rules for ports 80 and 443
        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )
        return security_group_id
    except Exception as e:
        print(f"Erro ao criar ou configurar o grupo de segurança: {e}")
        raise

# Create the security group and get its ID
security_group_id = create_security_group()

try:
    # Criar a instância EC2
    instance_params = {
        'ImageId': AMI_ID,
        'InstanceType': 't2.micro',
        'SecurityGroupIds': [security_group_id],
        'MinCount': 1,
        'MaxCount': 1,
        'UserData': USER_DATA,
        'IamInstanceProfile': {
            'Arn': 'arn:aws:iam::905418073202:role/ROLE-SSM'
        },
        'TagSpecifications': [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': 'MyConfiguredInstance'}
                ]
            }
        ],
        'NetworkInterfaces': [
            {
                'AssociatePublicIpAddress': True,
                'DeviceIndex': 0
            }
        ]
    }

    # Remove KeyName to ensure no key pair is used
    response = ec2.run_instances(**instance_params)

    instance_id = response['Instances'][0]['InstanceId']
    print(f"Instância criada com sucesso. ID da instância: {instance_id}")
except Exception as e:
    print(f"Erro ao criar a instância EC2: {e}")
