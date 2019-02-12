# -*- coding: utf-8 -*-
# quiz-orm/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, HiddenField, FieldList
from wtforms import SelectField, FormField, BooleanField
from wtforms.validators import Required

blad1 = 'To pole jest wymagane'


class KlasaForm(FlaskForm):
    id = HiddenField()
    klasa = StringField("Klasa: ",
                        validators=[Required(message=blad1)])
    rok_naboru = StringField("Rok naboru: ")
    rok_matury = StringField("Rok matury: ", )


class UczenForm(FlaskForm):
    id = HiddenField()
    imie = StringField("Imie: ", validators=[Required(message=blad1)])
    nazwisko = StringField("Nazwisko: ", validators=[Required(message=blad1)])
    plec = BooleanField("Czy jesteś kobietą?: ")
    klasa = StringField("Klasa: ")
