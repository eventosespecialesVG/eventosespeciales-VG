from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Variables de entorno de Render
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/servicios')
def servicios():
    return render_template('servicios.html')


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():

    if request.method == 'POST':

        nombre = request.form['nombre']
        correo = request.form['correo']
        mensaje = request.form['mensaje']

        cuerpo = f"""
Nuevo mensaje desde la página web

Nombre: {nombre}

Correo del cliente: {correo}

Mensaje:

{mensaje}
"""

        msg = MIMEText(cuerpo, "plain", "utf-8")
        msg["Subject"] = "Nuevo mensaje - Eventos Especiales VG"
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg["Reply-To"] = correo

        try:
            servidor = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            servidor.login(EMAIL, PASSWORD)
            servidor.send_message(msg)
            servidor.quit()

            return render_template("contacto.html", enviado=True)

        except Exception as e:
            print("Error al enviar el correo:", e)
            return f"Error al enviar el correo: {e}"

    return render_template("contacto.html", enviado=False)


if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)