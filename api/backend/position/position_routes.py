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

# fetch data based upon learning percent
@position.route('/Position/PosStats/Learning', methods=['GET'])
def get_positions_by_yield_rate():
    query = '''
        SELECT pt.*, pst.AvgLearning 
        FROM positiontable pt 
        JOIN positionstatstable pst 
        ON pt.position_id = pst.position_id 
        ORDER BY pst.AvgLearning
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

# fetch data based upon GPA
@position.route('/Position/PosStats/<gpa>', methods=['GET'])
def get_positions_by_yield_rate(gpa):
    query = f'''
        SELECT pt.*, pst.AvgGpa
        FROM positiontable pt 
        JOIN positionstatstable pst 
        ON pt.position_id = pst.position_id 
        WHERE pst.AvgGpa == {int(gpa)}
        ORDER BY pst.AvgGpa
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

@position.route('/position', methods=['POST'])
def add_new_product():
    #collecting the data 
    the_data = request.json
    current_app.logger.info(the_data)

    
    #extracting the variable
    name = the_data['PositionName']
    description = the_data['Description']
    skills = the_data['Skills']
    Environment = skills = the_data['Enviroment']
    questions = the_data['AdditionalQuestions']
    CoverLetter = the_data['CoverLetter']
    
    query = f'''
        INSERT INTO products (PositionName,
                              Description,
                              Skills,
                              Environment, 
                              AdditionalQuestions,
                              CoverLetter)
        VALUES ('{name}', '{description}', '{skills}', '{Environment}', '{questions}', '{CoverLetter}')
    '''

    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added product")
    response.status_code = 200
    return response

    ------------------------------------------------------------
# Update customer info for customer with particular userID
#   Notice the manner of constructing the query.
@position.route('/posstats/<PositionID>', methods=['PUT'])
def update_posstats(PositionID):
    current_app.logger.info('PUT /posstats route')
    
    # Get the JSON request payload
    stats_info = request.json
    position_id = PositionID
    app_count = stats_info['AppCount']
    interview_amount = stats_info['InterviewAmount']
    offer_amount = stats_info['OfferAmount']
    acceptance_amount = stats_info['AcceptanceAmount']
    callback_amount = stats_info['CallbackAmount']
    avg_response_time = stats_info['AvgResponseTime']
    
    # SQL query to update the PosStats table
    query = '''
        UPDATE PosStats
        SET AppCount = %s,
            InterviewAmount = %s,
            OfferAmount = %s,
            AcceptanceAmount = %s,
            CallbackAmount = %s,
            AvgResponseTime = %s
        WHERE PositionID = %s
    '''
    
    # Data tuple for query execution
    data = (app_count, interview_amount, offer_amount, acceptance_amount, callback_amount, avg_response_time, position_id)
    
    # Execute the query
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 
@position.route('/position/Remove/<PositionID>', methods=['DELETE'])
def remove_user(PositionID):
    query = f'''
        DELETE *
        FROM PositionTable
        WHERE PositionID = {PositionID}
    '''
    
    current_app.logger.info(f'DELETE /position/remove/<PositionID> query={query}')
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    current_app.logger.info(f'DELETE /postion/Remove/<PositionID> postiontable with ={PositionID} deleted')
    
    response = make_response(jsonify({'message': f'postiontable with ={PositionID} deleted'}))
    response.status_code = 200
    return response
    

