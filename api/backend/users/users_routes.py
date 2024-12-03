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
def get_advisor_students (id):

    query = f'''SELECT GPA, 
                       MajorID, 
                       description, 
                       list_price, 
                       category 
                FROM products 
                WHERE id = {str(id)}
    '''
    
    # logging the query for debugging purposes.  
    # The output will appear in the Docker logs output
    # This line has nothing to do with actually executing the query...
    # It is only for debugging purposes. 
    current_app.logger.info(f'GET /product/<id> query={query}')

    # get the database connection, execute the query, and 
    # fetch the results as a Python Dictionary
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    # Another example of logging for debugging purposes.
    # You can see if the data you're getting back is what you expect. 
    current_app.logger.info(f'GET /product/<id> Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response
    
# ------------------------------------------------------------
