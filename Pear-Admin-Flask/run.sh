cd /home/ponding_object/Pear-Admin-Flask
# poetry run flask  --app app.py run -h 0.0.0.0 -p 5000 --debug
poetry run gunicorn -c gunicorn_config.py app:app
echo "flask run end!"
