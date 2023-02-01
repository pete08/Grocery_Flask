

# CLI: $ python3 <--- does not produce a Flask Application Automatic Context: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/contexts
# CLI: $ flask --app grocery shell <--- produces Flask Application Automatice Context: https://flask.palletsprojects.com/en/2.2.x/cli/#open-a-shell. This "Autoamtic Context" is necessary to populate/test DBs
#### CLI DBs:
#### $ flask --app grocery shell
#### >>> from grocery import db
#### >>> db.create_all()
#### >>> user_1 = User(username='peter', email='p@mail.com, password='password')
#### >>> db.session.add(user_1)
#### >>> db.session.commit()
#### >>> User.query.all()




from grocery import app



if __name__ == '__main__':
    app.run(debug=True)