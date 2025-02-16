import json
import socket
from certificate.certification import CertificadoSSL

def define_requisicao(requisicao: int, operacao: int, x: int, y: int) -> str:
    if requisicao == 1:
        body = json.dumps(
            {
                "metodo": "GET",
                "body": ""
            }
        )
    elif requisicao == 2:
        body = json.dumps(
            {
                "metodo": "POST",
                "body": f"operacao={operacao}&x={x}&y={y}"
            }
        )
    else:
        raise ValueError("Requisição inválida.")
    return body

if __name__ == "__main__":
    caminho_certificado = "certificate/server-client/server.crt"
    caminho_chave = "certificate/server-client/server.key"
    certificado = CertificadoSSL(certificado_path=caminho_certificado, chave_path=caminho_chave)
    contexto = certificado.configurar_cliente()

    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cliente.connect(('localhost', 443))
    socket_seguro_cliente = contexto.wrap_socket(socket_cliente, server_hostname='localhost', server_side=False)
    
    while True:
        try:
            print("Qual tipo de requisição deseja fazer?\n1.\tGET\n2.\tPOST\n")
            requisicao = int(input(":> "))
            print("\n--------------------------------------------------------------------------------------------------------------------------\n")
            
            if requisicao == 1:
                body = define_requisicao(requisicao, 0, 0, 0)
                socket_seguro_cliente.send(body.encode("utf-8"))
                resposta = socket_seguro_cliente.recv(1024).decode("utf-8")
                
                if resposta:
                    resposta_dict = json.loads(resposta)
                    if "operacoes" in resposta_dict:
                        print("Operações salvas no servidor:")
                        for op in resposta_dict["operacoes"]:
                            print(f"Operação: {op['operacao']}, X: {op['x']}, Y: {op['y']}, Resultado: {op['resultado']}, Timestamp: {op['timestamp']}")
                    else:
                        print("Nenhuma operação salva no servidor.")
                else:
                    print("Erro: Nenhuma resposta recebida do servidor.")
            
            elif requisicao == 2:
                # Requisição POST: Realizar operação matemática
                print("Digite qual operação deseja fazer.\n1.\tSoma\n2.\tSubtração\n3.\tMultiplicação\n4.\tDivisão\n0.\tEncerrar programa\n")
                operacao = int(input(":> "))
                if operacao == 0:
                    print("Encerrando programa...")
                    break
                
                print("\n--------------------------------------------------------------------------------------------------------------------------\n")
                print("Vamos tratar apenas operações simples com 2 dígitos:")
                x = int(input("Agora digite o valor de X:\n:> "))
                y = int(input("Digite o valor de Y:\n:> "))
                
                body = define_requisicao(requisicao, operacao, x, y)
                socket_seguro_cliente.send(body.encode("utf-8"))
                resposta = socket_seguro_cliente.recv(1024).decode("utf-8")
                
                if resposta:
                    resposta_dict = json.loads(resposta)
                    print(f"Resultado da operação: {resposta_dict['resultado']}")
                else:
                    print("Erro: Nenhuma resposta recebida do servidor.")
            
            else:
                print("Opção inválida.")
            
            print("\n--------------------------------------------------------------------------------------------------------------------------\n")
            continuar = input("Deseja continuar? [S/N]\n:> ")
            if continuar.lower() != "s":
                break
        except Exception as e:
            print(f"Erro ao tratar requisição: {e}")
            break
    socket_seguro_cliente.close()