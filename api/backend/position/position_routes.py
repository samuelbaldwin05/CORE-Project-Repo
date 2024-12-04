########################################################
# Routes for Position blueprint
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
position = Blueprint('position', __name__)

# ------------------------------------------------------------

# ------------------------------------------------------------

# Get positions ordered by yield rate
@position.route('/Position/PosStats/YieldRate', methods=['GET'])
def get_positions_by_yield_rate():
    query = '''
        SELECT pt.*, pst.yield_rate 
        FROM positiontable pt 
        JOIN positionstatstable pst 
        ON pt.position_id = pst.position_id 
        ORDER BY pst.yield_rate
    '''
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for positions ordered by yield rate
    cursor.execute(query)

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it after "jsonify"-ing it.
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response