"""
Simple Password Manager
A command-line password manager with encryption support.
"""

from storage import PasswordStorage
import getpass
import sys


class PasswordManager:
    """Main password manager application."""
    
    def __init__(self):
        """Initialize the password manager."""
        self.storage = PasswordStorage()
        self.master_password = None
    
    def authenticate(self) -> bool:
        """
        Authenticate user with master password.
        
        Returns:
            True if authentication successful
        """
        master_password = getpass.getpass("Enter your master password: ")
        self.master_password = master_password
        return True
    
    def show_menu(self):
        """Display the main menu."""
        print("\n" + "="*40)
        print("PASSWORD MANAGER")
        print("="*40)
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. List all services")
        print("4. Delete a password")
        print("5. Exit")
        print("="*40)
    
    def add_password(self):
        """Add a new password entry."""
        service = input("Enter service/website name: ").strip()
        
        if not service:
            print("Service name cannot be empty!")
            return
        
        if service in self.storage.list_services():
            overwrite = input(f"'{service}' already exists. Overwrite? (y/n): ").strip().lower()
            if overwrite != 'y':
                return
        
        username = input("Enter username: ").strip()
        password = getpass.getpass("Enter password: ")
        password_confirm = getpass.getpass("Confirm password: ")
        
        if password != password_confirm:
            print("Passwords do not match!")
            return
        
        try:
            self.storage.add_password(service, username, password, self.master_password)
            print(f"✓ Password for '{service}' saved successfully!")
        except Exception as e:
            print(f"✗ Error saving password: {e}")
    
    def retrieve_password(self):
        """Retrieve a stored password."""
        service = input("Enter service/website name: ").strip()
        
        if not service:
            print("Service name cannot be empty!")
            return
        
        result = self.storage.get_password(service, self.master_password)
        
        if result is None:
            print(f"✗ Service '{service}' not found!")
            return
        
        print(f"\nService: {service}")
        print(f"Username: {result['username']}")
        print(f"Password: {result['password']}")
        print()
    
    def list_services(self):
        """List all stored services."""
        services = self.storage.list_services()
        
        if not services:
            print("No passwords stored yet!")
            return
        
        print("\nStored services:")
        for i, service in enumerate(services, 1):
            print(f"{i}. {service}")
        print()
    
    def delete_password(self):
        """Delete a password entry."""
        service = input("Enter service/website name to delete: ").strip()
        
        if not service:
            print("Service name cannot be empty!")
            return
        
        confirm = input(f"Are you sure you want to delete '{service}'? (y/n): ").strip().lower()
        
        if confirm == 'y':
            if self.storage.delete_password(service):
                print(f"✓ Password for '{service}' deleted!")
            else:
                print(f"✗ Service '{service}' not found!")
        else:
            print("Deletion cancelled.")
    
    def run(self):
        """Run the password manager application."""
        print("Welcome to Password Manager!")
        
        if not self.authenticate():
            print("Authentication failed!")
            return
        
        while True:
            self.show_menu()
            choice = input("Select an option (1-5): ").strip()
            
            if choice == '1':
                self.add_password()
            elif choice == '2':
                self.retrieve_password()
            elif choice == '3':
                self.list_services()
            elif choice == '4':
                self.delete_password()
            elif choice == '5':
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid option! Please try again.")


if __name__ == "__main__":
    app = PasswordManager()
    app.run()
