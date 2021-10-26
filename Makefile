
.PHONY: all run
all: run

myenv:
	python -m venv myenv

stamps/requirements: myenv requirements.txt
	./myenv/bin/pip install -r requirements.txt
	touch $@

run: stamps/requirements
	./myenv/bin/strawberry server main

