from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
from datetime import timedelta
from flask import Response

# Create a Blueprint object for job postings
job_posting = Blueprint('job_posting', __name__)

########################################################
# Routes for JobPosting
########################################################

# Get all job postings 
@job_posting.route('/JobPosting', methods=['GET'])
def get_all_job_postings():
    query = '''SELECT jp.*, pt.PositionName 
        FROM JobPosting jp
        JOIN PositionTable pt ON jp.PositionID = pt.PositionID
        '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data), 200

# Get all job posting info including PostionName and PostStats
@job_posting.route('/Info', methods=['GET'])
def get_all_job_posting_info():
    query = '''SELECT c.Name, pt.PositionName, jp.*, ps.AvgGpa, ps.YieldRate, ps.AvgAppAmount, ps.AvgLearning, ps.AvgEnvironment
        FROM Company c
        JOIN JobPosting jp ON c.CompanyID = jp.CompanyID
        JOIN PositionTable pt ON jp.PositionID = pt.PositionID
        JOIN PosStats ps on pt.PositionID = ps.PositionID
        WHERE jp.Status = 1'''
    cursor = db.get_db().cursor()
    cursor.execute(query)
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
    return Response(status=204)

# Update a job posting
@job_posting.route('/JobPosting/<int:PostingID>', methods=['PUT'])
def update_job_posting(PostingID):
    data = request.json
    query = '''
        UPDATE JobPosting
        SET Status = %s
        WHERE PostingID = %s
    '''
    params = (data['Status'], PostingID)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    return Response(status=204)

# Delete a job posting
@job_posting.route('/JobPosting/<int:PostingID>', methods=['DELETE'])
def delete_job_posting(PostingID):
    query = 'DELETE FROM JobPosting WHERE PostingID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (PostingID,))
    db.get_db().commit()
    return jsonify({'message': f'Job posting with ID {PostingID} deleted successfully'}), 200