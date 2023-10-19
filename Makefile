.PHONY: fmt lint test release generate-lockfiles clean

fmt:
	python -m autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive .
	python -m isort . --profile=black
	python -m black . --experimental-string-processing

lint:
	python -m flake8 . --max-line-length 88 --ignore F401,W503
	python -m isort . --profile=black --check-only
	python -m black . --check

check:
	python -m mypy .

test:
	python -m pytest tests -n auto

dist:
	python -m build
build: dist

release:
	python -m semantic_release publish

generate-lockfiles:
	docker run -it -v $$PWD:/vol -w /vol python:3.9 bash -c "python -m pip install -e '.[tools]' && python -m pip freeze > .lockfiles/tools.txt"

clean:
	rm -rf build dist *.egg-info
