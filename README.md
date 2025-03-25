### **Explicação Detalhada sobre o Código e Projeto**

### **Visão Geral**

O projeto foi desenvolvido para simular um painel de monitoramento de chamadas telefônicas. O painel permite visualizar informações como o total de chamadas, a duração total das chamadas e o tempo total de chamadas, além de permitir o acompanhamento em tempo real da inserção e processamento dessas informações.

### **Arquitetura**

O projeto segue a arquitetura padrão do Django, onde:

- **Modelos**: Contêm a estrutura de dados da aplicação.
- **Views**: Processam as requisições e retornam respostas ao usuário.
- **Templates**: São responsáveis pela apresentação da interface para o usuário.
- **URLs**: Gerenciam as rotas e como as requisições são direcionadas para as views.

### **Principais Componentes do Projeto**

1. **Modelo de Dados (`Call`)**:
    - O modelo `Call` representa uma chamada telefônica, com campos para armazenar a origem, destino, hora de início, hora de término, duração e status da chamada.
2. **Scripts de Automação (`populate_calls.py`)**:
    - Este script é responsável pela inserção de dados de chamadas fictícias no banco de dados. Ele utiliza o Django ORM para criar instâncias do modelo `Call` e preenchê-las com dados.
    - O comando `populate_calls` foi criado para permitir a execução do script diretamente do terminal, facilitando a automatização da inserção de dados de teste.
    - Para rodar o script basta usar o `python manage.py populate_calls`
3. **Painel de Monitoramento (Interface HTML)**:
    - A interface é baseada em HTML e é atualizada periodicamente via AJAX (com o uso de jQuery), garantindo que as informações sobre as chamadas e as estatísticas sejam exibidas em tempo real.
    - O gráfico é gerado com a biblioteca **Chart.js**, que permite visualizar dados de chamadas, como o total de chamadas e a duração total.
4. **API de Dados**:
    - O Django também fornece uma API para fornecer os dados das chamadas em formato JSON, o que permite que o painel de monitoramento seja atualizado dinamicamente sem necessidade de recarregar a página.

### **Instruções de Instalação e Deploy no Debian Linux**

### **Pré-requisitos**

Antes de seguir as instruções abaixo, tenha certeza de que você tem o Python 3, Git e o Debian Linux configurado corretamente. Você pode verificar isso com os seguintes comandos:

```
python3 --version
git --version

```

### **1. Clonar o Repositório**

Primeiro, você deve clonar o repositório do projeto. Se você ainda não o fez, execute o seguinte comando:

```
git clone https://github.com/Kayro-rocha/Mailing.git
cd gestao_mailing

```

### **2. Criar um Ambiente Virtual**

Crie um ambiente virtual para isolar as dependências do seu projeto:

```
python3 -m venv venv
source venv/bin/activate  # Para Linux/macOS

```

Para desativar o ambiente virtual, basta rodar o comando `deactivate`.

### **3. Instalar Dependências**

Instale as dependências necessárias com o comando:

```
pip install -r requirements.txt

```

Esse comando instalará as bibliotecas listadas no arquivo `requirements.txt`, que inclui o Django, entre outras bibliotecas.

### **4. Configuração do Banco de Dados**

Após instalar as dependências, você precisa rodar as migrações para configurar o banco de dados:

- O banco de dados usado foi o PostgreSQL(localhost) se desejar usar ele localmente segue os passos:
    - 1 - Acesse o PoweShell e use o comando `psql -U postgres` com isso você ira acessar o PowerShell do postrgres. Logo após ele pedira uma senha (essa senha e a que você colocou na hora da instalação)
    - 2 - Já dentro do terminal postgres voce criara a tabela do banco com o comando `CREATE DATABASE mailing;`
    - 3 - Após isso vamos conectar ele com o Django. Vamos no `app > [settings.py](http://settings.py)` apos isso procure `DATABASE`  nele iremos fazer a configuração. Ficara assim:
        
        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'Nome da tabela', #mailing
                'USER': 'postgres', #usuario padrao
                'PASSWORD': 'admin', #senha de acesso que foi configurado no banco
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
        ```
        
    - 4 - Se desejar usar o SQLlite que já vem por padrão no python/django e só fazer essa configuração:
        
        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
        ```
        
    - 45- Após isso e só rodar o comando abaixo e estará tudo certo;
        
        ```
        python manage.py migrate
        
        ```
        

