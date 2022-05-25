all: pcore/pcore pcore_rhel8.zip

pcore/pcore: src/pcore.main src/getdebuginfo
	@if [ ! -d pcore_tmp ]; then mkdir pcore_tmp; fi
	./build.py src/getdebuginfo < src/pcore.main > pcore_tmp/pcore
	mv pcore_tmp pcore
	chmod +x pcore/pcore

pcore_rhel8.zip: pcore/pcore
	zip pcore_rhel8.zip -r pcore

clean:
	rm -fr pcore pcore_tmp pcore.rhel8.zip
