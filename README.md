# Projeto de Gerenciamento de Instâncias EC2

Este projeto contém scripts Python para gerenciar instâncias EC2 na AWS. Ele inclui funcionalidades para configurar, iniciar e parar instâncias EC2 com base em tags específicas.

## Estrutura do Projeto

- **`setup_ec2.py`**: Cria instâncias EC2 com tags predefinidas e configurações iniciais.
- **`start_ec2.py`**: Inicia instâncias EC2 que estão nos estados `stopped` ou `stopping` e possuem as tags especificadas.
- **`stop_ec2.py`**: Para instâncias EC2 que estão no estado `running` e possuem as tags especificadas.

## Pré-requisitos

1. **Python**: Certifique-se de ter o Python 3.7 ou superior instalado.
2. **Bibliotecas**: Instale as dependências listadas no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
3. **Credenciais AWS**: Configure suas credenciais AWS usando variáveis de ambiente ou argumentos de linha de comando.

## Configurações Gerais

Os scripts utilizam as seguintes configurações padrão:
- **Região AWS**: `us-east-1`
- **Tags**:
  - `Environment=production`
  - `Owner=Norman`
  - `Team=DevOps`

## Scripts

### 1. `setup_ec2.py`

Este script cria uma instância EC2 com as seguintes configurações:
- **Tipo de instância**: `t4g.micro`
- **Tamanho do EBS**: 8 GB
- **Perfil IAM**: `ROLE-SSM`
- **Script de inicialização**: Instala Apache e Docker, e configura uma página HTML inicial.

#### Uso:
```bash
python setup_ec2.py --aws-access-key-id <ACCESS_KEY> --aws-secret-access-key <SECRET_KEY> --aws-session-token <SESSION_TOKEN>
```

### 2. `start_ec2.py`

Este script inicia instâncias EC2 que estão nos estados `stopped` ou `stopping` e possuem as tags especificadas.

#### Uso:
```bash
python start_ec2.py --aws-access-key-id <ACCESS_KEY> --aws-secret-access-key <SECRET_KEY> --aws-session-token <SESSION_TOKEN>
```

### 3. `stop_ec2.py`

Este script para instâncias EC2 que estão no estado `running` e possuem as tags especificadas.

#### Uso:
```bash
python stop_ec2.py --aws-access-key-id <ACCESS_KEY> --aws-secret-access-key <SECRET_KEY> --aws-session-token <SESSION_TOKEN>
```

## Observações

- Certifique-se de que as tags das instâncias EC2 correspondam às especificadas nos scripts.
- Verifique se você possui permissões adequadas na AWS para executar as operações descritas.

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou correções. Faça um fork do repositório, crie uma branch para suas alterações e envie um pull request.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.
