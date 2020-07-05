#!env make

APPLICATION = jd_app
    VERSION = 0.1.0

# / ------ python stuff --------/ #
        REQ = requirements.txt
        APP = $(APPLICATION).py
     PYLIBS = jd_lib/*.py jd_modules/*.py
       DOCS = README.md

     APPTMP = tasks/ app.db
     RUNENV = venv __pycache__ jd_lib/__pycache__ jd_modules/__pycache__
# / ------ python stuff --------/ #

      phony = prep run package clean


all:    prep run package clean


run:    venv $(APP) $(PYLIBS)
	-( . venv/bin/activate && python3 $(APP) )

venv: $(REQ)
	python3 -m venv venv

prep: venv
	( . venv/bin/activate && pip install -r $(REQ) )

edit: venv
	( . venv/bin/activate && atom . )

# $(APP):
# $(PYLIBS):

package: $(REQ) $(APP) $(PYLIBS)
	( . venv/bin/activate && pip freeze > $(REQ) )
	tar -czvpSf $(APPLICATION)-$(VERSION).tgz Makefile $(APP) $(PYLIBS) $(REQ) $(DOCS)
	sha256sum $(APPLICATION)-$(VERSION).tgz > $(APPLICATION)-$(VERSION).tgz.sha256sum

clobber: clean
	-rm -r $(APPTMP)

clean:
	-rm -r $(RUNENV)
