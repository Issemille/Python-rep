Auth and AUdit API


A samll API, written in Python, just to try it out and learn some stuff


This API provides the following functionality:

- User creation with securely hashed passwords

- User authentication via login

- Token-based authentication

- Protected endpoints requiring a valid token

- Audit logging of successful and failed login attempts

- Persistent storage using SQLite



This project is built using the following technologies:

- Python

- FastAPI

- Pydantic

- SQLite

- passlib (bcrypt)


How to run:

Clone the repository

Create and activate a Python virtual environment

Install dependencies

Start the server using uvicorn


pip install -r requirements.txt
uvicorn main:app --reload


http://127.0.0.1:800



Curl commands:

curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"hugo","password":"securepassword"}'


curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"hugo","password":"securepassword"}'


curl http://127.0.0.1:8000/people \
  -H "Authorization: Bearer <TOKEN>"
