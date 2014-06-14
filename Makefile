
all: test2

test1: rendered.py
	cat parser.syntax | python rendered.py

test2: rendered.py
	cat parser.syntax | python rendered.py >dat
	diff parser.data dat
	rm -f dat

rendered.py: python.mustache parser.data
	python -mstaching -t python.mustache -d parser.data -r rendered.py

xtest1: python.out
	diff python.out parser.py
	@echo "## TEST1 SUCCEEDS ##"

clean:
	rm -f m out *.pyc .*~ *~ *.json *.out \#* .\#* rendered.py

