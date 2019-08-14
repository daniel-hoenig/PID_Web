### Definition of the Fields that shoul appear on the Controller Webpage
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class PIDForm(FlaskForm):
    P= FloatField('Proportional Gain', validators=[NumberRange(0,10)])
    I = FloatField('Integral Gain', validators=[NumberRange(0,10)])
    D = FloatField('Differential Gain',validators=[NumberRange(0,10)])
    submit = SubmitField('Set PID')
    
class TemperatureForm(FlaskForm):
    SP = FloatField('Temperature',validators=[NumberRange(0,120)])
    submit = SubmitField('Set Temperature')
    
class BiasForm(FlaskForm):
    Bias = FloatField ('PID Offset', validators=[NumberRange(0,1)])
    submit = SubmitField('Set Offset')

class LimitForm(FlaskForm):
    uplim = FloatField('Upper Limit',validators=[NumberRange(0,3)])
    lolim = FloatField('Lower Limit',validators=[NumberRange(0,3)])
    submit = SubmitField('Set Limits')