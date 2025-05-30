import boto3
import os
import requests

INSTANCE_IDS = ['i-06a4184ec28822e99']
REGION = 'us-east-1'
WEBHOOK_URL = 'https://n8n.archcloud.com.br/webhook-test/1f102a99-fb05-4668-a350-dc67ed93ee46/webhook'

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
    
    # Adicionar log para depuração antes de enviar o webhook
    print(f"Enviando webhook para {WEBHOOK_URL} com payload: {{'status': 'success', 'message': f'Instâncias paradas: {INSTANCE_IDS}'}}")
    requests.post(WEBHOOK_URL, json={"status": "success", "message": f"Instâncias paradas: {INSTANCE_IDS}"})
    exit(0)  # Sucesso
except Exception as e:
    print(f"Erro ao parar instâncias: {e}")
    requests.post(WEBHOOK_URL, json={"status": "failure", "message": str(e)})
    exit(1)  # Falha
