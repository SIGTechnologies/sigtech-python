.PHONY: fmt lint test release generate-lockfiles clean

fmt:
	python -m isort .
	python -m black .

lint:
	python -m flake8 . --max-line-length 200 --ignore F401,W503
	python -m isort . --check-only
	python -m black . --check

test:
	python -m pytest tests

dist:
	python -m build
build: dist

release:
	python -m semantic_release publish

generate-lockfiles:
	docker run -it -v $$PWD:/vol -w /vol python:3.9 bash -c "python -m pip install -e '.[tools]' && python -m pip freeze > .lockfiles/tools.txt"

clean:
	rm -rf build dist *.egg-info
