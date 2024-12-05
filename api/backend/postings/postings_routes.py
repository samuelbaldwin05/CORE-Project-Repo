from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a Blueprint object for job postings
job_posting = Blueprint('job_posting', __name__)

########################################################
# Routes for JobPosting
########################################################

# Get all job postings
@job_posting.route('/JobPosting', methods=['GET'])
def get_all_job_postings():
    query = 'SELECT * FROM JobPosting'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data), 200

# Get job postings by PositionID
@job_posting.route('/JobPosting/<int:PositionID>', methods=['GET'])
def get_job_postings_by_position(PositionID):
    query = 'SELECT * FROM JobPosting WHERE PositionID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (PositionID,))
    data = cursor.fetchall()
    return jsonify(data), 200

# Add a new job posting
@job_posting.route('/JobPosting', methods=['POST'])
def add_new_job_posting():
    data = request.json
    query = '''
        INSERT INTO JobPosting (CompanyID, DatePosted, Status, PositionID)
        VALUES (%s, %s, %s, %s)
    '''
    params = (data['CompanyID'], data['DatePosted'], data['Status'], data['PositionID'])
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    return jsonify({'message': 'Job posting added successfully'}), 201

# Update a job posting
@job_posting.route('/JobPosting/<int:PostingID>', methods=['PUT'])
def update_job_posting(PostingID):
    data = request.json
    query = '''
        UPDATE JobPosting
        SET CompanyID = %s,
            DatePosted = %s,
            Status = %s,
            PositionID = %s
        WHERE PostingID = %s
    '''
    params = (data['CompanyID'], data['DatePosted'], data['Status'], data['PositionID'], PostingID)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    return jsonify({'message': f'Job posting with ID {PostingID} updated successfully'}), 200

# Delete a job posting
@job_posting.route('/JobPosting/<int:PostingID>', methods=['DELETE'])
def delete_job_posting(PostingID):
    query = 'DELETE FROM JobPosting WHERE PostingID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (PostingID,))
    db.get_db().commit()
    return jsonify({'message': f'Job posting with ID {PostingID} deleted successfully'}), 200

########################################################
# Routes for PostStats
########################################################

# Get all post stats
@job_posting.route('/PostStats', methods=['GET'])
def get_all_post_stats():
    query = 'SELECT * FROM PostStats'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data), 200

# Get post stats by PostingID
@job_posting.route('/PostStats/Posting/<int:PostingID>', methods=['GET'])
def get_post_stats_by_posting(PostingID):
    query = 'SELECT * FROM PostStats WHERE PostingID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (PostingID,))
    data = cursor.fetchall()
    return jsonify(data), 200

# Add new post stats
@job_posting.route('/PostStats', methods=['POST'])
def add_new_post_stats():
    data = request.json
    query = '''
        INSERT INTO PostStats (PostingID, AppAmount, InterviewAmount, OfferAmnt, AcceptAmnt, CallBackNum, MeanResponseTime)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    params = (data['PostingID'], data['AppAmount'], data['InterviewAmount'], data['OfferAmnt'], data['AcceptAmnt'], data['CallBackNum'], data['MeanResponseTime'])
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    return jsonify({'message': 'Post stats added successfully'}), 201

# Update post stats
@job_posting.route('/PostStats/<int:PostStatID>', methods=['PUT'])
def update_post_stats(PostStatID):
    data = request.json
    query = '''
        UPDATE PostStats
        SET AppAmount = %s,
            InterviewAmount = %s,
            OfferAmnt = %s,
            AcceptAmnt = %s,
            CallBackNum = %s,
            MeanResponseTime = %s
        WHERE PostStatID = %s
    '''
    params = (data['AppAmount'], data['InterviewAmount'], data['OfferAmnt'], data['AcceptAmnt'], data['CallBackNum'], data['MeanResponseTime'], PostStatID)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    return jsonify({'message': f'Post stats with ID {PostStatID} updated successfully'}), 200

# Delete post stats
@job_posting.route('/PostStats/<int:PostStatID>', methods=['DELETE'])
def delete_post_stats(PostStatID):
    query = 'DELETE FROM PostStats WHERE PostStatID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (PostStatID,))
    db.get_db().commit()
    return jsonify({'message': f'Post stats with ID {PostStatID} deleted successfully'}), 200
