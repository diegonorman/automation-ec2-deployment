import argparse
import boto3

INSTANCE_IDS = ['i-1234567890abcdef0']
REGION = 'us-east-1'

# Configurar argumentos de linha de comando
parser = argparse.ArgumentParser(description='Iniciar instâncias EC2.')
parser.add_argument('--aws-access-key-id', required=True, help='AWS Access Key ID')
parser.add_argument('--aws-secret-access-key', required=True, help='AWS Secret Access Key')
parser.add_argument('--aws-session-token', required=True, help='AWS Session Token')
args = parser.parse_args()

# Configurar cliente boto3 com credenciais temporárias
ec2 = boto3.client(
    'ec2',
    region_name=REGION,
    aws_access_key_id=args.aws_access_key_id,
    aws_secret_access_key=args.aws_secret_access_key,
    aws_session_token=args.aws_session_token
)

response = ec2.start_instances(InstanceIds=INSTANCE_IDS)
print(f"Instâncias iniciadas: {INSTANCE_IDS}")
