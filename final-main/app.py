import logging
from flask import Flask, render_template
from controllers.cargo_controller import cargo_bp
from controllers.usuario_controller import usuario_bp
from controllers.rol_controller import rol_bp

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.register_blueprint(cargo_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(rol_bp)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True, use_reloader=True)