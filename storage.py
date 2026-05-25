"""
Storage utilities for the password manager.
Handles saving and loading password data from a JSON file.
"""

import json
import os
from typing import Dict, Optional
from encryption import EncryptionManager


class PasswordStorage:
    """Manages storage and retrieval of encrypted passwords."""
    
    def __init__(self, filename: str = "passwords.json"):
        """
        Initialize the password storage.
        
        Args:
            filename: The file to store password data
        """
        self.filename = filename
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load password data from file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def _save_data(self):
        """Save password data to file."""
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2)
        # Set restrictive permissions (read/write for owner only)
        os.chmod(self.filename, 0o600)
    
    def add_password(self, service: str, username: str, password: str, master_password: str):
        """
        Add a new password entry.
        
        Args:
            service: Name of the service/website
            username: Username for the service
            password: The password to store
            master_password: The master password for encryption
        """
        encrypted_password = EncryptionManager.encrypt_password(password, master_password)
        
        self.data[service] = {
            'username': username,
            'password': encrypted_password
        }
        
        self._save_data()
    
    def get_password(self, service: str, master_password: str) -> Optional[Dict]:
        """
        Retrieve a password entry.
        
        Args:
            service: Name of the service/website
            master_password: The master password for decryption
            
        Returns:
            Dictionary with username and decrypted password, or None if not found
        """
        if service not in self.data:
            return None
        
        entry = self.data[service]
        try:
            decrypted_password = EncryptionManager.decrypt_password(
                entry['password'], 
                master_password
            )
            return {
                'username': entry['username'],
                'password': decrypted_password
            }
        except Exception as e:
            print(f"Error decrypting password: {e}")
            return None
    
    def delete_password(self, service: str) -> bool:
        """
        Delete a password entry.
        
        Args:
            service: Name of the service/website
            
        Returns:
            True if deleted, False if not found
        """
        if service in self.data:
            del self.data[service]
            self._save_data()
            return True
        return False
    
    def list_services(self) -> list:
        """
        Get list of all stored services.
        
        Returns:
            List of service names
        """
        return list(self.data.keys())
