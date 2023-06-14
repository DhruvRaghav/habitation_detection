from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Swagger UI blueprint
SWAGGER_URL = '/docs'
API_URL = '/static/openapi.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My Flask App"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Serve the Swagger JSON file at the '/static/swagger.json' URL
@app.route('/static/openapi.json')
def serve_swagger_json():
    with open('/home/ceinfo/Downloads/openapi (2).json', 'r') as f:
        return f.read()

if __name__ == '__main__':
    app.run(host='0.0.0.0')