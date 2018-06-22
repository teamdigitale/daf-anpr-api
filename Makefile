
YAML=$(shell find * -name \*yaml)
YAMLSRC=$(shell find openapi -name \*yaml.src)
YAMLGEN=$(patsubst %.yaml.src,%.yaml,$(YAMLSRC))


yaml: $(YAMLGEN)

%.yaml: %.yaml.src
	. .tox/py36/bin/activate
	yamllint $<
	python ./scripts/yaml-resolver.py $< $@

#
# dataloader
#
prepare:
	which git-lfs || curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash && apt -y install git-lfs
	git lfs pull

setup: prepare
	docker-compose up -d elastic kibana
	docker-compose up dataloader


yamllint: $(YAML)
	. .tox/py36/bin/activate
	yamllint $?

# Create a simple project starting from OpenAPI v3 spec
#  in simple.yaml.
prj-simple/swagger_server/swagger/swagger.yaml: openapi/core-vocabularies.yaml
	./scripts/yaml-resolver.sh $< /dev/fd/1  > /tmp/openapi-resolved.yaml


	# Convert OpenAPI v3 to a temporary Swagger 2.0 using
	#  docker image ioggstream/api-spec-converter
	./scripts/openapi2swagger.sh /tmp/openapi-resolved.yaml > /tmp/swagger.yaml

	# Generate a flask client from v2 spec using
	#  docker image swaggerapi/swagger-codegen-cli
	./scripts/generate-flask.sh /tmp/swagger.yaml  ./prj-simple/

app-test: prj-simple/swagger_server/swagger/swagger.yaml
	docker-compose up --build test

app-run: prj-simple/swagger_server/swagger/swagger.yaml
	# Build and run the application
	docker-compose up --build simple

