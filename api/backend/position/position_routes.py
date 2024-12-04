from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint object for position-related routes
position = Blueprint('position', __name__)

########################################################
# Routes for Position Blueprint
########################################################

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
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data), 200

# ------------------------------------------------------------
# Get positions ordered by average learning percentage
@position.route('/Position/PosStats/Learning', methods=['GET'])
def get_positions_by_learning():
    query = '''
        SELECT pt.*, pst.AvgLearning 
        FROM positiontable pt 
        JOIN positionstatstable pst 
        ON pt.position_id = pst.position_id 
        ORDER BY pst.AvgLearning
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data), 200

# ------------------------------------------------------------
# Get positions filtered by GPA
@position.route('/Position/PosStats/<int:gpa>', methods=['GET'])
def get_positions_by_gpa(gpa):
    query = '''
        SELECT pt.*, pst.AvgGpa
        FROM positiontable pt 
        JOIN positionstatstable pst 
        ON pt.position_id = pst.position_id 
        WHERE pst.AvgGpa = %s
        ORDER BY pst.AvgGpa
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (gpa,))
    data = cursor.fetchall()
    return jsonify(data), 200

# ------------------------------------------------------------
# Add a new position to the PositionTable
@position.route('/position', methods=['POST'])
def add_new_position():
    data = request.json
    current_app.logger.info(data)

    query = '''
        INSERT INTO PositionTable (PositionName, Description, Skills, Environment, AdditionalQuestions, CoverLetter)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    params = (data['PositionName'], data['Description'], data['Skills'], data['Environment'], data['AdditionalQuestions'], data['CoverLetter'])
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    return jsonify({'message': 'Position added successfully'}), 201

# ------------------------------------------------------------
# Update position stats for a specific PositionID
@position.route('/posstats/<int:PositionID>', methods=['PUT'])
def update_posstats(PositionID):
    data = request.json
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
    params = (data['AppCount'], data['InterviewAmount'], data['OfferAmount'], data['AcceptanceAmount'], data['CallbackAmount'], data['AvgResponseTime'], PositionID)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    return jsonify({'message': f'Position stats for PositionID {PositionID} updated successfully.'}), 200

# ------------------------------------------------------------
# Remove a position from the PositionTable
@position.route('/position/Remove/<int:PositionID>', methods=['DELETE'])
def remove_position(PositionID):
    query = 'DELETE FROM PositionTable WHERE PositionID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (PositionID,))
    db.get_db().commit()
    return jsonify({'message': f'Position with ID {PositionID} deleted successfully.'}), 200

# ------------------------------------------------------------
