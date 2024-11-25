# Assignment05
# Travel API

 A Backend API.

## Table of Contents
- [Description](#description)
- [Git Clone Instructions](#git-clone-instructions)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Schema](#schema)
- [Dependencies](#dependencies)


## Description

Develop a Travel API using Flask with a microservices architecture. Each microservice handles specific functions: Destinations (managing travel destinations), Users (registration and profile management), and Authentication (token-based authentication with role-based access). The API follows OpenAPI/Swagger standards and uses Python's built-in data structures.

## Git Clone Instructions

To clone this project to your local machine, follow these steps:



1. **Open terminal (Command Prompt, PowerShell, or Terminal)**

2. **Clone the repository**: git clone https://github.com/M-E-U-E/travel_api.git
   
    Go to the Directory:
    ```bash
    cd travel_api
    ```
3. **Set Up Virtual Environment
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
    Run the backend api:
    ```bash
    # Terminal 1 - Users Service (Port 5001)
    python users/app.py
    
    # Terminal 2 - Destinations Service (Port 5002)
    python destinations/app.py
    
    # Terminal 3 - Authentication Service (Port 5003)
    python authentication/app.py
    ```
    
    ### Access Swagger UIs:
    1. Users Service: http://localhost:5001/swagger
    2. Destinations Service: http://localhost:5002/swagger
    3. Authentication Service: http://localhost:5003/swagger
    
    
    #### Now open POSTMAN to check API Endpoints
   
## Features

    - Users Service (Port 5001): Handles user registration, login, and profile management
    - Destinations Service (Port 5002): Manages travel destinations
    - Authentication Service (Port 5003): Handles token validation and authorization
    
### Endpoint Operations & Testing Guide





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

- **Node.js: Runtime environment for server-side application execution
- **Express.js: Web application framework for handling routes and HTTP requests
- **TypeScript: Programming language for type safety and enhanced developmentNext.js: React framework for server-side rendering and static site generation
- **Jest: Testing framework for unit and integration tests
- **Supertest: HTTP endpoint testing library
- **File System (fs): Node.js module for file operations
- **React.js: Frontend library for building interactive user interfaces
- **Next.js: React framework for server-side rendering and static site generation
  
    
## Database Schema (In-Memory):
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

## Dependencies

### Remember:
     -Keep all three services running
     -Use the token within 24 hours
     -Always include "Bearer " before the token
     -Check terminal outputs for error messages
