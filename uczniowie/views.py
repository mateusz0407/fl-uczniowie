# -*- coding: utf-8 -*-
# quiz-orm/views.py

from flask import Flask
from flask import render_template, request, redirect, url_for, abort, flash
from modele import *
from forms import *

app = Flask(__name__)


@app.route('/')
def index():
    """Strona główna"""
    return render_template('index.html')


@app.route("/dodaj_kl", methods=['GET', 'POST'])
def dodaj_kl():
    form = KlasaForm()
    if form.validate_on_submit():
        kl = Klasa(klasa=form.klasa.data, rok_naboru=form.rok_naboru.data,
                   rok_matury=form.rok_matury.data)
        kl.save()
        for o in form.odpowiedzi.data:
            odp = Odpowiedz(odpowiedz=o['odpowiedz'], pytanie=p.id,
                            odpok=int(o['odpok']))
            odp.save()
        flash("DOdano pytanie: {}".format(form.pytanie.data))
        return redirect(url_for("lista"))
    elif request.method == "POST":
        flash_errors(form)

    return render_template("dodaj.html", form=form)

