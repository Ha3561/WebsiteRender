from flask import Flask, jsonify ,request, make_response, render_template, redirect, url_for    

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        return jsonify({'message': 'Login Success'})
    else:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})	
if __name__ == '__main__':
    app.run(debug=True,port=8080)
