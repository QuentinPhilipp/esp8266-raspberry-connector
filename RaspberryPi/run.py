"""Application entry point."""
from os import environ
from SensorInterfacing import app

if __name__ == '__main__':
    app.run("0.0.0.0", port=5555,use_reloader=True)
