.PHONY: run install

run:
	python3 k-means.py 3 100

install:
	pip3 install -r requirements.txt