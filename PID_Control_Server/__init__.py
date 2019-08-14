import os

from flask import Flask

#from  import PID


def create_app(test_config=None):
    #create and configure the app
    app=Flask(__name__, instance_relative_config=True)
    
    from . import PID
    from .forms import LoginForm
    import usbtmc
    
    pid=PID.PID()
    pid.I=20
    
    @app.route('/hello')
    def hello():
        form = LoginForm
        
        return render_template('login.html', title='Sign In', form=form)
        
    
    return app