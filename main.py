from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('trialPost.html')#index.html
	
@app.route('/picDisplay', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      
      #perform desired function on f: facialCommunism     
      f.save(secure_filename(f.filename))
      return render_template('picDisplay.html')

@app.route('/picTaking', methods = ['GET', 'POST'])
def undo():
   if request.method == 'POST':
      f = request.files['file']

      #perform desired function on f      
      #f.save(secure_filename(f.filename))
      return render_template('vidya.html')


