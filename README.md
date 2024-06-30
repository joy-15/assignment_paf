# assignment_paf

# Auth REST API

## Setup

1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies
4. Start the application using Docker Compose

```sh
git clone <repository-url>
cd assignment
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
docker-compose up --build

#Signup (POST /signup/)
curl -X POST http://localhost:8000/signup/ \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "securepassword"}'

#Signin (POST /signin/)
curl -X POST http://localhost:8000/signin/ \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=securepassword"

#Get Current User (GET /users/me/)
curl -H "Authorization: Bearer <your_access_token>" http://localhost:8000/users/me/

#Revoke Token (POST /token/revoke/)
curl -X POST http://localhost:8000/token/revoke/ \
     -H "Authorization: Bearer <your_access_token>"

#Refresh Token (POST /token/refresh/)
curl -X POST http://localhost:8000/token/refresh/ \
     -H "Authorization: Bearer <your_refresh_token>"



