.PHONY: test

export PYTHONPATH := $(CURDIR)

test:
	python ./test/test.py
