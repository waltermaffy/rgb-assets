frontend:
	poetry run streamlit run webapp.py

test:
	pytest tests/
	
isort:
	poetry run isort --profile black . 

black:
	poetry run black . 

format:
	make isort
	make black
