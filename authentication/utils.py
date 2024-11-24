import jwt

SECRET_KEY = 'your-secret-key'  # Must match the key in users service

def validate_token(token):
    if not token:
        return None, None
        
    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
            
        # Decode the token
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        # Check if we have username and role in the token
        username = data.get('username')
        role = data.get('role')
        
        if not username or not role:
            return None, None
            
        return username, role  # Return username instead of user_id
        
    except Exception as e:
        print(f"Token validation error: {str(e)}")  # For debugging
        return None, None

def is_authorized(role, resource):
    if role == 'admin':
        return True
    elif role == 'user' and resource in ['view_destinations']:
        return True
    return False