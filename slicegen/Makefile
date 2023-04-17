
#
#  Two external enviroment varible are needed.
# FABRIC_ME -- keep don and greg from colliding on the...
#  ... same docker instance  Just define it to ..
#  ... be unique to you e.g Don user DLP etc..

# FABRIC_FILES -- is a directory  with ssh keys...
#    the current tokem, ssh config


TAG := planner_$(FABRIC_ME)

check:
	test ! -z "$(FABRIC_ME)"     || exit 1
	test ! -z "$(FABRIC_FILES)"  || exit 1


build: check
	docker build ../slicegen --build-arg FABRIC_FILES=$(FABRIC_FILES)   -t $(TAG)

run:  check
	docker run -it -v $(FABRIC_FILES):$(FABRIC_FILES)  $(TAG)

clean:
	rm *~
	docker system prune

purge:
	docker system prune -a
