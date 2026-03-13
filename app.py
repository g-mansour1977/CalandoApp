from flask import Flask, jsonify, request, send_file
import sqlite3
import qrcode
import io

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("calando.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS paiements(
    id INTEGER PRIMARY KEY,
    voiture TEXT,
    montant INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/payer", methods=["POST"])
def payer():

    data = request.json or {}

    voiture = data.get("voiture")
    montant = data.get("montant")

    if not voiture or not montant:
        return jsonify({"error": "données manquantes"}), 400

    conn = sqlite3.connect("calando.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO paiements (voiture,montant) VALUES (?,?)",
        (voiture,montant)
    )

    conn.commit()
    conn.close()

    return jsonify({"status":"ok"})


@app.route("/stats/<voiture>")
def stats(voiture):

    conn = sqlite3.connect("calando.db")
    c = conn.cursor()

    c.execute(
        "SELECT COUNT(*), SUM(montant) FROM paiements WHERE voiture=?",
        (voiture,)
    )

    data = c.fetchone()
    conn.close()

    return jsonify({
        "passagers": data[0] if data[0] else 0,
        "total": data[1] if data[1] else 0
    })


@app.route("/qr/<voiture>")
def qr(voiture):

    url = f"http://192.168.1.27:5000/payer/{voiture}"

    img = qrcode.make(url)

    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)

    return send_file(buf, mimetype="image/png")


@app.route("/payer/<voiture>", methods=["GET"])
def payer_voiture(voiture):

    montant = 100

    conn = sqlite3.connect("calando.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO paiements (voiture,montant) VALUES (?,?)",
        (voiture,montant)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": f"Paiement enregistré pour {voiture}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)