#!/bin/bash

source ./env_files/zib-templates.env

ENV_FILE="env_files/zib-templates.env"

create_dynamic_template_variables() { # $1 __ID
    # Only append variables which don't exist in the env file
    ZIB_NAME=$1; ZIB_NAME="${ZIB_NAME#*-}"; ZIB_NAME="${ZIB_NAME//-/}"
    if ! [[ -n $1 ]]; then
      echo "Parameter \$1 does not exist or is empty."
      return 0
    fi
    if ! grep -q "^TEMPLATES__${ZIB_NAME^^}__API_ROUTE=" ${ENV_FILE}; then
      echo TEMPLATES__${ZIB_NAME^^}__API_ROUTE="${ETL_PROJECT_NAME}/${ZIB_NAME}" >> ${ENV_FILE}
    else
      echo "Variable TEMPLATES__${ZIB_NAME^^}__API_ROUTE aldready exist."
    fi
    if ! grep -q "^TEMPLATES__${ZIB_NAME^^}__FILENAME=" ${ENV_FILE}; then
      local YEAR=$(echo $1 | grep -o '[0-9]\{4\}')
      echo TEMPLATES__${ZIB_NAME^^}__FILENAME="data/templates/${YEAR}/$1.opt" >> ${ENV_FILE}
    else
      echo "Variable TEMPLATES__${ZIB_NAME^^}__FILENAME aldready exist."
      return 0
    fi
    echo "Succesfully generated TEMPLATES__${ZIB_NAME^^}__API_ROUTE and TEMPLATES__${ZIB_NAME^^}__FILENAME variables."
    return 0
}

create_dynamic_template_variables ${TEMPLATES__PATIENT__ID}
create_dynamic_template_variables ${TEMPLATES__ALCOHOLGEBRUIK2023__ID}
create_dynamic_template_variables ${TEMPLATES__ALCOHOLGEBRUIK2017__ID}
create_dynamic_template_variables ${TEMPLATES__BURGERLIJKESTAAT2023__ID}
create_dynamic_template_variables ${TEMPLATES__BURGERLIJKESTAAT2017__ID}
create_dynamic_template_variables ${TEMPLATES__CONTACTPERSOON2017__ID}
create_dynamic_template_variables ${TEMPLATES__WOONSITUATIE2017__ID}
