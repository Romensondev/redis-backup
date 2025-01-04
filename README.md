# Redis Backup

Este projeto tem como objetivo realizar backups automáticos de um banco de dados Redis e enviar os arquivos gerados para um bucket na nuvem. Ele utiliza a biblioteca `boto3` para integração com o armazenamento S3 e conta com um script Python otimizado para gerenciar backups e organizar arquivos antigos.

## Funcionalidades

- **Backup Automático**: Exporta os dados do Redis para um arquivo `.rdb`.
- **Envio Seguro**: Os backups são enviados para um bucket configurado no serviço S3.
- **Organização por Subpastas**: Os backups são organizados em subpastas com base no nome do Redis configurado.
- **Limpeza de Backups Antigos**: Somente os objetos dentro da subpasta correspondente são removidos durante a limpeza.

## Como Configurar

1. Configure as seguintes variáveis de ambiente para integração com o serviço S3:
   ```bash
   export ENDPOINT_URL="<URL do serviço S3>"
   export ACCESS_KEY="<Sua chave de acesso ao S3>"
   export SECRET_KEY="<Sua chave secreta para autenticação no S3>"
   export BUCKET_NAME="<Nome do bucket>"
   export REDIS_HOST="<Endereço do servidor Redis>"
   export REDIS_PORT=<Porta do Redis>
   export REDIS_NAME="<Nome do Redis para organização dos backups>"
   ```

2. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o script para realizar um backup:
   ```bash
   python send-s3.py
   ```

## Observações de Segurança

- Certifique-se de que as chaves de acesso e outras informações sensíveis sejam protegidas e nunca expostas em arquivos de configuração públicos.
- Utilize um serviço de monitoramento de credenciais, como o GitGuardian, para evitar vazamentos acidentais.

---

Sinta-se à vontade para contribuir com melhorias ou reportar problemas encontrados no projeto!
