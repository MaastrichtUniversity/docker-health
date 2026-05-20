# Variables section
variable "ENV_TAG" {
  default = "latest"
}

variable "MAVEN_VERSION" {
  default = "3.9.16"
}

variable "ENV_REGISTRY_HOST" {
  default = "registry.prod.dh.unimaas.nl"
}

group "default" {
  targets = ["transform-rest", "federation-rest", "test-federation-rest", "etl-zib-pipeline", "etl-zib-rest", "test-single-node", "jupyter-zib", "jupyter-zib-prd", "portal", "terminology-server-proxy", "elk", "init-container"]
}

target "_src_etl" {
  contexts = {
    src_etl = "./externals/dh-hdp-etl"
  }
}

target "_hdp_templates" {
  contexts = {
    hdp_templates = "./externals/dh-hdp-zib-templates"
  }
}

target "transform-rest" {
  inherits = ["_hdp_templates"]
  args = {
    MAVEN_VERSION = "${MAVEN_VERSION}"
  }
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/transform-rest:${ENV_TAG}"]
  context = "./externals/dh-hdp-transform-rest"
}

target "federation-rest" {
  target = "rest"
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/federation-rest:${ENV_TAG}"]
  context = "./externals/dh-hdp-federation-api"
}

target "test-federation-rest" {
  target = "test"
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/federation-test:${ENV_TAG}"]
  context = "./externals/dh-hdp-federation-api"
}

target "etl-zib-pipeline" {
  inherits = ["_hdp_templates"]
  target = "pipeline"
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/etl-zib-pipeline:${ENV_TAG}"]
  context = "./externals/dh-hdp-etl"
}

target "etl-zib-rest" {
  inherits = ["_hdp_templates"]
  target = "rest"
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/etl-zib-rest:${ENV_TAG}"]
  context = "./externals/dh-hdp-etl"
}

target "test-single-node" {
  inherits = ["_hdp_templates"]
  target = "test"
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/etl-zib-test:${ENV_TAG}"]
  context = "./externals/dh-hdp-etl"
}

target "jupyter-zib" {
  inherits = ["_hdp_templates", "_src_etl"]
  args = {
    MAVEN_VERSION = "${MAVEN_VERSION}"
  }
  target = "development"
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/jupyter-zib:${ENV_TAG}"]
  context = "./externals/dh-hdp-notebooks"
}

target "jupyter-zib-prd" {
  inherits = ["_hdp_templates", "_src_etl"]
  args = {
    MAVEN_VERSION = "${MAVEN_VERSION}"
  }
  target = "production"
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/jupyter-zib-prd:${ENV_TAG}"]
  context = "./externals/dh-hdp-notebooks"
}

target "portal" {
  dockerfile = "Dockerfile"
  target = "development"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/portal:${ENV_TAG}"]
  context = "./externals/dh-hdp-portal"
}

target "terminology-server-proxy" {
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/terminology-server-proxy:${ENV_TAG}"]
  context = "./externals/dh-hdp-terminology-server-proxy"
}

target "elk" {
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/elk:${ENV_TAG}"]
  context = "./elk"
}

target "init-container" {
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/init-container:${ENV_TAG}"]
  context = "./init-container"
}