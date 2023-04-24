#!/usr/bin/env python3
from app import app

def application(environ, start_response):
        return app(environ, start_response)

if __name__ == "__main__":
    app.run()




