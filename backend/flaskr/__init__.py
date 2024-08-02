import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

#Variable initialization
QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)
    CORS(app, resources={r"/api/*": {"origins": '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type,Authorization,true")
        response.headers.add(
            'Access-Control-Allow-Headers',
            'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add(
            "Access-Control-Allow-Origin",
            "*")
        return response

    # GET request for all available categories.
    @app.route("/categories", methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            if len(categories) == 0:
                abort(400)

            categories = {category.id: category.type for category in categories}
            
            return jsonify({
                "success": True,
                "categories": categories
            })
        except Exception as e:
            print(e)
            abort(422)

    # Pagination
    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions
    
    # GET requests for questions
    @app.route("/questions", methods=['GET'])
    def get_questions():
        try:
            questions = Question.query.all()
            categories = Category.query.all()
            current_category = {
                category.id: category.type for category in categories}
            questions_list = paginate_questions(request, questions)

            if len(questions_list) == 0:
                abort(404)

            categories = [category.type for category in categories]

            return jsonify({
                "success": True,
                "questions": questions_list,
                "total_questions": len(questions),
                "categories": categories,
                "current_category": current_category,
            }), 200
        
        except Exception as e:
            print(e)
            abort(422)

    # DELETE question using a question ID.
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question_to_delete = Question.query.get(question_id)

            if question_to_delete is None:
                abort(404)

            deleted_question = question_to_delete
            question_to_delete.delete()
            questions = Question.query.order_by(Question.id).all()

            return jsonify({
                "success": True,
                "deleted_id": question_id,
                "deleted_question": deleted_question.format(),
                "total_questions": len(questions),
            })
        
        except Exception as e:
            print(e)
            abort(422)

    # POST a new question
    # require: question, answer, category, difficulty score
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')

        try:
            if not new_question:
                abort(422)
            elif not new_answer:
                abort(422)
            elif not new_difficulty:
                abort(422)
            else:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty
                    )
                question.insert()
                questions = Question.query.all()

                return jsonify({
                    "success": True,
                    "created": question.id,
                    "created_question": question.format(),
                    "total_questions": len(questions),
                    })
        except Exception as e:
            print(e)
            abort(422)

    # Endpoint to get questions based on a search term.
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        if not search_term:
            abort(404)
        else:
            try:
                results = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')).all()
                formatted = paginate_questions(request, results)
                return jsonify({
                    "success": True,
                    "questions": formatted,
                    "total_questions": len(results)
                    })
            except Exception as e:
                print(e)
                abort(422)

    # Endpoint to get questions based on category.
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            category = Category.query.get(category_id)
            
            if category is None:
                abort(404)

            questions = Question.query.filter(Question.category == (category_id)).all()

            if len(questions) == 0:
                abort(404)

            current_questions = paginate_questions(request, questions)
            categories = Category.query.all()
            categories = {
                category.id: category.type for category in categories}
            
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "categories": categories,
                "current_category":  category.format(),
                })
        except Exception as e:
            print(e)
            abort(404)

    # Get questions to play the quiz.
    # Takes category and previous question parameters
    # Returns a random questions within the given category
    # Don't return one of the previous questions

    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')
            quiz_cat_id = quiz_category['id']

            if quiz_category is None and previous_questions is None:
                abort(400)

            if quiz_cat_id == 0:

                if len(previous_questions) == 0:
                    questions = Question.query.all()
                else:
                    questions = Question.query.filter(
                        Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(
                    Question.category == quiz_cat_id, 
                    Question.id.notin_(previous_questions)).all()

            if len(questions) is None:
                question = None
            else:
                question = random.choice(questions)

                return jsonify({
                    'success': True,
                    'question': question.format(),
                    'total_questions': len(questions)
                    })
        except Exception as e:
            print(e)
            abort(422)

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessed(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Request Cannot Be Processed"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Not Allowed"
        }), 500

    return app
