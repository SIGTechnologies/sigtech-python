.PHONY: install test clean

install:
    pip install -r requirements.txt

test:
    pytest tests

clean:
    rm -rf build dist *.egg-info
