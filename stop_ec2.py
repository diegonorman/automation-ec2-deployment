import argparse
import boto3
import os

INSTANCE_IDS = ['i-06a4184ec28822e99']
REGION = 'us-east-1'

# Configurar argumentos de linha de comando
parser = argparse.ArgumentParser(description='Parar instâncias EC2.')
parser.add_argument('--aws-access-key-id', help='AWS Access Key ID')
parser.add_argument('--aws-secret-access-key', help='AWS Secret Access Key')
parser.add_argument('--aws-session-token', help='AWS Session Token')
args = parser.parse_args()

# Configurar cliente boto3 com credenciais temporárias
aws_access_key_id = args.aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = args.aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token = args.aws_session_token or os.getenv('AWS_SESSION_TOKEN')

# Verificar se todas as credenciais estão disponíveis
if not aws_access_key_id:
    raise ValueError("AWS_ACCESS_KEY_ID não encontrado. Certifique-se de que as credenciais estão configuradas corretamente.")
if not aws_secret_access_key:
    raise ValueError("AWS_SECRET_ACCESS_KEY não encontrado. Certifique-se de que as credenciais estão configuradas corretamente.")
if not aws_session_token:
    raise ValueError("AWS_SESSION_TOKEN não encontrado. Certifique-se de que as credenciais estão configuradas corretamente.")

# Configurar cliente boto3
ec2 = boto3.client(
    'ec2',
    region_name=REGION,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

response = ec2.stop_instances(InstanceIds=INSTANCE_IDS)
print(f"Instâncias paradas: {INSTANCE_IDS}")
