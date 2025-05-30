import argparse
import boto3
import os
import requests

INSTANCE_IDS = ['i-06a4184ec28822e99']
REGION = 'us-east-1'
WEBHOOK_URL = 'https://n8n.archcloud.com.br/webhook-test/1f102a99-fb05-4668-a350-dc67ed93ee46/webhook'

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

try:
    response = ec2.start_instances(InstanceIds=INSTANCE_IDS)
    print(f"Instâncias iniciadas: {INSTANCE_IDS}")
    
    # Adicionar log para depuração antes de enviar o webhook
    print(f"Enviando webhook para {WEBHOOK_URL} com payload: {{'status': 'success', 'message': f'Instâncias iniciadas: {INSTANCE_IDS}'}}")
    requests.post(WEBHOOK_URL, json={"status": "success", "message": f"Instâncias iniciadas: {INSTANCE_IDS}"})
    exit(0)  # Sucesso
except Exception as e:
    print(f"Erro ao iniciar instâncias: {e}")
    requests.post(WEBHOOK_URL, json={"status": "failure", "message": str(e)})
    exit(1)  # Falha
