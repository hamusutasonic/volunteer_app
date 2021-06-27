#!/bin/bash
export FLASK_APP=app.py
export FLASK_ENV=development

#development env variables
export DB_HOST="0.0.0.0:5433"
export DB_USER="postgres"
export DB_PASSWORD="password"
export DB_NAME="volunteer_app"

export AUTH0_DOMAIN="dev--3lz2zai.us.auth0.com"
export API_AUDIENCE="volunteer_app"
export ALGORITHMS="RS256"
export AUTH0_CLIENT_ID="58E0NNPVPMGakxyx3c3FMY5l8Zoh3WJe"
