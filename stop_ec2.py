import boto3
import os

# Configurações gerais
REGION = 'us-east-1'
TAG_FILTERS = [
    {'Name': 'tag:Environment', 'Values': ['production']},
    {'Name': 'tag:Owner', 'Values': ['Norman']},
    {'Name': 'tag:Team', 'Values': ['DevOps']}
]

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

# Buscar instâncias com as tags especificadas
instances = ec2.describe_instances(Filters=TAG_FILTERS)
instance_ids = [
    instance['InstanceId']
    for reservation in instances['Reservations']
    for instance in reservation['Instances']
]

if not instance_ids:
    print("Nenhuma instância encontrada com as tags especificadas.")
    exit(0)

try:
    ec2.stop_instances(InstanceIds=instance_ids)
    print(f"Instâncias paradas: {instance_ids}")
    print("Instância parada com sucesso.")
    exit(0)  # Sucesso
except Exception as e:
    print(f"Erro ao parar instâncias: {e}")
    exit(1)  # Falha
