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
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
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
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
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
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    
    return response


# Get all company data
@company.route('/Company', methods=['GET'])
def get_all_companies():
    query = f'''
        SELECT *
        FROM Company
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    
    return response

# Create new company review
@company.route('/CompanyReview', methods=['POST'])
def add_com_review():
    data = request.json  # Expecting JSON input
    query = '''
        INSERT INTO CompanyReview (
            CompanyId, Type, Description, EnvironmentRating,
            CultureRating
        )
        VALUES (%s, %s, %s, %s, %s)
    '''
    params = (
        data['CompanyId'], data['Type'], data['Description'],
        data['EnvironmentRating'], data['CultureRating']
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    
    return jsonify({'message': 'Review added successfully'}), 200

# Update company name
@company.route('/Company/int<CompanyID>', methods=['PUT'])
def update_company_name(CompanyID):
    data = request.json
    query = '''
        UPDATE Company
        SET Name = %s
        WHERE CompanyID = %s
    '''
    params = (data['Name'], CompanyID)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    
    return jsonify({'message': f'Company name for CompanyID {CompanyID} updated successfully.'}), 200


# Get all reviews for a company
@company.route('/CompanyReview/<CompanyID>', methods=['GET'])
def get_company_reviews(CompanyID):
    query = f'''
        SELECT * FROM company_review WHERE company_id = {CompanyID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    
    return response

# Add a new review for a company
@company.route('/CompanyReview/<CompanyID>', methods=['POST'])
def add_company_review(CompanyID):
    the_data = request.json
    current_app.logger.info(the_data)
    review_type = the_data['Type']
    description = the_data['Description']
    environment_rating = the_data['EnvironmentRating']
    culture_rating = the_data['CultureRating']
    
    query = f'''
        INSERT INTO company_review (company_id, type, description, environment_rating, culture_rating)
        VALUES ({CompanyID}, '{review_type}', '{description}', {environment_rating}, {culture_rating})
    '''
    current_app.logger.info(query)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()  
    response = make_response("Successfully added review")
    response.status_code = 200
    
    return response

# Delete a review by ComReviewID
@company.route('/CompanyReview/<ComReviewID>', methods=['DELETE'])
def delete_company_review(ComReviewID):
    query = f'''
        DELETE FROM company_review WHERE com_review_id = {ComReviewID}
    '''
    current_app.logger.info(query)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    response = make_response("Successfully deleted review")
    response.status_code = 200
    
    return response