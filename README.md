# Learning Hub API

Open Source Project with Chingu

Project Setup
-------------
Get the latest version of Python: 3.7

In the project root, run these commands to setup the virtual environment:

- virtualenv venv
- .\venv\Scripts\activate
- pip install -r requirements.txt

To run all tests, use this commands:
- pytest 

# Contributing to Learning Hub API
- Checkout a new feature branch: git checkout -b feature-branch-name
- Write an acceptance test
  - Create a new file with the name of the feature you are writing, ex. test_create_learning_path.py
  - Use the aiohttp test client for blackbox testing. https://aiohttp.readthedocs.io/en/stable/testing.html#pytest
- Add a route
  - routes are added to routes.py, inside the setup_routes function. ex. app.add_get("/", coro_handler)
  - The handler must be an async method or function
  - If the api is very simple you can use functions.
  - You can pass dependencies through the app, using the setup_usecases ex. app["usecase_name"] = usecase
- Unit testing
  - If you're not comfortable with TDD then you need to write more acceptance test cases to cover the regression
  - I've used the London-style of TDD which uses mocking for all of the collaborators of the system under test. 
  - You are free to use any style you wish for unit testing.
- Creating a Usecase
  - The usecase is the core of the feature you are adding. 
  - The API handler should parse all relevant information and then delegate to the usecase via a use case request.
  - The use case should have an execute method that accepts the use case request and returns a usecase response.
  - The request and response should be frozen dataclasses which are immutable.
  - Use an in memory repository for testing, but be sure to add methods to an interface. Check to see if an interface or repository already exists.
- Run all tests

  
