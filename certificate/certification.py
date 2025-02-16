import ssl
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta
import os


class CertificadoSSL:
    def __init__(self, certificado_path, chave_path):
        self.certificado_path = certificado_path
        self.chave_path = chave_path

    def gerar_certificado_autoassinado(self):
        if os.path.exists(self.certificado_path) and os.path.exists(self.chave_path):
            return

        chave = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"BR"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"DF"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Brasília"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"MeuServidor"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
        ])

        certificado = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(
            chave.public_key()).serial_number(x509.random_serial_number()).not_valid_before(
            datetime.utcnow()).not_valid_after(datetime.utcnow() + timedelta(days=365)).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"localhost")]), critical=False).sign(chave, hashes.SHA256())

        os.makedirs(os.path.dirname(self.certificado_path), exist_ok=True)
        with open(self.chave_path, "wb") as chave_file:
            chave_file.write(chave.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()))

        with open(self.certificado_path, "wb") as cert_file:
            cert_file.write(certificado.public_bytes(encoding=serialization.Encoding.PEM))

        print(f"Certificado e chave gerados em {self.certificado_path} e {self.chave_path}.")

    def carregar_certificado(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.certificado_path, keyfile=self.chave_path)
        return context

    def configurar_cliente(self):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context