Isso criará as tabelas no banco de dados conforme o modelo `Call` e outros modelos definidos no Django.

### **5. Rodar o Servidor de Desenvolvimento**

Para rodar o servidor de desenvolvimento local, execute o seguinte comando:

```
python manage.py runserver

```

Você pode acessar a aplicação no navegador, em: [http://127.0.0.1:8000](http://127.0.0.1:8000/).

### **6. Criar um Comando Customizado para Inserir Chamadas (Opcional)**

Se desejar preencher o banco de dados com dados fictícios, você pode rodar o comando personalizado que criamos (`populate_calls`):

```
python manage.py populate_calls

```

Esse comando insere chamadas falsas no banco de dados para simular um cenário de monitoramento de chamadas.

### **7. Criando o super usuário para esta acessando o painel do adm**

- Para criar o super usuário basta por o comando `python [manage.py](http://manage.py/) createsuperuser` após isso crie um usuário e senha. Depois e so rodar o projeto com o comando `python manage.py runserver`  e acessar a rota `/admin`

### **Deploy no Debian Linux com Gunicorn e Nginx**

### **1. Instalar Dependências**

Caso o Debian não tenha o Python 3, Gunicorn e Nginx instalados, use o seguinte comando para instalá-los:

```
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

```

### **2. Criar um Usuário para Execução da Aplicação**

Crie um novo usuário dedicado para rodar o projeto, isso melhora a segurança:

```
sudo useradd -m -s /bin/bash gestao_mailing
sudo su - gestao_mailing

```

### **3. Configurar o Projeto no Debian**

Agora, clone o repositório no servidor e configure o ambiente:

```
sh
CopiarEditar
git clone https://github.com/Kayro-rocha/Mailing.git
cd gestao_mailing
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### **4. Executar a Aplicação com Gunicorn**

Gunicorn é um servidor WSGI para aplicações Python, recomendado para ambientes de produção. Para executá-lo, use o comando:

```
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 gestao_mailing.wsgi:application

```

Isso fará a aplicação rodar no IP 0.0.0.0 e na porta 8000.

### **5. Configurar o Nginx como Proxy Reverso**

O Nginx pode ser configurado para servir sua aplicação Django via Gunicorn. Edite o arquivo de configuração do Nginx para apontar para o Gunicorn.

Edite o arquivo de configuração:

```
sudo nano /etc/nginx/sites-available/gestao_mailing

```

Adicione a seguinte configuração:

```
ng
server {
    listen 80;
    server_name sua-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

Ative a configuração do Nginx:

```
sudo ln -s /etc/nginx/sites-available/gestao_mailing /etc/nginx/sites-enabled
sudo systemctl restart nginx

```

### **6. Iniciar a Aplicação em Produção**

Se você deseja que a aplicação rode em segundo plano, pode usar o **systemd** ou ferramentas como o **Supervisor** para manter a aplicação rodando após reinicializações.

---

### **Explicação do Processo de Validação via BNE (Borda, Normalidade, Excepcionalidade)**

1. **Borda**: Certificar-se de que os dados estão sendo inseridos corretamente no banco de dados. Para isso, as validações no modelo `Call` e na inserção de dados devem garantir que os valores estão dentro de um intervalo aceitável.
2. **Normalidade**: Assegurar que o fluxo de chamadas segue um padrão normal. Você pode validar se a duração das chamadas está dentro de um intervalo razoável e se os dados são consistentes (por exemplo, se o horário de término não é anterior ao horário de início).
3. **Excepcionalidade**: Garantir que o sistema consegue lidar com dados excepcionais, como chamadas com durações negativas, dados ausentes ou outros erros inesperados.

## 🚀 Funcionalidades

📊 Painel com estatísticas de chamadas.

📜 Registro de chamadas com origem, destino, início, fim, duração e status.

🔄 Atualização automática da interface a cada 5 segundos.

📡 API para fornecimento de dados em JSON.

🛠️ Tecnologias Utilizadas

Python + Django

PostgreSQL

HTML, CSS e JavaScript

Chart.js para visualização de dados

jQuery para atualização dinâmica
