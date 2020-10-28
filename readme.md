1. create a virtual environment named venv   
`python -m venv venv`
2. activate the virtual environment  
on windows:
`venv\Scripts\activate.bat`  
on unix or macos:
`source venv/bin/activate`
3. install dependencies  
`pip install -r requirements.txt`
4. start the server  
`flask run`  
view the application via: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)