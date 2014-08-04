BASEDIR=$(CURDIR)
DISTDIR=$(BASEDIR)/dist
BUILDDIR=$(BASEDIR)/build
PACKAGE='serialkiller-plugins'

test: pep8 coverage

build: 
	@echo 'Running build'
	@python setup.py build

deploy:
	@echo 'Upload to PyPi'
	@python setup.py sdist upload
	@echo 'Done'

dist:
	@echo 'Generating a distributable python package'
	@python setup.py sdist
	@echo 'Done'

install: 
	@echo 'Running install'
	@echo 'install metar'
	@wget "http://downloads.sourceforge.net/project/python-metar/python-metar/v1.4.0/metar-1.4.0.tar.gz?r=&ts=1407175653&use_mirror=freefr" -O metar-1.4.0.tar.gz
	@pip install metar-1.4.0.tar.gz
	@python setup.py install


pep8:
	@pep8 $(PACKAGE) --config=pep8.rc
	@echo 'PEP8: OK'

coverage:
	@echo 'Running test suite with coverage'
	@coverage erase
	@coverage run --rcfile=coverage.rc tests.py
	@coverage html
	@coverage report --rcfile=coverage.rc

clean:
	@rm -fr $(DISTDIR)
	@rm -fr $(BUILDDIR)

.PHONY: help doc build test dist install clean 
