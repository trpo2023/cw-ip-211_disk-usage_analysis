run:
	python3.9 main.py

test:
	pytest test.py

clean:
	rm -rf __pycache__
	rm -rf venv