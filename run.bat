if exist .\\database.enc (
    waitress-serve --listen=0.0.0.0:8080 app:app
) else (
    flask initdb
    waitress-serve --listen=0.0.0.0:8080 app:app
)
