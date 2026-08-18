from flask import Flask, render_template, request, send_from_directory
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

app = Flask(__name__)

# Clave de API de Brevo
BREVO_API_KEY = os.environ.get("BREVO_API_KEY")

print("BREVO_API_KEY configurada:", bool(BREVO_API_KEY))
print("Longitud de la API KEY:", len(BREVO_API_KEY) if BREVO_API_KEY else 0)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

#google
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml', mimetype='application/xml')


@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')
    
# Verificación de Google
@app.route('/googledf2a635172360864.html')
def google_verification():
    return send_from_directory(
        'static',
        'googledf2a635172360864.html'
    )


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():

    if request.method == 'POST':

        nombre = request.form['nombre']
        correo = request.form['correo']
        mensaje = request.form['mensaje']

        try:
            configuracion = sib_api_v3_sdk.Configuration()
            configuracion.api_key['api-key'] = BREVO_API_KEY

            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
                sib_api_v3_sdk.ApiClient(configuracion)
            )

            email = sib_api_v3_sdk.SendSmtpEmail(
                sender={
                    "name": "Eventos Especiales VG",
                    "email": "ventasvg2022@gmail.com"
                },
                to=[
                    {
                        "email": "ventasvg2022@gmail.com"
                    }
                ],
                reply_to={
                    "email": correo,
                    "name": nombre
                },
                subject="Nuevo mensaje - Eventos Especiales VG",
                html_content=f"""
                <h2>Nuevo mensaje desde la página web</h2>

                <p><strong>Nombre:</strong> {nombre}</p>

                <p><strong>Correo del cliente:</strong> {correo}</p>

                <p><strong>Mensaje:</strong></p>

                <p>{mensaje}</p>
                """
            )

            api_instance.send_transac_email(email)

            print("Correo enviado correctamente")

            return render_template(
                "contacto.html",
                enviado=True
            )

        except ApiException as e:

            print("ERROR DE BREVO:", e)

            return render_template(
                "contacto.html",
                enviado=False,
                error=True
            )

        except Exception as e:

            print("ERROR:", e)

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