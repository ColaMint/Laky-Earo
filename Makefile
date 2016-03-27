.PHONY: test docs

export PYTHONPATH := $(CURDIR)

test:
	python ./test/test.py

docs:
	$(MAKE) -C docs html
