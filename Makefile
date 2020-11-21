.PHONY: pre-commit
pre-commit:
	pre-commit install
shell:
	docker-compose exec app python manage.py shell -i bpython
check:
	docker-compose exec app python manage.py check --deploy
