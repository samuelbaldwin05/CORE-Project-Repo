########################################################
# Routes for Company blueprint
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
company = Blueprint('company', __name__)

#------------------------------------------------------------

# Get companies ordered by average culture rating
@company.route('/Company/CultureRating', methods=['GET'])
def get_companies_by_culture_rating():
    query = '''
        SELECT c.company_id, c.company_name, AVG(cr.culture_rating) AS avg_culture_rating
        FROM company c
        JOIN company_review cr ON c.company_id = cr.company_id
        GROUP BY c.company_id, c.company_name
        ORDER BY avg_culture_rating DESC
    '''
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for companies ordered by average culture rating
    cursor.execute(query)

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it after "jsonify"-ing it.
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get companies by industry
@company.route('/Company/<Industry>', methods=['GET'])
def get_companies_by_industry(Industry):
    query = f'''
        SELECT * FROM company
        WHERE industry = '{Industry}'
    '''
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for companies by industry
    cursor.execute(query)

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it after "jsonify"-ing it.
    response = make_response(jsonify(theData))
    response.status_code = 200

# Get companies by city
@company.route('/Company/Location/<City>', methods=['GET'])
def get_companies_by_city(City):
    query = f'''
        SELECT c.*
        FROM company c
        JOIN location l ON c.locationid = l.locationid
        WHERE l.city = '{City}'
    '''
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for companies by city
    cursor.execute(query)

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it after "jsonify"-ing it.
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


# Get all company data
@company.route('/Company', methods=['GET'])
def get_companies_by_city():
    query = f'''
        SELECT *
        FROM Company'
    '''
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for companies by city
    cursor.execute(query)

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it after "jsonify"-ing it.
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response