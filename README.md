# assignment_paf

# Auth REST API

## Setup

Follow the initial commands in the git bash

```sh
git clone <repository-url>
cd assignment_paf
docker-compose up -d

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



