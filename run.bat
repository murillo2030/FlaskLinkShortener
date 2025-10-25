if exist .\\database.db (
    waitress-serve app:app
) else (
    flask initdb
    waitress-serve app:app
)
