from flask_script import Shell, Manager

from flasky import create_app

if __name__ == '__main__':
    app = create_app()
    app.debug = True
    
    from flasky.auth.models import db
    def _make_context():
        return dict(app=app, db=db)

    manager = Manager(create_app)
    manager.add_command("shell", Shell(make_context=_make_context))
    manager.run()