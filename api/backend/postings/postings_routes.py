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
