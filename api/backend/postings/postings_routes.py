########################################################
# Routes for Postings blueprint
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
postings = Blueprint('postings', __name__)

# Get all reviews for a company
@postings.route('/CompanyReview/<CompanyID>', methods=['GET'])
def get_company_reviews(CompanyID):
    query = f'''
        SELECT * FROM CompanyReview WHERE CompanyID = {CompanyID}
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

# Add a new review for a company
@postings.route('/CompanyReview/<CompanyID>', methods=['POST'])
def add_company_review(CompanyID):
    # In a POST request, there is a collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    # extracting the variable
    review_type = the_data['Type']
    description = the_data['Description']
    environment_rating = the_data['EnvironmentRating']
    culture_rating = the_data['CultureRating']
    
    query = f'''
        INSERT INTO CompanyReview (CompanyID, Type, Description, EnvironmentRating, CultureRating)
        VALUES ({CompanyID}, '{review_type}', '{description}', {environment_rating}, {culture_rating})
    '''
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added review")
    response.status_code = 200
    return response

# Delete a review by ComReviewID
@postings.route('/CompanyReview/<ComReviewID>', methods=['DELETE'])
def delete_company_review(ComReviewID):
    query = f'''
        DELETE FROM CompanyReview WHERE ComReviewID = {ComReviewID}
    '''
    current_app.logger.info(query)

    # executing and committing the delete statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully deleted review")
    response.status_code = 200
    return response
#------------------------------------------------------------

@persona2.route('/persona2/<id>', methods=['GET'])
def view_student_data (id):

    query = f'''SELECT Username,
                       GPA, 
                       MajorID, 
                       AppCount, 
                       OfferCount, 
                       NUID
                        
                FROM Users 
                WHERE AdvisorId = {str(id)}
    '''
    
    current_app.logger.info(f'GET /persona2/<id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /persona2/<id> Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


