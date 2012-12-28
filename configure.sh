#!/bin/bash

## 
# auto-configure the settings of Okapi
# 1. set the dot.cshrc
# 2. set the databases directory
# 3. put the 'source dot.cshrc' into .bashrc

set -e

OKAPI_ROOT_DIR="${PWD}"
DB_DIR="${PWD}/databases"
BIB_DIR="${PWD}/bibfiles"
DOT_DIR="${PWD}/dot-files"

# Modify the dot.cshrc
DOT_FILE="${DOT_DIR}/dot.cshrc"
if [[ -f "${DOT_FILE}" ]]; then
    sed -i "/OKAPI_ROOT=/c\export OKAPI_ROOT=${OKAPI_ROOT_DIR}"\
           "${DOT_FILE}"
fi

# Modify the databases meta files
# Get all installed databases
for db in $( awk  'BEGIN { FS=" " } /^[^#]/ {print $1}' \
            "${DB_DIR}/db_avail" ); do
    sed -i "/bib_dir=/c\bib_dir=${BIB_DIR}"\
           "${DB_DIR}/${db}"
    sed -i "/ix_stem=/c\ix_stem=${BIB_DIR}/${db}"\
           "${DB_DIR}/${db}"
done

# Put the 'source dot.cshrc' to .bashrc or .zshrc
config_rc () {
    local RC_FILE
    echo "Which rc file do you want to set?"
    read -p "(1).bash_rc (2).zshrc :" rc
    case ${rc} in
        1)
            RC_FILE=".bashrc"
            ;;
        2)
            RC_FILE=".zshrc"
            ;;
        *)
            echo "Unknown rc file, please type the # again"
            config_rc
            ;;
    esac

    local OKAPI_LABEL="# Okapi environment setting"
    if [[ -z $(grep "${OKAPI_LABEL}" "${HOME}/${RC_FILE}") ]]; then
        echo "source ${DOT_FILE} # Okapi environment setting" >> \
             "${HOME}/${RC_FILE}"
        echo "export PATH=${OKAPI_ROOT_DIR}/bin:\$PATH" >> \
             "${HOME}/${RC_FILE}"
    fi
}

config_rc
