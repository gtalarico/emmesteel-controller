build:
	python3 -m build

upload:
	python3 -m twine upload --verbose --repository testpypi dist/*
