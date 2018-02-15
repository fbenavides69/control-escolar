from flask import render_template


def index():
    return render_template("index.html", title='Index')

#def profile(email):
#    user = User.query.filter_by(email=email).first()
#    return render_template('profile.html', user=user)
