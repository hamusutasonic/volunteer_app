from datetime import datetime

from flask import Flask

from models import setup_db, db, User, Organisation, Event


def reset_db_with_fixtures(db=db):
    db.drop_all()
    db.create_all()

    #----------------------------------------------------------------------------#
    # Fixtures - organisation 
    #----------------------------------------------------------------------------#
    org0 = Organisation(
        auth0_id =  'auth0|60c58135612d820070a5f049',
        name = 'Test Organisation',
        description = 'Test organisation authenticated through Auth0',
        website = 'http://mywebsite.com',
        phone_contact = '1111111',
        email_contact = 'test_org_01@test.com'
    )
    org0.insert()
    
    org1 = Organisation(
        name = 'Pet Welfare Society', 
        description = 'Open your heart to a cat in need',
        website = 'https://www.catwelfare.org/',
        email_contact = 'info@catwelfare.org',
        phone_contact = '96111111'
    )
    org1.insert()
    
    org2 = Organisation(
        name = 'East Youths', 
        description = 'An organisation of youths for the community',
        website = 'eastyouths.org', 
        email_contact = 'hey@eastyouths.org'
    )
    org2.insert()

    #----------------------------------------------------------------------------#
    # Fixtures - users 
    #----------------------------------------------------------------------------#

    u0 = User(
        auth0_id = 'auth0|60c58174612d820070a5f057',
        name = 'Test User', 
        age = 17,
        email_contact = 'test_user_01@test.com',
        phone_contact = '1111111',
        join_date = datetime(2020,5,21,21,30,0),
        skills = ['cooking', 'web development']
    )
    u0.insert()

    u1 = User(
        name = 'User01', 
        age = 31,
        email_contact = 'user01@test.com',
        phone_contact = '1111111',
        join_date = datetime(2020,7,1,0,0,0),
        skills = ['counselling']
    )
    u1.insert()

    u2 = User(
        name = 'User02', 
        age = 45,
        email_contact = 'user02@test.com',
        phone_contact = '1111111',
        join_date = datetime(2019,12,12,0,0,0),
        skills = None
    )
    u2.insert()

    u3 = User(
        name = 'User03', 
        age = 28,
        email_contact = 'user03@test.com',
        phone_contact = '1111111',
        join_date = datetime(2020,12,12,0,0,0),
        skills = ['counselling']
    )
    u3.insert()

    #----------------------------------------------------------------------------#
    # Fixtures - Events 
    #----------------------------------------------------------------------------#

    e0 = Event(
        name = 'test event 0',
        description = 'this is a test event',
        start_datetime = datetime(2021, 1, 12, 10, 0, 0),
        end_datetime = datetime(2021, 1, 12, 12, 0, 0),
        address = 'London SW1A 0AA, UK',
        organisation = org0,
        participants = [u0, u1]
    )
    e0.insert()

    e1 = Event(
        name = 'test event 1',
        description = 'this is a test event',
        start_datetime = datetime(2021, 1, 12, 17, 0, 0),
        end_datetime = datetime(2021, 1, 12, 18, 0, 0),
        address = 'London SW1A 0AA, UK',
        organisation = org1,
        participants = [u0]
    )
    e1.insert()

    e2 = Event(
        name = 'test event 2',
        description = 'this is a test event',
        start_datetime = datetime(2021, 3, 1, 10, 0, 0),
        end_datetime = datetime(2021, 3, 1, 12, 0, 0),
        address = 'London SW1A 0AA, UK',
        organisation = org2, 
        participants = [u1, u3]
    )
    e2.insert()

    e3 = Event(
        name = 'test event 3',
        description = 'this is a test event',
        start_datetime = datetime(2021, 4, 1, 10, 0, 0),
        end_datetime = datetime(2021, 4, 1, 12, 0, 0),
        address = 'London SW1A 0AA, UK',
        organisation = org2, 
        participants = [u0, u1, u3]
    )
    e3.insert()

    e4 = Event(
        name = 'test event 4',
        description = 'this is a test event',
        start_datetime = datetime(2021, 5, 1, 10, 0, 0),
        end_datetime = datetime(2021, 5, 1, 12, 0, 0),
        address = 'London SW1A 0AA, UK',
        organisation = org2, 
        participants = [u0, u2, u3]
    )
    e4.insert()

if __name__ == '__main__':
    #run python fixtures.py to populate test database
    app = Flask(__name__)
    db = setup_db(app)
    reset_db_with_fixtures(db)