# Assignment05
# Travel API

The Travel API is a microservices-based system that manages user authentication, travel destinations, and authorization using three interconnected services (Users, Destinations, and Authentication) to provide secure access to travel-related data and operations.

## Table of Contents
- [Description](#description)
- [Git Clone Instructions](#git-clone-instructions)
- [How to Run](#how-to-run)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Validations](#validations)
- [Schema](#schema)
- [Dependencies](#dependencies)


## Descriptionxdg-open htmlcov/index.html

Develop a Travel API using Flask with a microservices architecture. Each microservice handles specific functions: Destinations (managing travel destinations), Users (registration and profile management), and Authentication (token-based authentication with role-based access). The API follows OpenAPI/Swagger standards and uses Python's built-in data structures.

## Git Clone Instructions

To clone this project to your local machine, follow these steps:



1. **Open terminal (Command Prompt, PowerShell, or Terminal)**

2. **Clone the repository**: git clone https://github.com/M-E-U-E/travel_api.git
   
    Go to the Directory:
    ```bash
    cd travel_api
    ```
3. **Set Up Virtual Environment**
   
    ```bash
    # Create virtual environment
    python -m venv venv
    
    # Activate virtual environment
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
    Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```
    If requirements.txt is missing, install these packages:
    ```bash
    pip install flask
    pip install flask-cors
    pip install flask-swagger-ui
    pip install pyjwt
    pip install werkzeug
    pip install requests
    ```
4. **Start the Services
    Open three separate terminals (make sure virtual environment is activated in each):
    Run the backend api:**
    ```bash
    # Terminal 1 - Users Service (Port 5001)
    python users/app.py
    
    # Terminal 2 - Destinations Service (Port 5002)
    python destinations/app.py
    
    # Terminal 3 - Authentication Service (Port 5003)
    python authentication/app.py
    ```
    
    ### **Access Swagger UIs:**
    1. Users Service: http://localhost:5001/swagger
    2. Destinations Service: http://localhost:5002/swagger
    3. Authentication Service: http://localhost:5003/swagger
    
    
# How to Run:
   Here are the command to run every micro services, make sure that all three are running in separate terminal.
   ```
      python users/app.py or python -m users.app
      python authentication/app.py or python -m authentication.app
      python destinations/app.py or python -m destinations.app
   ```
 1. ## Users:
      Register: 
      ```
      {
       "username": "admin_jane",
       "password": "AdminPass123",
       "email": "jane.admin@example.com",
       "role": "admin"
      }
      ```
     Login:
     ```
     {
     "username": "admin_jane",
     "password": "AdminPass123"
     }
     ```
     Then generated token can be use.


     For Get/Profile:
     Use this for Get Profile:
     ```
     {
       "username": "admin",
       "password": "admin123"
     }
     ```
     Then use the generated token, Click "Authorize" at the top and enter your token without the Bearer prefix.
     Only use the token then clicked "Authorize" and "Close" 
     Then you can directly click "Execute" on the /profile endpoint.
   3. ## Authentication:
      Use the generated token, Click "Authorize" at the top and enter your token with the "Bearer" prefix.
      
        ```
        Bearer eyfhysrfyurf...
        ```
     
      Like this way then clicked "Authorize" and "Close" 
      then you can check Authorization and Validity
   5. ## Destinations
       Here any one can check all hotel but only admin can delete destinations by its ID
       here can be use the generated tokhn of this:  
       Here you can use any admin token to delete any destination,
       for this you have to follow the previous method.
       Use the generated token, Click "Authorize" at the top and enter your token with the "Bearer" prefix.
      
        ```
        Bearer eyfhysrfyurf...
        ```
        
       Like this way then clicked "Authorize" and "Close" 
       then you can delete a destination by its ID.
    
   ## Features
   
       - Users Service (Port 5001): Handles user registration, login, and profile management
       - Destinations Service (Port 5002): Manages travel destinations
       - Authentication Service (Port 5003): Handles token validation and authorization

   # Test
   
      # Step 1: Install necessary dependencies (if not already installed)
      pip install Flask coverage werkzeug requests pytest
      
      # Step 2: Run the tests using unittest (with coverage)
      # This will discover and run all the tests in the 'tests' directory
      python -m unittest discover tests  # This runs the tests in the 'tests' folder
      
      # Step 3: Alternatively, run the tests directly with coverage for more detailed reports
      # This will execute the tests in the specified test file and track code coverage
      python test_users_api.py  # Ensure the script with tests is named 'test_users_api.py'
      
      # Step 4: View the coverage summary after running the tests
      # This will print out a coverage report and generate an HTML report if configured in the test file
      # Make sure you have COV.report() and COV.html_report() in your code
      
      # Step 5: If you prefer using pytest for better test output and features, install pytest
      pip install pytest  # Install pytest
      
      # Step 6: Run the tests using pytest for more detailed output and reporting
      pytest tests/  # This runs all tests in the 'tests' directory with pytest
      
      # Step 7: If you want to run a specific test file or test method with pytest
      # You can run it like this:
      pytest tests/test_users_api.py  # Run a specific test file
      pytest -k 'test_register_success'  # Run a specific test method by name
      
      # Step 8: View the pytest test output for success or failure details
      # It will provide detailed logs indicating which tests failed or passed.
## Main Testing Command:

      pip install coverage
      python -m coverage run -m unittest discover -s tests
      python -m coverage html
      start htmlcov/index.html or xdg-open htmlcov/index.html

```coverage run -m unittest discover -s tests```

   ### Endpoint Operations & Testing Guide
    1. Users Service (Port 5001)
       ```
         User {
            id: string
            username: string
            password: string (hashed)
            email: string
            role: string (admin/user)
        }
       ```
        - Endpoints:
        POST /register
        POST /login
        GET /profile
    2. Destinations Service (Port 5002)
        ```
         Destination {
             id: integer
             name: string
             description: string
             location: string
         }
        ```
        - Endpoints:
        GET /destinations
        DELETE /destinations/{id} (admin only)
     3. Authentication Service (Port 5003)
       ```
        Token {
            username: string
            role: string
            exp: datetime
        }
       ```
        - Endpoints:
         POST /validate
         POST /authorize


## Project Structure
```
TRAVEL_API/
│
├── authentication/
│   ├── __pycache__/
│   ├── static/
│   │   └── swagger.json
│   ├── __init__.py
│   ├── app.py
│   └── utils.py
│
├── destinations/
│   ├── __pycache__/
│   ├── static/
│   │   └── swagger.json
│   ├── __init__.py
│   ├── app.py
│   └── requirements.txt
│
├── static/
│
├── users/
│   ├── __pycache__/
│   ├── static/
│   │   └── swagger.json
│   ├── __init__.py
│   ├── app.py
│   └── utils.py
│
├── venv/
│
├── __init__.py
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```
## Technologies Used

- **Backend Framework: Flask (Python web framework)
- **Authentication: JWT (JSON Web Tokens) with PyJWT library
- **API Documentation: Swagger/OpenAPI with flask-swagger-ui
- **Jest: Testing framework for unit and integration tests
- **Security: Werkzeug for password hashing, CORS handling with flask-cors
- **Database: In-memory Python dictionaries (can be extended to SQLite/PostgreSQL)
- **Architecture: Microservices (3 services: Users, Destinations, Authentication)
  
## Validations  
  valid:
**Use this for Register and login**
   ```
       register:
       {
           "username": "admin_jane",
           "password": "AdminPass123",
           "email": "jane.admin@example.com",
           "role": "admin"
       }
       login:
       {
         "username": "admin_jane",
         "password": "AdminPass123"
       }
   ```
   
  invalid:
  
       // Invalid username (special characters)
       {
           "username": "john@doe",
           "password": "Password123"
       }
       // Invalid password (no uppercase)
       {
           "username": "john_doe",
           "password": "password123"
       }
       // Invalid email format
       {
           "username": "john_doe",
           "password": "Password123",
           "email": "not-an-email"
       }
       // Invalid role
       {
           "username": "john_doe",
           "password": "Password123",
           "email": "john@example.com",
           "role": "superuser"
       }


## Schema
  Database Schema (In-Memory):
  ```bash
  Users Table:
  +----------+-----------+----------+-------+
  | id       | username  | email    | role  |
  +----------+-----------+----------+-------+
  | string   | string    | string   | string|
  +----------+-----------+----------+-------+
  
  Destinations Table:
  +----+--------+-------------+----------+
  | id | name   | description | location |
  +----+--------+-------------+----------+
  | int| string | string      | string   |
  +----+--------+-------------+----------+
  ```
  # Authorization Rules:
   ```
      Role Permissions:
    ├── Admin
    │   ├── View all destinations
    │   ├── Delete destinations
    │   └── Access all profiles
    └── User
        ├── View destinations
        └── Access own profile
   ```
 ## Dependencies

 ### Remember:
     -Keep all three services running
     -Use the token within 24 hours
     -Always include "Bearer " before the token only exception for Get/profile
     -Check terminal outputs for error messages
