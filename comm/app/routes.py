from flask import render_template, request
from werkzeug import secure_filename
from app import app
import sys
sys.path.append("..")
import facialcommunism as fc

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      fn = secure_filename(f.filename)
      f.save(fn)
      print(fn)
      fc.get_image(fn)
