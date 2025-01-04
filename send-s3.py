import sys
import os
import json
import requests
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.config import Config
import redis

def enviar_arquivo_ovh(arquivo, bucket_name, endpoint_url, access_key, secret_key):
    https_proxy = os.getenv("HTTPS_PROXY")
    redis_name = os.getenv("REDIS_NAME")

    config = Config(
        proxies={
            'http': https_proxy,
            'https': https_proxy
        } if https_proxy else {}
    )

    s3 = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='',
        config=config
    )

    chave_arquivo = f"{redis_name}/{arquivo}"

    try:
        s3.upload_file(arquivo, bucket_name, chave_arquivo)
        print(f"Arquivo '{arquivo}' enviado para o cloud no bucket '{bucket_name}' na pasta '{redis_name}'.")
        return True
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return False
    except NoCredentialsError:
        print("Credenciais inválidas para acessar o cloud.")
        return False
    except Exception as e:
        print(f"Erro ao enviar arquivo para o cloud: {e}")
        return False

def enviar_notificacao_falha(mensagem):
    url = os.getenv("WEBHOOK_URL")
    data = {
        "text": mensagem
    }
    response = requests.post(url, headers={"Content-Type": "application/json; charset=UTF-8"}, json=data)
    
    if response.status_code == 200:
        print("Mensagem de falha enviada com sucesso!")
    else:
        print("Erro ao enviar mensagem para o webhook:", response.status_code, response.text)

def verificar_conexao_redis():
    host = os.getenv("REDIS_HOST")
    port = os.getenv("REDIS_PORT", 6379)

    if not host:
        print("A variável de ambiente REDIS_HOST não está definida.")
        return False

    try:
        r = redis.Redis(host=host, port=int(port), socket_connect_timeout=5)
        r.ping()
        print("Conexão com o Redis estabelecida com sucesso.")
        return True
    except redis.ConnectionError as e:
        print(f"Falha ao conectar ao Redis: {e}")
        return False
    except redis.TimeoutError:
        print("Conexão com o Redis expirou.")
        return False
    except Exception as e:
        print(f"Erro inesperado ao conectar ao Redis: {e}")
        return False

def manter_apenas_dois_ultimos_backups(s3, bucket_name, prefixo=''):
    try:
        arquivos = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefixo)
        
        if 'Contents' not in arquivos:
            print(f"Nenhum arquivo encontrado na subpasta '{prefixo}'.")
            return

        arquivos_ordenados = sorted(arquivos['Contents'], key=lambda x: x['LastModified'])

        for arquivo in arquivos_ordenados[:-2]:
            s3.delete_object(Bucket=bucket_name, Key=arquivo['Key'])
            print(f"Arquivo antigo '{arquivo['Key']}' deletado da subpasta '{prefixo}'.")
    except Exception as e:
        print(f"Erro ao tentar limpar backups antigos na subpasta '{prefixo}': {e}")

def main():
    if len(sys.argv) < 2:
        print("Caminho do arquivo não fornecido.")
        sys.exit(1)
    
    arquivo = sys.argv[1]
    bucket_name = os.getenv("BUCKET_NAME")
    endpoint_url = os.getenv("ENDPOINT_URL")
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")

    if not all([bucket_name, endpoint_url, access_key, secret_key]):
        print("Uma ou mais variáveis de ambiente necessárias não estão definidas.")
        sys.exit(1)

    if not verificar_conexao_redis():
        mensagem_falha = "Falha ao conectar ao Redis. Verifique as configurações de host e porta."
        enviar_notificacao_falha(mensagem_falha)

    redis_name = os.getenv("REDIS_NAME")
    prefixo = f"{redis_name}/" 

    s3 = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=''
    )

    manter_apenas_dois_ultimos_backups(s3, bucket_name, prefixo=prefixo)


    backup_realizado = enviar_arquivo_ovh(arquivo, bucket_name, endpoint_url, access_key, secret_key)

    if not backup_realizado:
        mensagem_falha = "Falha ao enviar o arquivo para o cloud."
        enviar_notificacao_falha(mensagem_falha)

if __name__ == "__main__":
    main()