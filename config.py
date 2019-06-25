
# used by Flask to encrypt session cookies
SECRET_KEY = 'secret'
DATA_BACKEND = 'cloudsql'
MONGO_URI = 'mongodb+srv://ttsapp:3Ca56aiL7gk_E2k@tts-jbbfq.gcp.mongodb.net/jupez-dev?retryWrites=true&w=majority'
CLOUD_STORAGE_BUCKET = 'jupez-p-images'
GOOGLE_PROJECT_ID = 'jupez-p',
GOOGLE_CLIENT_ID = "116272384731804151381"
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# CloudSQL & SQLAlchemy configuration
# Replace the following values the respective values of your Cloud SQL
# instance.
import os

CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = '135296'
CLOUDSQL_DATABASE = 'jupez'
# Set this value to the Cloud SQL connection name, e.g.
#   "project:region:cloudsql-instance".
# You must also update the value in app.yaml.
CLOUDSQL_CONNECTION_NAME = 'jupez-p:us-central1:library'

# The CloudSQL proxy is used locally to connect to the cloudsql instance.
# To start the proxy, use:
#
#   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
#
# Port 3306 is the standard MySQL port. If you need to use a different port,
# change the 3306 to a different port number.

# Alternatively, you could use a local MySQL instance for testing.
LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)

# When running on App Engine a unix socket is used to connect to the cloudsql
# instance.
LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI
