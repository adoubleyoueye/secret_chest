# Secret Chest - One time dead letter box. 

Stop sending sensitive information in emails. Send a one-time encrypted, password protected note instead.

## Interaction Flow CRUD
1. Create message (request body): POST ​/message​/
```
{
  "text": "Between me and you, pineapples don't belong on pizza."
}
```
2. Retrieve message location(message id) and password (response body)
```
{
  "Location": "https://0.0.0.0:8099/5f5fe721-b42e-48be-834a-1f3696f496bd",
  "Password": "UnzuNqji2UtozaxPj_HAZEDopwjoeDbMY0D-BCIkR4Q="
}
```
3.  Retrieve message (request body): POST /message/{id}
```
{
  "password": "UnzuNqji2UtozaxPj_HAZEDopwjoeDbMY0D-BCIkR4Q="
}
```
4. Delete and Read decrypted message (response body)
```
"Between me and you, pineapples don't belong on pizza."
```

## Getting started

### Installing Dependencies

clone repo
cd repo
pip install -r requirements.txt

### Configuring Environment Variables
export DEBUG_MODE=True
export DB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"
export DB_NAME="<db_name>"
e
Once everything is installed and configured, run the server with python main.py and visit http://localhost:8000/docs

You'll notice that the interactive documentation is automatically generated for us by FastAPI. 
The primary elements of the application are covered in the interactive documentation, that is, creating a message (encrypt) and revealing a message (decrypt). Try it out and explore the responses you get back from the FastAPI server.

## App Structure

```
📦apps
 ┣ 📂message
 ┃ ┣ 📜models.py
 ┃ ┗ 📜routers.py
 ┗ 📜__init__.py
  📜__init__.py
  📜 main.py
```