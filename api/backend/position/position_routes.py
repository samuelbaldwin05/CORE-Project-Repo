########################################################
# Routes for Position blueprint
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint object for position-related routes
position = Blueprint('position', __name__)

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

@position.route('/PositionReview/<int:PositionID>', methods=['GET'])
def get_reviews_by_position(PositionID):
    query = '''
        SELECT *
        FROM PositionReview
        WHERE PositionID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (PositionID,))
    reviews = cursor.fetchall()
    return jsonify(reviews), 200

# creating a new route for a specific position
@position.route('/PositionReview/<int:PositionID>', methods=['POST'])
def add_review(PositionID):
    data = request.json  # Expecting JSON input
    query = '''
        INSERT INTO PositionReview (
            Description, Offer, ApplicationRating, EnvironmentRating,
            EducationRating, ProfessionalRating, Applied, AppliedDate,
            ResponseDate, PositionID
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (
        data['Description'], data['Offer'], data['ApplicationRating'],
        data['EnvironmentRating'], data['EducationRating'], 
        data['ProfessionalRating'], data['Applied'], data['AppliedDate'],
        data['ResponseDate'], PositionID
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    return jsonify({'message': 'Review added successfully'}), 201

# deleting reviews
@position.route('/PositionReview/<int:PosReviewID>', methods=['DELETE'])
def delete_review(PosReviewID):
    query = '''
        DELETE FROM PositionReview
        WHERE PosReviewID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (PosReviewID,))
    db.get_db().commit()
    return jsonify({'message': f'Review with ID {PosReviewID} deleted successfully'}), 200

# position based on major
@position.route('/positions/related_majors/<int:major_id>', methods=['GET'])
def get_positions_by_related_majors(major_id):
    query = '''
        SELECT DISTINCT 
            pt.PositionID, pt.PositionName, pt.Description
        FROM 
            Majors m
        INNER JOIN 
            Users u ON m.MajorID = u.MajorID
        INNER JOIN 
            PositionReview pr ON pr.PositionID = u.PositionId
        INNER JOIN 
            PositionTable pt ON pt.PositionID = pr.PositionID
        WHERE 
            m.MajorID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (major_id,))
    positions = cursor.fetchall()

    return jsonify(positions), 200
