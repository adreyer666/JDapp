#!env make

APPLICATION = jd_app
    VERSION = 0.1.1

# / ------ python stuff --------/ #
        REQ = requirements.txt
        APP = $(APPLICATION).py
     PYLIBS = jd_lib/*.py jd_modules/*.py
       DOCS = README.md

     APPTMP = tasks/ app.db
     RUNENV = venv
# / ------ python stuff --------/ #

all:    venv test run

venv: $(REQ)
	python3 -m venv venv
	( . venv/bin/activate \
	&& test -f $(REQ) && python -m pip install --upgrade -r $(REQ) \
	&& python -m pip freeze > $(REQ).tmp )
	diff -qB $(REQ).tmp $(REQ) || cp $(REQ).tmp $(REQ)
	rm $(REQ).tmp

test: venv
	( . venv/bin/activate && python -m pip install flake8 pytest )

run: venv $(APP) $(PYLIBS)
	-( . venv/bin/activate && python $(APP) )

edit: venv
	( . venv/bin/activate && python -m pip install --upgrade 'python-language-server[all]' )
	( . venv/bin/activate && atom . )

clobber: clean
	-rm -r $(APPTMP)

clean:
	-rm -r $(RUNENV)
	-find -type d -name __pycache__ -exec rm -r '{}' ';'

# ------------------------------------------------------------------------------------------# 

pyimage: Dockerfile $(REQ) $(APP) $(PYLIBS)
	buildah bud -f Dockerfile -t py-$(APPLICATION) .

runpyimage: $(APP) $(PYLIBS) image
	podman run -p 5000:5000 -ti py-$(APPLICATION)

debimage: Dockerfile.debian $(REQ) $(APP) $(PYLIBS)
	buildah bud -f Dockerfile.debian -t deb-$(APPLICATION) .

rundebimage: $(APP) $(PYLIBS) image
	podman run -p 5000:5000 -ti deb-$(APPLICATION)

package: $(REQ) $(APP) $(PYLIBS)
	tar -czvpSf $(APPLICATION)-$(VERSION).tgz Makefile $(APP) $(PYLIBS) $(REQ) $(DOCS)
	sha256sum $(APPLICATION)-$(VERSION).tgz > $(APPLICATION)-$(VERSION).tgz.sha256sum

