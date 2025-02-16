import json
import socket
import time
from certificate.certification import CertificadoSSL
import defs

operacoes_realizadas = []

def handle_client(cliente_socket: socket.socket, context) -> None:
    cliente_socket_seguro = None
    try:
        cliente_socket_seguro = context.wrap_socket(cliente_socket, server_side=True)
        while True:
            requisicao = cliente_socket_seguro.recv(1024).decode("utf-8")
            if not requisicao:
                break
            handle_request(requisicao, cliente_socket_seguro)
    except Exception as e:
        print(f"Erro ao tratar requisição: {e}")
        if cliente_socket_seguro:
            resposta = {"erro": str(e)}
            cliente_socket_seguro.sendall(json.dumps(resposta).encode("utf-8"))
    finally:
        if cliente_socket_seguro:
            cliente_socket_seguro.close()

def handle_request(requisicao: str, cliente_socket_seguro: socket.socket) -> None:
    try:
        dados = json.loads(requisicao)
        metodoHTTP = dados.get("metodo")
        detalhes = dados.get("body", "")
        
        if metodoHTTP == "GET":
            handle_get_request(cliente_socket_seguro)
        elif metodoHTTP == "POST":
            handle_post_request(detalhes, cliente_socket_seguro)
        else:
            raise ValueError("Método HTTP inválido.")
    except json.JSONDecodeError:
        raise ValueError("Requisição malformada. Não é um JSON válido.")
    except KeyError:
        raise ValueError("Requisição incompleta. Faltam campos obrigatórios.")

def handle_get_request(cliente_socket_seguro: socket.socket) -> None:
    resposta = {"operacoes": operacoes_realizadas}
    resposta_json = json.dumps(resposta)
    cliente_socket_seguro.sendall(resposta_json.encode("utf-8"))

def handle_post_request(detalhes: str, cliente_socket_seguro: socket.socket) -> None:
    try:
        parametros = dict(param.split("=") for param in detalhes.split("&"))
        operacao = int(parametros.get("operacao", 0))
        x = int(parametros.get("x", 0))
        y = int(parametros.get("y", 0))
        resultado = calcular(operacao, x, y)
        
        # Salva a operação realizada
        operacoes_realizadas.append({
            "operacao": operacao,
            "x": x,
            "y": y,
            "resultado": resultado,
            "timestamp": time.time()
        })
        
        resposta = {"resultado": resultado, "mensagem": "POST realizado com sucesso"}
        cliente_socket_seguro.sendall(json.dumps(resposta).encode("utf-8"))
    except (IndexError, ValueError) as e:
        raise ValueError(f"Erro ao processar os detalhes da requisição: {e}")

def calcular(operacao: int, x: int, y: int) -> float:
    if operacao == 1:
        return defs.soma(x, y)
    elif operacao == 2:
        return defs.subtracao(x, y)
    elif operacao == 3:
        return defs.multiplicacao(x, y)
    elif operacao == 4:
        return defs.divisao(x, y)
    else:
        raise ValueError("Operação inválida.")

if __name__ == "__main__":
    caminho_certificado = "certificate/server-client/server.crt"
    caminho_chave = "certificate/server-client/server.key"
    certificado = CertificadoSSL(certificado_path=caminho_certificado, chave_path=caminho_chave)
    certificado.gerar_certificado_autoassinado()
    context = certificado.carregar_certificado()

    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.bind(("localhost", 443))
    socket_servidor.listen(5)
    print("Servidor aguardando conexões...")
    
    while True:
        cliente_socket, endereco_cliente = socket_servidor.accept()
        print(f"Conexão estabelecida com {endereco_cliente}")
        handle_client(cliente_socket, context)