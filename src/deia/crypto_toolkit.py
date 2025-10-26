"""
Encryption & Cryptography Toolkit - Comprehensive crypto library.

Provides symmetric/asymmetric encryption, hashing, digital signatures,
key management, and certificate support with security best practices.
"""

from typing import Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import logging

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding, ec
from cryptography.hazmat.primitives.kdf import pbkdf2
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import utils as asym_utils
from cryptography import x509
from cryptography.x509.oid import NameOID
import base64


logger = logging.getLogger(__name__)


# ===== ENUMS =====

class SymmetricAlgorithm(str, Enum):
    """Supported symmetric algorithms."""
    AES_128_CBC = "AES-128-CBC"
    AES_192_CBC = "AES-192-CBC"
    AES_256_CBC = "AES-256-CBC"
    AES_128_GCM = "AES-128-GCM"
    AES_256_GCM = "AES-256-GCM"
    CHACHA20 = "CHACHA20"


class AsymmetricAlgorithm(str, Enum):
    """Supported asymmetric algorithms."""
    RSA_2048 = "RSA-2048"
    RSA_4096 = "RSA-4096"
    ECDH_P256 = "ECDH-P256"
    ECDH_P384 = "ECDH-P384"
    ECDH_P521 = "ECDH-P521"


class HashAlgorithm(str, Enum):
    """Supported hash algorithms."""
    SHA256 = "SHA-256"
    SHA384 = "SHA-384"
    SHA512 = "SHA-512"
    BLAKE3 = "BLAKE3"


# ===== DATA STRUCTURES =====

@dataclass
class EncryptionResult:
    """Result of encryption operation."""
    ciphertext: bytes
    iv: bytes
    salt: Optional[bytes] = None
    tag: Optional[bytes] = None  # for GCM mode


@dataclass
class KeyPair:
    """Asymmetric key pair."""
    private_key: Any
    public_key: Any
    algorithm: AsymmetricAlgorithm
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


@dataclass
class Certificate:
    """X.509 certificate."""
    certificate: Any
    private_key: Optional[Any] = None
    issuer: Optional[str] = None
    subject: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None


# ===== SECURE RANDOM GENERATION =====

class SecureRandomGenerator:
    """Cryptographically secure random number generation."""

    @staticmethod
    def generate_bytes(length: int) -> bytes:
        """Generate random bytes."""
        return os.urandom(length)

    @staticmethod
    def generate_iv(length: int = 16) -> bytes:
        """Generate random IV (initialization vector)."""
        return os.urandom(length)

    @staticmethod
    def generate_salt(length: int = 16) -> bytes:
        """Generate random salt for key derivation."""
        return os.urandom(length)

    @staticmethod
    def generate_nonce(length: int = 12) -> bytes:
        """Generate random nonce (number used once)."""
        return os.urandom(length)


# ===== HASHING =====

class Hasher:
    """Hash data using various algorithms."""

    @staticmethod
    def hash(data: Union[str, bytes], algorithm: HashAlgorithm = HashAlgorithm.SHA256) -> str:
        """Hash data using specified algorithm."""
        if isinstance(data, str):
            data = data.encode()

        if algorithm == HashAlgorithm.SHA256:
            digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        elif algorithm == HashAlgorithm.SHA384:
            digest = hashes.Hash(hashes.SHA384(), backend=default_backend())
        elif algorithm == HashAlgorithm.SHA512:
            digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
        elif algorithm == HashAlgorithm.BLAKE3:
            try:
                import blake3
                return blake3.blake3(data).hex()
            except ImportError:
                # Fallback to SHA-256 if BLAKE3 not available
                digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        else:
            raise ValueError(f"Unknown hash algorithm: {algorithm}")

        digest.update(data)
        return digest.finalize().hex()

    @staticmethod
    def verify_hash(data: Union[str, bytes], hash_value: str, algorithm: HashAlgorithm = HashAlgorithm.SHA256) -> bool:
        """Verify data against a hash."""
        computed = Hasher.hash(data, algorithm)
        return computed == hash_value


# ===== SYMMETRIC ENCRYPTION =====

