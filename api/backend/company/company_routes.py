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

    return response

@company.route('/Company/info', methods=['GET'])
def get_company_info():
    query = f'''
        SELECT c.CompanyID, c.Name AS CompanyName, c.Industry, c.CompanySize, l.State, l.City, l.CountryCode, l.Address, 
        cr.ComReviewID, cr.Type AS ReviewType, cr.Description AS ReviewDescription, cr.EnvironmentRating, cr.CultureRating, 
        u.NUID AS ReviewerNUID, u.Username AS ReviewerUsername
        FROM Company c
        INNER JOIN Location l ON c.LocationId = l.LocationId
        LEFT JOIN CompanyReview cr ON c.CompanyID = cr.CompanyId
        LEFT JOIN CompanyReviewers crv ON cr.ComReviewID = crv.ComReviewID
        LEFT JOIN Users u ON crv.NUID = u.NUID;
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
@company.route('/Company/<int:CompanyID>', methods=['PUT'])
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

# Get all company reviews
@company.route('/CompanyReview', methods=['GET'])
def get_all_company_reviews():
    query = f'''
        SELECT * 
        FROM CompanyReview cr
        LEFT JOIN CompanyReviewers crr ON cr.ComReviewID = crr.ComReviewID
        LEFT JOIN Users u ON crr.NUID = u.NUID;
    '''
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for reviews
    cursor.execute(query)

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it after "jsonify"-ing it.
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Delete Company
@company.route('/Company/<int:CompanyID>', methods=['DELETE'])
def delete_company(CompanyID):
    query = f'''
        DELETE FROM Company
        WHERE CompanyID = {CompanyID}
    '''
    current_app.logger.info(query)

    # executing and committing the delete statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return jsonify({'message': f'Position with ID {CompanyID} deleted successfully.'}), 200

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
@company.route('/CompanyReview/<int:ComReviewID>', methods=['DELETE'])
def delete_company_review(ComReviewID):
    query = f'''
        DELETE FROM CompanyReview 
        WHERE ComReviewId = {ComReviewID}
    '''
    current_app.logger.info(query)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return jsonify({'message': f'Position with ID {ComReviewID} deleted successfully.'}), 200

@company.route('/Company/stats', methods=['GET'])
def get_average_company_stats():
    """
    Get averaged stats grouped by company from CompanyReview and Company tables.
    Returns:
        JSON response with averaged stats grouped by company.
    """
    query = """
        SELECT 
            c.CompanyID,
            c.Name AS CompanyName,
            c.Industry,
            c.CompanySize,
            AVG(cr.EnvironmentRating) AS AvgEnvironmentRating,
            AVG(cr.CultureRating) AS AvgCultureRating,
            COUNT(cr.ComReviewID) AS TotalReviews
        FROM Company c
        LEFT JOIN CompanyReview cr ON c.CompanyID = cr.CompanyId
        GROUP BY c.CompanyID, c.Name, c.Industry, c.CompanySize
    """
    cursor = db.get_db().cursor()

    # use cursor to query the database for companies by city
    cursor.execute(query)
    results = cursor.fetchall()
    return jsonify(results), 200

