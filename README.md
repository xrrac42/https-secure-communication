# HTTPS Secure Communication

Este projeto é um exemplo de comunicação segura entre um cliente e um servidor usando HTTPS (SSL/TLS). O cliente envia requisições para o servidor, que realiza operações matemáticas simples (soma, subtração, multiplicação e divisão) e retorna os resultados de forma segura.

## Visão Geral
O projeto consiste em três componentes principais:

- **Cliente (`client.py`)**: Um script Python que se conecta ao servidor e envia requisições para realizar operações matemáticas.
- **Servidor (`server.py`)**: Um script Python que recebe as requisições do cliente, realiza as operações matemáticas e retorna os resultados.
- **Operações Matemáticas (`defs.py`)**: Um módulo que contém as funções para realizar as operações matemáticas.

A comunicação entre o cliente e o servidor é protegida por certificados SSL/TLS, garantindo que os dados sejam transmitidos de forma segura.

## Porta Utilizada
O servidor roda na porta **443**, que é a porta padrão para comunicação HTTPS.

## Pré-requisitos
Antes de executar o projeto, certifique-se de ter o **Python 3.x** instalado em sua máquina. Além disso, instale as dependências necessárias.

## Instalando Dependências
O projeto utiliza algumas bibliotecas externas, que podem ser instaladas usando o arquivo `requirements.txt`. Para instalar as dependências, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

## Como Executar o Projeto

### 1. Executando o Servidor
Primeiro, inicie o servidor. Ele ficará aguardando conexões do cliente na porta **443**.

```bash
python server.py
```

O servidor irá gerar um certificado SSL autoassinado e aguardar conexões do cliente.

### 2. Executando o Cliente
Em outro terminal, execute o cliente. O cliente se conectará ao servidor e permitirá que você faça requisições para realizar operações matemáticas.

```bash
python client.py
```

O cliente solicitará que você escolha o tipo de requisição (**GET** ou **POST**), a operação matemática (**soma, subtração, multiplicação ou divisão**) e os valores de **x** e **y**.

### 3. Interagindo com o Sistema
1. O cliente enviará a requisição ao servidor.
2. O servidor processará a requisição, realizará a operação matemática e retornará o resultado ao cliente.
3. O cliente exibirá o resultado na tela.

## Ambiente Virtual (Opcional)
Recomendamos o uso de um ambiente virtual para isolar as dependências do projeto. Para criar e ativar um ambiente virtual, siga os passos abaixo:

### Criando um Ambiente Virtual
```bash
python -m venv venv
```

### Ativando o Ambiente Virtual
No **Linux/MacOS**:
```bash
source venv/bin/activate
```

No **Windows**:
```bash
venv\Scripts\activate
```

### Instalando Dependências no Ambiente Virtual
Após ativar o ambiente virtual, instale as dependências:
```bash
pip install -r requirements.txt
```

## Considerações Finais
- **Certificados SSL/TLS**: O projeto utiliza certificados autoassinados, o que é adequado para testes locais. Para um ambiente de produção, você deve usar certificados válidos emitidos por uma autoridade certificadora (CA).
- **Segurança**: Este projeto é um exemplo básico de como implementar comunicação segura usando SSL/TLS. Para aplicações reais, você deve considerar questões de segurança adicionais, como validação de certificados, proteção contra ataques de **man-in-the-middle**, etc.

## Comandos Resumidos
### Instalar dependências:
```bash
pip install -r requirements.txt
```

### Executar o servidor:
```bash
python server.py
```

### Executar o cliente:
```bash
python client.py
```

### Criar e ativar ambiente virtual (opcional):
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
