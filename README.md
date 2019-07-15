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
  - routes are added to routes.py, inside the setup_routes function, ex. app.add_get("/", coro_handler)
  - The handler must be an async method or function
  - If the API is small or isn't linked to a domain you can just use functions
  - You can pass dependencies to the handler inside setup_usecases, ex. app["usecase_name"] = usecase
- Unit testing
  - If you're not comfortable with TDD then you need to write more acceptance test cases to cover regression
  - I've used the London-style of TDD in which you mock all of the collaborators of the system under test
  - You are free to use any style you wish for unit testing (as long as it doesn't break other tests)
- Run all tests as much as possible

  
