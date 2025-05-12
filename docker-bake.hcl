# Variables section
variable "ENV_TAG" {
  default = "latest"
}

variable "MAVEN_VERSION" {
  default = "3.9.5"
}

variable "ENV_REGISTRY_HOST" {
  default = "registry.prod.dh.unimaas.nl"
}

group "default" {
  targets = ["transform-rest", "federation-api", "etl-zib", "jupyter-zib", "portal"]
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

target "federation-api" {
  inherits = ["_src_etl"]
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/federation-api:${ENV_TAG}"]
  context = "./externals/dh-hdp-federation-api"
}

target "etl-zib" {
  inherits = ["_hdp_templates"]
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/etl-zib:${ENV_TAG}"]
  context = "./externals/dh-hdp-etl"
}

target "jupyter-zib" {
  inherits = ["_hdp_templates", "_src_etl"]
  args = {
    DATA = "zib"
  }
  dockerfile = "Dockerfile"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/jupyter-zib:${ENV_TAG}"]
  context = "./externals/dh-hdp-notebooks"
}

target "portal" {
  dockerfile = "Dockerfile"
  target = "development"
  tags = ["${ENV_REGISTRY_HOST}/docker-health/portal:${ENV_TAG}"]
  context = "./externals/dh-hdp-portal"
}
