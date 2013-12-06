# eTorta ![eTorta](http://etorta.herokuapp.com/static/core/img/logo.png)
Aplicação que permite a comparação de preços de produtos em diferentes lojas

## Instalação

Tanto no servidor local quanto no servidor de produção é necessário definir uma variável de ambiente com o valor da chave secreta: `SECRET_KEY="sua chave aqui"`

### Local
- Crie um ambiente com o virtualenv
- Após clonar o repositório, instale todas as dependências: `pip install -r requirements/local.txt`
- Inicialize as variáveis de ambiente para o módulo settings padrão `DJANGO_SETTINGS_MODULE=etorta.settings.local`
- Crie os bancos de dados com os comandos `python etorta/manage.py syncdb` e `python etorta/manage.py core`

### Produção
Para instalar as dependências no servidor remoto, basta executar o comando `pip install -r requirements.txt`.
É importante definir a o módulo de settings para produção `DJANGO_SETTINGS_MODULE=etorta.settings.production`

## Testes
Rode o comando `python etorta/manage.py test --settings=etorta.settings.test`
