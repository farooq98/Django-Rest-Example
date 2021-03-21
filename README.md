# Django-Rest-Example

It is a simple django rest project, it is available on http://farooqhidayat.pythonanywhere.com <br/>

Only GET request /api/test -----> Response List of Objects <br/>
Both GET and POST requests /api/test/create <br/>
GET Response List of Objects <br/>
POST Response Posted Object <br/>
Send Email: POST request /api/test/sendemail -----> JSON Payload { "email": "email@email.com" } or { "email": ["email_1@email.com", "email_2@email.com"] } <br/>
Response : { "send": true, "message": "success" } or { "sent": false, "message": "error message" }


# Note:
After Cloning the Project <br/>
Create environment.py file inside the /myproject/myproject/ <br/>

and copy these statements <br/>

ENV = "DEV" <br/>

ALLOWED_HOSTS = [] <br/>

SECRET_KEY = "mysecretkey" <br/>

TIME_ZONE = 'UTC' <br/>
