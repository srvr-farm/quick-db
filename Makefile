
.PHONY: develop clean check-env

venv: venv/bin/activate
venv/bin/activate: setup.py
	touch constraints.txt
	test -d venv || virtualenv --never-download venv
	. venv/bin/activate ; pip install -U pip
	. venv/bin/activate ; pip install -U setuptools
	. venv/bin/activate ; pip install -U .
develop: venv
	. venv/bin/activate ; unset https_proxy; pip install -e .
clean:
	rm -rf dist *.egg-info build _trial_temp _tox.ini venv .tox pkgbuild dist
	find . -name '__pycache__' -print | xargs rm -rf
	find . -name '*pyc' -delete
check-env:
	ifndef BUILD_NUMBER
		$(error BUILD_NUMBER is not set)
	endif
