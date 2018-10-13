from flask import Flask, render_template

app = Flask(__name__)

@app.route('/taken_pic', methods=['GET','POST'])
def taken_pic():
    if request.method == 'POST':
        inputImg = request.form['file'];
        #import blend function with facialCommunism function
        outputImg = facialCommunism(inputImg);
        return jsonify(request.form['userID'], )#return what?
    return render_template('signup.html')#return what?
#troubleshooting
if __name__ == "__main__":
    app.run(debug=True)
