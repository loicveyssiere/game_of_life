# ==============================================================================
# 	PYTHON MAKEFILE
# ==============================================================================

.PHONY: all env clean deep-clean

# ------------------------------------------------------------------------------
# 	VARIABLES: only make changes in this section
# ------------------------------------------------------------------------------
VIRTUALENV = .env3.6
PYTHON = python3.6

# ------------------------------------------------------------------------------
# 	VARIABLE CONSTRUCTION
# ------------------------------------------------------------------------------
SITE_PACKAGES := $(shell pip show pip | grep '^Location' | cut -f2 -d':')

# ------------------------------------------------------------------------------
# 	RULES
# ------------------------------------------------------------------------------
all:
	@echo "Please use 'make env'"

env: $(VIRTUALENV) $(SITE_PACKAGES)

$(VIRTUALENV):
	virtualenv -p $(PYTHON) ./$(VIRTUALENV)

$(SITE_PACKAGES): requirements.txt
	./$(VIRTUALENV)/bin/pip install -r $<

clean:
	@echo "Cleaning"

deep-clean: clean
	@echo "Deep Cleaning"
	@rm -rf ./$(VIRTUALENV)
