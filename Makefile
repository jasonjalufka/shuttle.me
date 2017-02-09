verify:
		pyflakes src/doublemap
		pep8 --ignore=E501, E225 src/doublemap

install:
		python setup.py install

clean:
		find . -name *.pyc -delete
		rm build -rf
		rm dist -rf
		rm src/doublemap.egg-info -rf
