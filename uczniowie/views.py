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


@app.route("/lista_kl")
def lista_kl():
    klasy = Klasa().select()
    return render_template('lista_kl.html', kalsy=klasy)


@app.route("/lista_ucz")
def lista_ucz():
    uczniowie = Uczen().select()
    return render_template('lista_ucz.html', uczniowie=uczniowie)


@app.route("/dodaj_kl", methods=['GET', 'POST'])
def dodaj_kl():
    form = KlasaForm()
    form.klasa.choices = [(kl.id, kl.klasa) for kl in Klasa.select()]

    if form.validate_on_submit():
        kl = Klasa(klasa=form.klasa.data, rok_naboru=form.rok_naboru.data,
                   rok_matury=form.rok_matury.data)
        kl.save()

        flash("Dodano klasę!")
        return redirect(url_for("index"))
    elif request.method == "POST":
        flash_errors(form)

    return render_template("dodaj_kl.html", form=form)


@app.route("/dodaj_ucz", methods=['GET', 'POST'])
def dodaj_ucz():
    form = UczenForm()
    if form.validate_on_submit():
        ucz = Uczen(imie=form.imie.data, nazwisko=form.nazwisko.data,
                    plec=form.plec.data, klasa=form.klasa.data)
        ucz.save()

        flash("Dodano ucznia!")
        return redirect(url_for("index"))
    elif request.method == "POST":
        flash_errors(form)

    return render_template("dodaj_ucz.html", form=form)


def flash_errors(form):
    """Odczytanie wszystkich błędów formularza i przygotowanie komunikatów"""
    for field, errors in form.errors.items():
        for error in errors:
            if type(error) is list:
                error = error[0]
            flash("Błąd: {}. Pole: {}".format(
                error,
                getattr(form, field).label.text))


def get_or_404(pid):
    try:
        k = Klasa.get_by_id(kid)
        return k
    except Klasa.DoesNotExist:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
