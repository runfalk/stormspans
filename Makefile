init:
	virtualenv --prompt="(stormspans)" venv
	source venv/bin/activate; pip install -r requirements.txt

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +

test:
	python setup.py test

sdist:
	python setup.py sdist
	rm -rf *.egg-info

.PHONY : init clean-pyc test sdist
