LAMMPS_DIR=lammps
DOCSET_ROOT=lammps.docset
DOCSET_DOCS=$(DOCSET_ROOT)/Contents/Resources/Documents

docset: doc
	rm -rv $(DOCSET_DOCS) || true
	mkdir -p $(DOCSET_DOCS)
	cp -rv $(LAMMPS_DIR)/doc/html/* $(DOCSET_DOCS)
	python3 scripts/build.py

doc:
	mkdir -p $(LAMMPS_DIR)
	curl -fsSL https://download.lammps.org/tars/lammps.tar.gz --output - |\
		tar -xzvf - --strip-components=1 --directory=$(LAMMPS_DIR)
	$(MAKE) -C $(LAMMPS_DIR)/doc html

clean:
	rm -rvf $(LAMMPS_DIR)
