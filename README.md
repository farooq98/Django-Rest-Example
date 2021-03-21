# Django-Rest-Example

It is a simple django rest project, it is available on http://farooqhidayat.pythonanywhere.com <br/>

Only GET request /api/test -----> Response List of Objects <br/>
Both GET and POST requests /api/test/create <br/>
<ul>
  <li>GET Response List of Objects</li>
  <li>POST Response Posted Object<li>
</ul>
Send Email: POST request /api/test/sendemail <br/> 
JSON Payload: 
<ul>
  <li>{ "email": "email@email.com" }</l1> 
  <li>{ "email": ["email_1@email.com", "email_2@email.com"] } </li>
</ul>
Response: 
<ul>
  <li>{ "send": true, "message": "success" }</li> 
  <li>{ "sent": false, "message": "error message" } </li>
</ul>

# Note:
After Cloning the Project <br/>
Create environment.py file inside the /myproject/myproject/ <br/>

and copy these statements <br/>

ENV = "DEV" <br/>

ALLOWED_HOSTS = [] <br/>

SECRET_KEY = "mysecretkey" <br/>

TIME_ZONE = 'UTC' <br/>
