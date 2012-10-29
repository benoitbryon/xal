# Makefile for development.
# See INSTALL and docs/dev.txt for details.
SHELL = /bin/bash
PROJECT = 'xal'
ROOT_DIR = $(shell pwd)
DATA_DIR = $(ROOT_DIR)/var
PYTHON = python
BUILDOUT_DIR = $(ROOT_DIR)/lib/buildout
BUILDOUT_BOOTSTRAP_URL = "https://raw.github.com/buildout/buildout/7a4f6107bfc0d3669f11c7893f2934696af319dc/bootstrap/bootstrap.py"
BUILDOUT_BOOTSTRAP = $(BUILDOUT_DIR)/bootstrap.py
BUILDOUT = $(ROOT_DIR)/bin/buildout
BUILDOUT_ARGS = 


bootstrap-buildout:
	# Install zc.buildout.
	if [ ! -x $(BUILDOUT) ]; then \
	    mkdir -p $(BUILDOUT_DIR); \
	    if [ ! -f $(BUILDOUT_BOOTSTRAP) ]; then \
	        wget $(BUILDOUT_BOOTSTRAP_URL) -O $(BUILDOUT_BOOTSTRAP); \
	    fi; \
	    $(PYTHON) $(BUILDOUT_BOOTSTRAP); \
	fi


buildout: bootstrap-buildout
	# Run zc.buildout.
	$(BUILDOUT) $(BUILDOUT_ARGS)


develop: buildout


update: develop


clean:
	find $(ROOT_DIR)/ -name "*.pyc" -delete
	find $(ROOT_DIR)/ -name ".noseids" -delete


distclean: clean
	rm -rf $(ROOT_DIR)/*.egg-info


maintainer-clean: distclean
	rm -rf $(ROOT_DIR)/bin/
	rm -rf $(ROOT_DIR)/lib/


test: documentation


apidoc:
	rm -rf docs/api/*
	$(ROOT_DIR)/bin/sphinx-apidoc --output-dir=$(ROOT_DIR)/docs/api/ --suffix=txt $(ROOT_DIR)/xal


sphinx:
	make --directory=docs clean html doctest


documentation: apidoc sphinx


release:
	bin/fullrelease
