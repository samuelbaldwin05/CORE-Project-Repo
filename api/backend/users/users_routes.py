########################################################
# Routes for Users blueprint
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
users = Blueprint('users', __name__)

# ------------------------------------------------------------
# GET user information for a particular advisor

@users.route('/advisor/<id>', methods=['GET'])
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
    
    current_app.logger.info(f'GET /users/<id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /users/<id> Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response
    
# ------------------------------------------------------------
