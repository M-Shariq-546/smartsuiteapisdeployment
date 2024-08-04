from django.contrib.auth.base_user import BaseUserManager



# This manager is used for normaliztion to prevent some improper data integrations in db
class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, role, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        
        if not email:
            raise ValueError('Email is required')
        
        user = self.normalize_email(email)
        user = self.model(email = email, first_name = first_name, last_name = last_name, role = role, **extra_fields)
        

        user.set_password(password)
        user.save(using = self.db)
        
        return user
    
    def create_superuser(self, email, first_name, last_name, role, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Super user must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Super user must have is_superuser=True")


        return self.create_user(email, first_name, last_name, role, password, **extra_fields)
