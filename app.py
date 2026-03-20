import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE = "database/landing_page.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()

    configuracion = conn.execute("SELECT * FROM configuracion_sitio LIMIT 1").fetchone()

    hero = conn.execute("SELECT * FROM hero LIMIT 1").fetchone()

    estadisticas = conn.execute("SELECT * FROM estadisticas ORDER BY orden").fetchall()

    cursos = conn.execute("SELECT * FROM cursos ORDER BY orden").fetchall()

    curso_caracteristicas = conn.execute("SELECT * FROM curso_caracteristicas ORDER BY curso_id, orden").fetchall()

    nosotros = conn.execute("SELECT * FROM nosotros LIMIT 1").fetchone()

    valores = conn.execute("SELECT * FROM valores ORDER BY orden").fetchall()

    conn.close()

    return render_template(
        'index.html',
        configuracion=configuracion,
        hero=hero,
        estadisticas=estadisticas,
        cursos=cursos,
        curso_caracteristicas=curso_caracteristicas,
        nosotros=nosotros,
        valores=valores
    )

@app.route('/enviar-contacto', methods=['POST'])
def enviar_contacto():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO mensajes_contacto (nombre, email, mensaje) VALUES (?, ?, ?)",
        (nombre, email, mensaje)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('ver_mensajes'))

@app.route('/mensajes')
def ver_mensajes():
    conn = get_db_connection()
    mensajes = conn.execute(
        "SELECT * FROM mensajes_contacto ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template('mensajes.html', mensajes=mensajes)

@app.route('/eliminar-mensaje/<int:id>', methods=['POST'])
def eliminar_mensaje(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM mensajes_contacto WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('ver_mensajes'))

if __name__ == "__main__":
    ##app.run(debug=True)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)