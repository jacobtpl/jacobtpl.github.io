from flask import make_response, render_template, request, send_from_directory, send_file, redirect
from werkzeug import secure_filename
from app import app
import sys
sys.path.append("..")
import facialcommunism as fc

@app.route('/')
def rootpage():
	print("hello")
	print(sys.path)
	return app.send_static_file('index.html')

@app.route('/form')
def formpage():
	print("yay form")
	print(sys.path)
	return app.send_static_file('form.html')

@app.route('/final')
def finalpage():
	print("nay final")
	print(sys.path)
	return app.send_static_file('final.html')

@app.route("/images/<path:path>")
def images(path):
    # fullpath = "./app/images/" + path
    # resp = make_response(open(fullpath).read())
    # resp.content_type = "image/jpeg"
    return send_file('images/'+path)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      fn = 'app/images/'+secure_filename(f.filename)
      f.save(fn)
      print(fn)
      fc.write_image(fn)
      return redirect("/final", code=302)