# Trivia App

## Trivia App

Trivia app allow Udacity's employees and students to play trivia game and connect with each other.

## API Description:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions - text and answer is required.
4. Search for questions based on a text query string.
5. Play the quiz game, all questions or within a specific category.


## Local Requirements
Required software:

#### Python 3.7 
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment 
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Postgres
If you don't already have it installed, see installation instructions for your operating system here:[PostgreSQL Downloads] (https://www.jetbrains.com/datagrip/features/postgresql/?msclkid=ced27949b01317887af21fddb9f49998&utm_source=bing&utm_medium=cpc&utm_campaign=EMEA_en_GB_DataGrip_Search&utm_term=postgres&utm_content=postgres)

## Set up and populate local Database
With Postgres running, create a trivia database:
```bash
create database trivia;
```

Populate the database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Initialize and activate a virtual environment using:
```bash
python -m virtualenv env
.\env\Scripts\activate.bat
```

## Install Dependencies
Navigate to backedn directory and install required dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Key Dependencies
- [Flask](http://flask.pocoo.org/) is a lightweight backend micro-services framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

Step 3: Start the Server
In the backend directory, start the Flask server by running:
```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
python -m flask run
```

## FrontEnd Instructions

1. Install Node and NPM This project requires on Nodejs and Node Package Manager (NPM). If you haven't already installed Node on your local machine, see the instructions here: Before continuing, you must download and install Node (the download includes NPM) from Nodejs.com(opens in a new tab).
2. Install project dependencies After confirming you have NPM installed, navigate to the frontend directory of the project and run:
```bash
npm install
```

3. To start the app in development mode, run:
```bash
npm start
```

Open (opens in a new tab)http://localhost:3000(opens in a new tab) to view it in the browser. The page will reload if you make edits.

# Endpoints

### GET '/categories'

- Retrieve categories
- Request Arguments: None
- Returns list of categories

Example: curl http://localhost:5000/categories
```bash
{
    'categories': { 
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'success': true
}
```

### GET '/questions?page=${integer}'

- Retrieve paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

Example: curl http://127.0.0.1:5000/questions?page=2
```bash
{
    'categories': [ 
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports" 
    ],
    'currentCategory': null,
    'questions': [
        {
            'answer': 'This is an answer',
            'category': 2,
            'difficulty': 5,
            'id': 1,
            'question': 'This is a question'
        },
    ],
    'success': true,
    'totalQuestions': 100   
}
```

### GET '/categories/${id}/questions'

- Retrieve questions for a category specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string

Example: `curl http://localhost:5000/categories/1/questions`
```bash
{
    'categories': [ 
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports" 
    ],
    'current_category': {
    'id': 1,
    'type': 'Science'},
    'questions': [
        {
            'answer': 'This is an answer',
            'category': 4,
            'difficulty': 5,
            'id': 1,
            'question': 'This is a question',
        },
    ],
    'success': true,
    'totalQuestions': 100
}
```

### DELETE '/questions/${id}'

-Deletes a specified question using the id of the question
-Request Arguments: id - integer
-Returns JSON object with deleted question and number of total questions remaining

Example: `curl -X DELETE http://localhost:5000/questions/2`
```bash
{
    'deleted_question': {
        'answer': 'Tom Cruise',
        'category': 5,
        'difficulty': 4,
        'id': 4,
        'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?'},
    'success': true,
    'total_questions': 32
}
```

### POST '/quizzes'

- Sends a post request in order to get question based on category or a random selection depending on what user chooses.
- Returns random question

Example: curl http://localhost:5000/quizzes -X POST -H "Content-Type: application/json" -d "{\"previous_questions\":[], \"quiz_category\":{\"type\":\"Art\",\"id\":2}}"
```bash
{
  "question": {
    "answer": "One", 
    "category": 2, 
    "difficulty": 4, 
    "id": 18, 
    "question": "How many paintings did Van Gogh sell in his lifetime?"}, 
  "success": true
}
```

### POST '/questions'

- Sends a post request in order to create a new question
- Fileds required: question, answer, difficulty and category
- Return success if question added successfully and returns the question added and total number of questions

Example: curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d "{\"question\":\"What is the capital of France?\", \"answer\":\"Paris\", \"category\":\"4\", \"difficulty\":\"2\"}"
```bash
{
    'created': 24,
    'created_question': {
    'answer': 'Answer',
    'category': 4,
    'difficulty': 2,
    'id': 32,
    'question': 'Question?'},
    'success': true, 
    'total_questions': 35
}
```

### POST '/questions/search'

- Sends a post request in order to search for a specific question by search term
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

Example: curl http://localhost:5000/questions/search -X POST -H "Content-Type: application/json" -d "{\"searchTerm\":\"One\"}"
```bash
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}
```

## Error Handlers

When an error occurs a JSON response is returned
- Returns these error types when the request fails
	- 400: Bad Request
	- 404: Resource Not Found
	- 422: Not Processable
	- 500: Internal Server Error
Example "Resource Not Found":
```bash
{
	"success": False,
	"error": 404,
	"message": "Resource Not Found"
}
```

## Testing

To run the tests

Start local postgres and run this commands to created database for testing:
```bash
drop database trivia_test;
create database trivia_test;
```
In terminal run this commands to populate DB and to perform tests:
```bash
psql trivia_test < trivia.psql
python test_flaskr.py
```