# Django-Rest-Example

It is a simple django rest project, it is available on https://farooqhidayat.pythonanywhere.com <br/>

Only GET request https://farooqhidayat.pythonanywhere.com/api/test <br/>
<ul>
  <li>Response List of Objects (Paginated)</li>
</ul>
Both GET and POST requests https://farooqhidayat.pythonanywhere.com/api/test/create <br/>
<ul>
  <li>GET Response List of Objects (Non-Paginated) </li>
  <li>POST Response Posted Object</li>
</ul>
Send Email: POST request https://farooqhidayat.pythonanywhere.com/api/test/sendemail <br/> 
JSON Payload: 
<ul>
  <li>{ "email": "email@email.com" } OR</l1> 
  <li>{ "email": ["email_1@email.com", "email_2@email.com"] } </li>
</ul>
Response: 
<ul>
  <li>{ "send": true, "message": "success" } OR</li> 
  <li>{ "sent": false, "message": "error message" } </li>
</ul>

# User Registration 

registration end-point: https://farooqhidayat.pythonanywhere.com/api/register/signup/ api to register a user </br>
It requires a json payload to be posted </br>
{ “email”: “you@email.com”, “password”: “yourpassword”}

after that you need to activate your user using the </br>
verification end-point: https://farooqhidayat.pythonanywhere.com/api/register/verify/ </br>
it also requires a json payload to be posted </br>
{ “email”: “email_you_signed_up_with@email.com”, “verification_code”: “code_you received_in_your_email”}

Note: “It has been built such a way that verfication code expires after 10 minutes”

# Note:
After Cloning the Project <br/>
Create environment.py file inside the /myproject/myproject/ <br/>

and copy these statements <br/>

ENV = "DEV" <br/>

ALLOWED_HOSTS = [] <br/>

SECRET_KEY = "mysecretkey" <br/>

TIME_ZONE = 'UTC' <br/>

EMAIL = "your@email.com"

PASSWORD = "yourpassword"
