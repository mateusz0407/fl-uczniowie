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
    return render_template('lista_kl.html', klasy=klasy)


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


def get_or_404(kid):
    try:
        k = Klasa.get_by_id(kid)
        return k
    except Klasa.DoesNotExist:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/edytuj_ucz/<int:kid>", methods=['GET', 'POST'])
def edytuj_ucz(kid):
    k = get_or_404(kid)
    form = UczenForm(obj=k)

    if form.validate_on_submit():
        k.imie = form.imie.data
        k.nazwisko = form.nazwisko.data
        k.plec = form.plec.data
        k.klasa = form.klasa.data
        k.save()
        flash("Zaktualizowano ucznia: {}".format(form.imie.data))
        return redirect(url_for("lista_ucz"))
    elif request.method == "POST":
        flash_errors(form)

    return render_template("edytuj_ucz.html", form=form)


@app.route("/edytuj_kl/<int:kid>", methods=['GET', 'POST'])
def edytuj_kl(kid):
    k = get_or_404(kid)
    form = KlasaForm(obj=k)

    if form.validate_on_submit():
        k.klasa = form.klasa.data
        k.rok_naboru = form.rok_naboru.data
        k.rok_matury = form.rok_matury.data
        k.save()
        flash("Zaktualizowano klasę: {}".format(form.klasa.data))
        return redirect(url_for("lista_kl"))
    elif request.method == "POST":
        flash_errors(form)

    return render_template("edytuj_kl.html", form=form)
