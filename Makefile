dev-run:
	python3 booklog/manage.py runserver

migrations:
	python3 booklog/manage.py makemigrations && python3 booklog/manage.py migrate
