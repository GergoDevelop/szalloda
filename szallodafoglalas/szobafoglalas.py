from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

class Szoba:
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=5000, szobaszam=szobaszam)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=8000, szobaszam=szobaszam)

class Foglalas:
    def __init__(self, szoba, datum_tol, datum_ig):
        self.szoba = szoba
        self.datum_tol = datum_tol
        self.datum_ig = datum_ig

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def foglalas(self, szobaszam, datum_tol, datum_ig):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam:
                if (datum_tol >= foglalas.datum_tol and datum_tol <= foglalas.datum_ig) or (datum_ig >= foglalas.datum_tol and datum_ig <= foglalas.datum_ig):
                    return None
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                foglalas = Foglalas(szoba, datum_tol, datum_ig)
                self.foglalasok.append(foglalas)
                return foglalas
        return None

    def lemondas(self, szobaszam, datum_tol):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum_tol == datum_tol:
                self.foglalasok.remove(foglalas)
                return
        return None

    def listaz(self):
        return sorted(self.foglalasok, key=lambda x: x.datum_tol)

szalloda = Szalloda("Hotel ABC")
szalloda.szobak.append(EgyagyasSzoba(101))
szalloda.szobak.append(EgyagyasSzoba(102))
szalloda.szobak.append(KetagyasSzoba(201))
szalloda.szobak.append(KetagyasSzoba(202))

@app.route('/')
def index():
    foglalasok = szalloda.listaz()
    return render_template('index.html', foglalasok=foglalasok)

@app.route('/foglalas', methods=['GET', 'POST'])
def foglalas():
    if request.method == 'POST':
        szobaszam = int(request.form['szobaszam'])
        datum_tol = datetime.strptime(request.form['datum_tol'], '%Y-%m-%d')
        datum_ig = datetime.strptime(request.form['datum_ig'], '%Y-%m-%d')
        foglalas = szalloda.foglalas(szobaszam, datum_tol, datum_ig)
        if foglalas:
            return redirect('/')
    return render_template('foglalas.html', szobak=szalloda.szobak)

@app.route('/lemondas', methods=['GET', 'POST'])
def lemondas():
    if request.method == 'POST':
        szobaszam = int(request.form['szobaszam'])
        datum_tol = datetime.strptime(request.form['datum_tol'], '%Y-%m-%d')
        szalloda.lemondas(szobaszam, datum_tol)
        return redirect('/')
    return render_template('lemondas.html')

if __name__ == '__main__':
    app.run(debug=True)