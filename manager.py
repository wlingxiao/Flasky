from flasky import create_app

if __name__ == '__main__':
    app = create_app()
    app.debug = True
    from flasky.auth.models import db
    with app.app_context():
        db.create_all()
    app.run()