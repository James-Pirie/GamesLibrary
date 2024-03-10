from games import create_app
from flask import Flask, render_template

app = create_app()


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/browse')
def about():
    return render_template('browse.html')


@app.route('/gamedescription')
def images():
    return render_template('gameDescription.html')


@app.route('/authentication')
def authentication():
    return render_template('credentials.html')


@app.route('/userprofile')
def userprofile():
    return render_template('userProfile.html')


if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False, debug=True)
