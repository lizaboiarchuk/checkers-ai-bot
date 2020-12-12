from .views import Views


def setup_routes(app):
    Views().configure(app)
