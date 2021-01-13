sleep 10
echo "\nScript starting!"
python manage.py makemigrations
python manage.py migrate
echo "\nMigrate finished!"
echo "\nRunserver!"
python manage.py runserver 0.0.0.0:8000