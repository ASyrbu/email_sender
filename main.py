from sanic_creation.configure import get_application

kodeson_app = get_application()

if __name__ == "__main__":
    kodeson_app.run(host='localhost', port=8000, fast=True)
