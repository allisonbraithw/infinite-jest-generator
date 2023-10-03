.PHONY: generate
generate: schema.graphql

venv: requirements.in
	python3.11 -m venv venv
	venv/bin/pip3.11 install wheel pip-tools pipdeptree

.PHONY: requirements.txt
requirements.txt: venv requirements.in
	venv/bin/pip-compile --resolver=backtracking requirements.in > requirements.txt
	venv/bin/pip3.11 install -r requirements.txt
	venv/bin/pipdeptree > .pip-deps.txt

schema.graphql: venv app/schema/schema.py
	venv/bin/python3.11 app/schema/schema.py > schema.graphql

run: venv
	venv/bin/python3.11 app/main.py