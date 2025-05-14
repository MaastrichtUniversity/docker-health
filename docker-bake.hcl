# Variables section
variable "ENV_TAG" {
  default = "latest"
}

variable "MAVEN_VERSION" {
  default = "3.9.5"
}

group "default" {
  targets = ["transform-rest", "federation-api", "test-federation-api", "etl-zib", "etl-zib-rest", "test-single-node", "jupyter-zib", "portal"]
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
    MAVEN_VERSION = "3.9.5"
  }
  dockerfile = "Dockerfile"
  tags = ["docker-health/transform-rest:${ENV_TAG}"]
  context = "./externals/dh-hdp-transform-rest"
}

target "federation-api" {
  target = "rest"
  dockerfile = "Dockerfile"
  tags = ["docker-health/federation-rest:${ENV_TAG}"]
  context = "./externals/dh-hdp-federation-api"
}

target "test-federation-api" {
  target = "test"
  dockerfile = "Dockerfile"
  tags = ["docker-health/federation-test:${ENV_TAG}"]
  context = "./externals/dh-hdp-federation-api"
}

target "etl-zib" {
  inherits = ["_hdp_templates"]
  target = "pipeline"
  dockerfile = "Dockerfile"
  tags = ["docker-health/etl-zib:${ENV_TAG}"]
  context = "./externals/dh-hdp-etl"
}

target "etl-zib-rest" {
  inherits = ["_hdp_templates"]
  target = "rest"
  dockerfile = "Dockerfile"
  tags = ["docker-health/etl-zib-rest:${ENV_TAG}"]
  context = "./externals/dh-hdp-etl"
}

target "test-single-node" {
  inherits = ["_hdp_templates"]
  target = "test"
  dockerfile = "Dockerfile"
  tags = ["docker-health/etl-zib-test:${ENV_TAG}"]
  context = "./externals/dh-hdp-etl"
}

target "jupyter-zib" {
  inherits = ["_hdp_templates", "_src_etl"]
  args = {
    DATA = "zib"
  }
  dockerfile = "Dockerfile"
  tags = ["docker-health/jupyter-zib:${ENV_TAG}"]
  context = "./externals/dh-hdp-notebooks"
}

target "portal" {
  dockerfile = "Dockerfile"
  target = "development"
  tags = ["docker-health/portal:${ENV_TAG}"]
  context = "./externals/dh-hdp-portal"
}