class SymmetricCrypto:
    """Symmetric encryption/decryption."""

    @staticmethod
    def derive_key(password: Union[str, bytes], salt: bytes, key_size: int = 32) -> bytes:
        """Derive encryption key from password using PBKDF2."""
        if isinstance(password, str):
            password = password.encode()

        kdf = pbkdf2.Pbkdf2(
            algorithm=hashes.SHA256(),
            length=key_size,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password)

    @staticmethod
    def encrypt(plaintext: Union[str, bytes], key: bytes, algorithm: SymmetricAlgorithm = SymmetricAlgorithm.AES_256_CBC) -> EncryptionResult:
        """Encrypt data using symmetric algorithm."""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()

        if algorithm in [SymmetricAlgorithm.AES_128_CBC, SymmetricAlgorithm.AES_192_CBC, SymmetricAlgorithm.AES_256_CBC]:
            return SymmetricCrypto._encrypt_aes_cbc(plaintext, key, algorithm)
        elif algorithm in [SymmetricAlgorithm.AES_128_GCM, SymmetricAlgorithm.AES_256_GCM]:
            return SymmetricCrypto._encrypt_aes_gcm(plaintext, key, algorithm)
        elif algorithm == SymmetricAlgorithm.CHACHA20:
            return SymmetricCrypto._encrypt_chacha20(plaintext, key)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    @staticmethod
    def _encrypt_aes_cbc(plaintext: bytes, key: bytes, algorithm: SymmetricAlgorithm) -> EncryptionResult:
        """Encrypt using AES CBC mode."""
        from cryptography.hazmat.primitives import padding as sym_padding

        iv = SecureRandomGenerator.generate_iv()

        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()

        # Add PKCS7 padding
        padder = sym_padding.PKCS7(128).padder()
        padded_plaintext = padder.update(plaintext) + padder.finalize()

        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

        return EncryptionResult(ciphertext=ciphertext, iv=iv)

    @staticmethod
    def _encrypt_aes_gcm(plaintext: bytes, key: bytes, algorithm: SymmetricAlgorithm) -> EncryptionResult:
        """Encrypt using AES GCM mode."""
        nonce = SecureRandomGenerator.generate_nonce()

        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(nonce),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        return EncryptionResult(
            ciphertext=ciphertext,
            iv=nonce,
            tag=encryptor.tag
        )

    @staticmethod
    def _encrypt_chacha20(plaintext: bytes, key: bytes) -> EncryptionResult:
        """Encrypt using ChaCha20."""
        nonce = SecureRandomGenerator.generate_nonce(16)  # ChaCha20 requires 16-byte nonce

        cipher = Cipher(
            algorithms.ChaCha20(key, nonce),
            None,
            backend=default_backend()
        )
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        return EncryptionResult(ciphertext=ciphertext, iv=nonce)

    @staticmethod
    def decrypt(encrypted: EncryptionResult, key: bytes, algorithm: SymmetricAlgorithm = SymmetricAlgorithm.AES_256_CBC) -> bytes:
        """Decrypt data using symmetric algorithm."""
        if algorithm in [SymmetricAlgorithm.AES_128_CBC, SymmetricAlgorithm.AES_192_CBC, SymmetricAlgorithm.AES_256_CBC]:
            return SymmetricCrypto._decrypt_aes_cbc(encrypted, key)
        elif algorithm in [SymmetricAlgorithm.AES_128_GCM, SymmetricAlgorithm.AES_256_GCM]:
            return SymmetricCrypto._decrypt_aes_gcm(encrypted, key)
        elif algorithm == SymmetricAlgorithm.CHACHA20:
            return SymmetricCrypto._decrypt_chacha20(encrypted, key)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    @staticmethod
    def _decrypt_aes_cbc(encrypted: EncryptionResult, key: bytes) -> bytes:
        """Decrypt using AES CBC mode."""
        from cryptography.hazmat.primitives import padding as sym_padding

        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(encrypted.iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()

        padded_plaintext = decryptor.update(encrypted.ciphertext) + decryptor.finalize()

        # Remove PKCS7 padding
        unpadder = sym_padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext

    @staticmethod
    def _decrypt_aes_gcm(encrypted: EncryptionResult, key: bytes) -> bytes:
        """Decrypt using AES GCM mode."""
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(encrypted.iv, encrypted.tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()

        plaintext = decryptor.update(encrypted.ciphertext) + decryptor.finalize()

        return plaintext

    @staticmethod
    def _decrypt_chacha20(encrypted: EncryptionResult, key: bytes) -> bytes:
        """Decrypt using ChaCha20."""
        cipher = Cipher(
            algorithms.ChaCha20(key, encrypted.iv),
            None,
            backend=default_backend()
        )
        decryptor = cipher.decryptor()

        plaintext = decryptor.update(encrypted.ciphertext) + decryptor.finalize()

        return plaintext


# ===== ASYMMETRIC ENCRYPTION =====

class AsymmetricCrypto:
    """Asymmetric encryption and key generation."""

    @staticmethod
    def generate_rsa_keypair(key_size: int = 2048) -> KeyPair:
        """Generate RSA key pair."""
        algorithm = AsymmetricAlgorithm.RSA_2048 if key_size == 2048 else AsymmetricAlgorithm.RSA_4096

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        return KeyPair(private_key=private_key, public_key=public_key, algorithm=algorithm)

    @staticmethod
    def generate_ecc_keypair(curve: str = "P256") -> KeyPair:
        """Generate ECC (Elliptic Curve) key pair."""
        if curve == "P256":
            algorithm = AsymmetricAlgorithm.ECDH_P256
            curve_obj = ec.SECP256R1()
        elif curve == "P384":
            algorithm = AsymmetricAlgorithm.ECDH_P384
            curve_obj = ec.SECP384R1()
        elif curve == "P521":
            algorithm = AsymmetricAlgorithm.ECDH_P521
            curve_obj = ec.SECP521R1()
        else:
            raise ValueError(f"Unknown curve: {curve}")

        private_key = ec.generate_private_key(curve_obj, default_backend())
        public_key = private_key.public_key()

        return KeyPair(private_key=private_key, public_key=public_key, algorithm=algorithm)

    @staticmethod
    def encrypt_rsa(plaintext: Union[str, bytes], public_key: Any) -> bytes:
        """Encrypt using RSA public key."""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()

        ciphertext = public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    @staticmethod
    def decrypt_rsa(ciphertext: bytes, private_key: Any) -> bytes:
        """Decrypt using RSA private key."""
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext


# ===== DIGITAL SIGNATURES =====

class DigitalSignature:
    """Digital signature generation and verification."""

    @staticmethod
    def sign(data: Union[str, bytes], private_key: Any) -> bytes:
        """Sign data using RSA private key."""
        if isinstance(data, str):
            data = data.encode()

        signature = private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    @staticmethod
    def verify(data: Union[str, bytes], signature: bytes, public_key: Any) -> bool:
        """Verify signature using RSA public key."""
        if isinstance(data, str):
            data = data.encode()

        try:
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False


# ===== KEY MANAGEMENT =====

class KeyManager:
    """Manage cryptographic keys securely."""

    @staticmethod
    def export_private_key(private_key: Any, password: Optional[bytes] = None) -> bytes:
        """Export private key (optionally encrypted)."""
        if password:
            encryption_algorithm = serialization.BestAvailableEncryption(password)
        else:
            encryption_algorithm = serialization.NoEncryption()

        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption_algorithm
        )

    @staticmethod
    def export_public_key(public_key: Any) -> bytes:
        """Export public key."""
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    @staticmethod
    def load_private_key(key_data: bytes, password: Optional[bytes] = None) -> Any:
        """Load private key (optionally encrypted)."""
        return serialization.load_pem_private_key(
            key_data,
            password=password,
            backend=default_backend()
        )

    @staticmethod
    def load_public_key(key_data: bytes) -> Any:
        """Load public key."""
        return serialization.load_pem_public_key(
            key_data,
            backend=default_backend()
        )

    @staticmethod
    def save_key_to_file(key_data: bytes, filepath: Path) -> None:
        """Save key to file securely."""
        filepath.write_bytes(key_data)
        # Set restrictive permissions on Unix systems
        try:
            os.chmod(filepath, 0o600)
        except (OSError, AttributeError):
            pass

    @staticmethod
    def load_key_from_file(filepath: Path, password: Optional[bytes] = None) -> Any:
        """Load key from file."""
        key_data = filepath.read_bytes()
        return KeyManager.load_private_key(key_data, password)


# ===== CERTIFICATE MANAGEMENT =====

class CertificateManager:
    """Manage X.509 certificates."""

    @staticmethod
    def generate_self_signed_cert(
        private_key: Any,
        subject_name: str,
        valid_days: int = 365
    ) -> Certificate:
        """Generate self-signed certificate."""
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Organization"),
            x509.NameAttribute(NameOID.COMMON_NAME, subject_name),
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=valid_days)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(subject_name)]),
            critical=False,
        ).sign(
            private_key,
            hashes.SHA256(),
            default_backend()
        )

        return Certificate(
            certificate=cert,
            private_key=private_key,
            subject=subject_name,
            valid_from=datetime.utcnow(),
            valid_until=datetime.utcnow() + timedelta(days=valid_days)
        )

    @staticmethod
    def export_certificate(cert: Certificate) -> bytes:
        """Export certificate in PEM format."""
        return cert.certificate.public_bytes(serialization.Encoding.PEM)

    @staticmethod
    def load_certificate(cert_data: bytes) -> Certificate:
        """Load certificate from PEM data."""
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        subject = cert.subject.rfc4514_string()
        return Certificate(certificate=cert, subject=subject)


# ===== UTILITY FUNCTIONS =====

def encode_base64(data: bytes) -> str:
    """Encode bytes to base64 string."""
    return base64.b64encode(data).decode('utf-8')


def decode_base64(data: str) -> bytes:
    """Decode base64 string to bytes."""
    return base64.b64decode(data.encode('utf-8'))
