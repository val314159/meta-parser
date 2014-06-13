
all: test

test: python.out
	diff python.out parser.py
	@echo "## TEST SUCCEEDS ##"

python.out: python.json
	pystache python.mustache python.json >python.out

python.json: parser.syntax
	python parser.py <parser.syntax >python.json

clean:
	rm -f m out *.pyc .*~ *~ *.json *.out \#* .\#*

