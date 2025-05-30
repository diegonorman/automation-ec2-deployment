import boto3
import os

INSTANCE_IDS = ['i-06a4184ec28822e99']
REGION = 'us-east-1'

# Configurar cliente boto3 com credenciais temporárias diretamente do ambiente
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token = os.getenv('AWS_SESSION_TOKEN')

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

try:
    response = ec2.stop_instances(InstanceIds=INSTANCE_IDS)
    print(f"Instâncias paradas: {INSTANCE_IDS}")
    exit(0)  # Sucesso
except Exception as e:
    print(f"Erro ao parar instâncias: {e}")
    exit(1)  # Falha
