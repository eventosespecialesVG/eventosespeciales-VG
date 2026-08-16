from flask import Flask, render_template, request
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Datos de Gmail desde las variables de entorno de Render
EMAIL = os.environ.get("ventasvg2022@gmail.com")
PASSWORD = os.environ.get("jmrz wyeg skxa yees")


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

        try:
            # Crear el correo
            email = MIMEMultipart()

            email["From"] = EMAIL
            email["To"] = EMAIL
            email["Subject"] = "Nuevo mensaje - Eventos Especiales VG"
            email["Reply-To"] = correo

            contenido = f"""
Nuevo mensaje desde la página web de Eventos Especiales VG

Nombre: {nombre}

Correo del cliente: {correo}

Mensaje:
{mensaje}
"""

            email.attach(
                MIMEText(contenido, "plain", "utf-8")
            )

            # Conectar con Gmail
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()

            # Iniciar sesión
            servidor.login(EMAIL, PASSWORD)

            # Enviar correo
            servidor.send_message(email)

            servidor.quit()

            print("Correo enviado correctamente")

            return render_template(
                "contacto.html",
                enviado=True
            )

        except Exception as e:

            print("ERROR AL ENVIAR CORREO:", e)

            return render_template(
                "contacto.html",
                enviado=False,
                error=True
            )

    return render_template(
        "contacto.html",
        enviado=False
    )


if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=puerto
    )