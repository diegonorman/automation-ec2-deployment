import argparse
import boto3
import os

# Configurações gerais
REGION = 'us-east-1'
TAG_FILTERS = [
    {'Name': 'tag:Environment', 'Values': ['production']},
    {'Name': 'tag:Owner', 'Values': ['Norman']},
    {'Name': 'tag:Team', 'Values': ['DevOps']}
]

# Configurar argumentos de linha de comando
parser = argparse.ArgumentParser(description='Iniciar instâncias EC2.')
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

instances = ec2.describe_instances(Filters=TAG_FILTERS)
instance_ids = [
    instance['InstanceId']
    for reservation in instances['Reservations']
    for instance in reservation['Instances']
    if instance['State']['Name'] in ['stopped', 'stopping']
]

if not instance_ids:
    print("Nenhuma instância nos estados 'stopped' ou 'stopping' encontrada com as tags especificadas.")
    exit(0)

try:
    response = ec2.start_instances(InstanceIds=instance_ids)
    print(f"Instâncias iniciadas: {instance_ids}")
    print("Instância iniciada com sucesso.")
    exit(0)  # Sucesso
except Exception as e:
    print(f"Erro ao iniciar instâncias: {e}")
    exit(1)  # Interrompe o processo se ocorrer um erro
