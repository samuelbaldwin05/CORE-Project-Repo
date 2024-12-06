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

# Create a new Blueprint object, which is a collection of 
# routes.
users = Blueprint('users', __name__)

# Route for all user data
@users.route('/users', methods=['GET'])
def get_users():

    query = f'''SELECT *
                FROM Users;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall() 
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Route for all user information
@users.route('/users/info', methods=['GET'])
def get_user_info():

    query = f'''SELECT *
                FROM Users u
                JOIN Advisor a on u.AdvisorId = a.AdvisorID
                JOIN Majors m on u.MajorID = m.MajorID
                JOIN College c on m.CollegeID = m.CollegeID;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall() 
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


# GET route for Persona2, retrieves student data under specfic advisor
@users.route('/users/<int:advisorid>', methods=['GET'])
def view_student_data_advisorid(advisorid):
    # Parameterized query to avoid SQL injection
    query = '''
        SELECT Username,
               MajorID, 
               GPA, 
               AppCount, 
               OfferCount, 
               NUID
        FROM Users 
        WHERE AdvisorId = %s
    '''
    
    current_app.logger.info(f'GET /users/{advisorid} query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query, (advisorid,))
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /users/{advisorid} Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

    
# ------------------------------------------------------------

# GET Route for all Personas, retrieves student data under specifc NUID

@users.route('/users/<nuid>', methods=['GET'])
def view_student_data (NUID):

    query = f'''SELECT Username,
                       GPA, 
                       MajorID, 
                       AppCount, 
                       OfferCount, 
                       NUID
                        
                FROM Users 
                WHERE NUID = {str(NUID)}
    '''
    
    current_app.logger.info(f'GET /users/<nuid> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /user/<nuid> Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# ------------------------------------------------------------

# PUT Route for Persona 2, allows advisor to update Users GPA

@users.route('/users/<nuid>/update_gpa', methods=['PUT'])

def update_user_gpa(NUID):
    data = request.get_json()
    gpa = data['gpa']
    
    query = f'''
        UPDATE Users
        SET GPA = {str(gpa)}
        WHERE NUID = {str(NUID)}
    '''
    
    current_app.logger.info(f'PUT /users/<nuid>/update_gpa query={query}')
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    current_app.logger.info(f'PUT /users/<nuid>/update_gpa GPA updated for NUID = {NUID}')
    
    response = make_response(jsonify({'message': f'GPA for user {NUID} updated to {gpa}'}))
    response.status_code = 200
    return response

# ------------------------------------------------------------

# POST Route for Persona 4, allows advisor to insert new student they are advising

@users.route('/users/add_user/<int:advisorid>', methods=['POST'])
def add_new_user(AdvisorID):
    
    the_data = request.get_json()
    current_app.logger.info(the_data)
    username = the_data['username']
    major_id = the_data['major_id']
    gpa = the_data['gpa']
    advisor_id = AdvisorID
    app_count = the_data.get('app_count', 0)  
    offer_count = the_data.get('offer_count', 0)  
    previous_count = the_data.get('previous_count', 0)  
    nuid = the_data['nuid']

    query = f'''
        INSERT INTO Users (NUID, Username, MajorID, 
                            GPA, AdvisorId, AppCount, 
                            OfferCount, PreviousCount)
        VALUES ('{username}', '{major_id}', '{gpa}', '{advisor_id}',
                '{app_count}', '{offer_count}', '{previous_count}',
                '{nuid}')
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added User")
    response.status_code = 200
    return response

# ------------------------------------------------------------

# DELETE Route for Persona 4, allows system administrator to remove users

@users.route('/deleteusers/<int:nuid>', methods=['DELETE'])
def remove_user(nuid):
    query = f'''
        DELETE FROM Users
        WHERE NUID = {nuid}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return jsonify({'message': f'User with NUID {nuid} successfully removed'}), 200

# ------------------------------------------------------------

# GET Route for Persona 3, retrieves all reviews written by a given user

@users.route('/users/<nuid>/reviews', methods=['GET'])
def get_user_reviews(nuid):

    position_reviews_query = f'''
        SELECT pr.PosReviewID, 
               pt.PositionName, 
               pr.EnvironmentRating
        FROM PositionReviewers prr
        JOIN PositionReview pr ON prr.PosReviewID = pr.PosReviewID
        JOIN PositionTable pt ON pr.PositionID = pt.PositionID
        WHERE prr.NUID = {str(nuid)}
    '''
    
    company_reviews_query = f'''
        SELECT cr.ComReviewID, 
               c.Name AS CompanyName, 
               cr.EnvironmentRating
        FROM CompanyReviewers crr
        JOIN CompanyReview cr ON crr.ComReviewID = cr.ComReviewID
        JOIN Company c ON cr.CompanyId = c.CompanyID
        WHERE crr.NUID = {str(nuid)}
    '''

    current_app.logger.info(f'GET /users/<nuid>/reviews Position Reviews Query: {position_reviews_query}')
    current_app.logger.info(f'GET /users/<nuid>/reviews Company Reviews Query: {company_reviews_query}')
    
    cursor = db.get_db().cursor()
    cursor.execute(position_reviews_query)
    position_reviews = cursor.fetchall()
    
    cursor.execute(company_reviews_query)
    company_reviews = cursor.fetchall()
    
    current_app.logger.info(f'GET /users/<nuid>/reviews Position Reviews Result: {position_reviews}')
    current_app.logger.info(f'GET /users/<nuid>/reviews Company Reviews Result: {company_reviews}')
    
    response_data = {
        "position_reviews": [
            {
                "review_id": row[0], 
                "position_name": row[1], 
                "environment_rating": row[2]
            }
            for row in position_reviews
        ],
        "company_reviews": [
            {
                "review_id": row[0], 
                "company_name": row[1], 
                "environment_rating": row[2]
            }
            for row in company_reviews
        ]
    }
    
    response = make_response(jsonify(response_data))
    response.status_code = 200
    return response

# ------------------------------------------------------------

# PUT Route for Cammy, allows advisor to update Users GPA

@users.route('/user/add', methods=['POST'])
def add_new_position():
    data = request.json
    current_app.logger.info(data)

    query = '''
        INSERT INTO Users (NUID, Username, MajorID, GPA, AdvisorId, AppCount, OfferCount, PreviousCount)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (data['NUID'], data['Username'], data['MajorID'], data['GPA'],
               data['AdvisorId'], data['AppCount'], data['OfferCount'], data['PreviousCount'])
    
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    return jsonify({'message': 'User added successfully'}), 200