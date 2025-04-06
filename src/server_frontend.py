from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html')

@app.route('/newmember')
def newmember():
   return render_template('newmember.html')

@app.route('/returningmember')
def returningmember():
   return render_template('returningmember.html')

if __name__ == '__main__':
   app.run(host="localhost", port="8080", debug=True)
