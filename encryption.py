"""
Encryption utilities for the password manager.
Handles encryption and decryption of passwords using Fernet (symmetric encryption).
"""

from cryptography.fernet import Fernet
import os
import base64
import hashlib


class EncryptionManager:
    """Manages encryption and decryption of passwords."""
    
    @staticmethod
    def derive_key_from_password(master_password: str) -> bytes:
        """
        Derive a Fernet key from a master password.
        
        Args:
            master_password: The master password to derive key from
            
        Returns:
            A valid Fernet key (bytes)
        """
        # Hash the master password and encode it to base64 to get a valid Fernet key
        password_hash = hashlib.sha256(master_password.encode()).digest()
        return base64.urlsafe_b64encode(password_hash)
    
    @staticmethod
    def encrypt_password(password: str, master_password: str) -> str:
        """
        Encrypt a password using the master password.
        
        Args:
            password: The password to encrypt
            master_password: The master password
            
        Returns:
            Encrypted password as a string
        """
        key = EncryptionManager.derive_key_from_password(master_password)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(password.encode())
        return encrypted.decode()
    
    @staticmethod
    def decrypt_password(encrypted_password: str, master_password: str) -> str:
        """
        Decrypt a password using the master password.
        
        Args:
            encrypted_password: The encrypted password
            master_password: The master password
            
        Returns:
            Decrypted password as a string
            
        Raises:
            cryptography.fernet.InvalidToken: If decryption fails
        """
        key = EncryptionManager.derive_key_from_password(master_password)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_password.encode())
        return decrypted.decode()
