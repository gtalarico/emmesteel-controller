pypi-test:
	rm -rdf ./dist
	python3 -m build
	python3 -m twine upload --verbose --repository testpypi dist/*

pypi:
	rm -rdf ./dist
	python3 -m build
	python3 -m twine upload dist/*
