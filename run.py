from server import app as app
import os

port = int(os.environ.get("PORT", 8000))
app.app.run(host='0.0.0.0', port=port)