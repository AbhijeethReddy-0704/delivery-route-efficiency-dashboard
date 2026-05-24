.PHONY: install generate-data validate-data build-db test run-dashboard

install:
	pip install -r requirements.txt

generate-data:
	python scripts/generate_data.py

validate-data:
	python scripts/validate_data.py

build-db:
	python scripts/build_sqlite_db.py

test:
	pytest

run-dashboard:
	streamlit run streamlit_app.py
