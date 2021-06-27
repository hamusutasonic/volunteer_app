import os
from datetime import datetime

from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from models import setup_db, User, Organisation, Event
from auth import AuthError, requires_auth

app = Flask(__name__)
db = setup_db(app)

CORS(app)

migrate = Migrate(app, db)

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
API_AUDIENCE = os.environ['API_AUDIENCE']
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']

if os.getenv('FLASK_ENV', None) == 'development':
    DOMAIN = "http://localhost:5000"
else:
    DOMAIN = "https://frozen-beach-49034.herokuapp.com"

#----------------------------------------------------------------------------#
# Routes to get jwt token
#----------------------------------------------------------------------------#
@app.route('/')
def index():
    """Render a button to direct to Auth0 login
    """
    authorize_link = f"https://{AUTH0_DOMAIN}/authorize?" + \
        f"audience={API_AUDIENCE}" + \
        "&response_type=token" + \
        f"&client_id={AUTH0_CLIENT_ID}" + \
        f"&redirect_uri={DOMAIN}/login-results"

    return render_template(
        'index.html',
        authorize_link=authorize_link
    )

@app.route('/login-results')
def login_results():
    """Print jwt token after successfully login to page
    """
    logout_link = f"https://{AUTH0_DOMAIN}/v2/logout?" + \
        f"client_id={AUTH0_CLIENT_ID}" + \
        f"&returnTo={DOMAIN}"
        
    return render_template(
        'login-results.html',
        logout_link = logout_link
    )

#----------------------------------------------------------------------------#
# Api Endpoints - Events
#----------------------------------------------------------------------------#
"""
Get all events
"""
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify({
        'success': True, 
        'data': [e.format() for e in events]
    })

"""
Get specific event
"""
@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify({
        'success': True, 
        'data': event.format()
    })

"""
Create an event
"""
@app.route('/events', methods=['POST'])
@requires_auth(permission='create:event')
def create_event(jwt_payload):
    body = request.get_json()
    
    org_id = body.get('organisation_id', None)
    org = Organisation.query.get(org_id) 
    if not org:
        abort(422)

    #login user different from resource user
    auth0_id = jwt_payload.get('sub', None)
    if org.auth0_id != auth0_id:
        abort(403)
        
    try:
        # nullable checking, foreign_id checking, datetime format 
        # checking all done at database layer
        event = Event(**body)
        event.insert()
        return jsonify({
            'success': True,
            'created': event.format()
        })
    except Exception as e:
        print(e)
        abort(422)

"""
Update an event
"""
@app.route('/events/<int:event_id>', methods=['PATCH'])
@requires_auth(permission='update:event')
def update_event(jwt_payload, event_id):
    body = request.get_json()

    event = Event.query.get(event_id)
    if not event:
        abort(422)

    #login user different from resource user
    org = event.organisation
    auth0_id = jwt_payload.get('sub', None)
    if org.auth0_id != auth0_id:
        abort(403)

    try:
        # nullable checking, foreign_id checking, datetime format 
        # checking all done at database layer
        for key, value in body.items():
            setattr(event, key, value)

        event.update()
        return jsonify({
            'success': True,
            'updated': event.format()
        })
    except Exception as e:
        print(e)
        abort(422)

"""
Delete an event
"""
@app.route('/events/<int:event_id>', methods=['DELETE'])
@requires_auth(permission='delete:event')
def delete_event(jwt_payload, event_id):
    
    event = Event.query.get(event_id)
    if not event:
        abort(422)

    #login user different from resource user
    org = event.organisation
    auth0_id = jwt_payload.get('sub', None)
    if org.auth0_id != auth0_id:
        abort(403)

    try:
        event.delete()

        return jsonify({
            'success': True,
            'deleted': event_id
        })
    except Exception as e:
        print(e)
        abort(422)

"""
Add user to event    
"""
@app.route('/events/<int:event_id>/participants', methods=['POST'])
@requires_auth(permission='add:event-participant')
def add_user_to_event(jwt_payload, event_id):
    body = request.get_json()

    user_id = body.get('user_id', None)
    user = User.query.get(user_id)
    if not user:
        abort(422) 
    
    auth0_id = jwt_payload.get('sub', None)
    if user.auth0_id != auth0_id:
        abort(403, 'not permitted')

    try:
        event = Event.query.get(event_id)
        if not event:
            raise 

        event.participants.append(user)
        event.update()

        return jsonify({
            'success': True,
            'updated': {
                'event_id': event.id,
                'event_participants': [u.id for u in event.participants]
            }
        })
    except Exception as e:
        print(e)
        abort(422)

"""
Remove user from event    
"""
@app.route('/events/<int:event_id>/participants', methods=['DELETE'])
@requires_auth(permission='remove:event-participant')
def remove_user_from_event(jwt_payload, event_id):
    body = request.get_json()

    user_id = body.get('user_id', None)
    user = User.query.get(user_id)
    if not user:
        abort(422) 

    auth0_id = jwt_payload.get('sub', None)
    if user.auth0_id != auth0_id:
        abort(403, 'not permitted')

    try:
        event = Event.query.get(event_id)
        if not event: 
            raise
        
        event.participants.remove(user)
        event.update()

        return jsonify({
            'success': True,
            'updated': {
                'event_id': event.id,
                'event_participants': [u.id for u in event.participants]
            }
        })
    except Exception as e:
        print(e)
        abort(422)

#----------------------------------------------------------------------------#
# Api Endpoints - Organisations
#----------------------------------------------------------------------------#
"""
Get all organisations
"""
@app.route('/organisations', methods=['GET'])
def get_organisations():
    organisations = Organisation.query.all()
    return jsonify({
        'success': True,
        'data': [org.format() for org in organisations]
    })


"""
Get specific organisation details
"""
@app.route('/organisations/<int:organisation_id>', methods=['GET'])
def get_organisation(organisation_id):
    organisation = Organisation.query.get_or_404(organisation_id)

    data = organisation.format()
    past_events = []
    upcoming_events = []
    for event in organisation.events:
        if event.end_datetime <= datetime.now():
            past_events.append(event.format(include_org=False))
        else:
            upcoming_events.append(event.format(include_org=False))
    data['past_events'] = past_events
    data['upcoming_events'] = upcoming_events
    
    return jsonify({
        'success': True, 
        'data': data 
    })

#---------------------------------------
# Custom error handlers
#---------------------------------------
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized access"
    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "access is forbidden"
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['code']
    }), error.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)