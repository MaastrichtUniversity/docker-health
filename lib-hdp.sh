#!/usr/bin/env bash

# In case of a new server, it needs to be added here!
export envs="
tst fhml-srv016 tst-docker-hdp"

export ERR=1
export WRN=2
export INF=3
export DBG=4

#==============================================================================
# Copied from https://github.com/MaastrichtUniversity/dh-env/blob/master/lib-dh.sh on 7-11-2023
# Syntax        abort <txt> [<errno>]
#
# Params        <txt> text for logging
#		<errno> exit value (optional, default=1)
#
# Description   This function writes (txt) to stdout and aborts the script with errno
#
# Changes
# 10-07-18 | R.Niesten | Initial version
#==============================================================================
function abort {
    echo "$1"
    echo -e "\e[31mScript aborted!\e[0m\n"
    if [[ -z $2 ]]; then
        exit 1
    else
        exit $errno
    fi
}


#==============================================================================
# Copied from https://github.com/MaastrichtUniversity/dh-env/blob/master/lib-dh.sh on 7-11-2023
# Syntax        log <lvl> <txt>
#
# Params        <lvl> logging level (1=ERR, 2=WRN, 3=INF, 4=DBG)
#		<txt> text for logging
#
# Description   This function writes the log-text (txt) to stdout if the level (lvl)
#               is lower or equal to the set logging-treshold
#
# Changes
# 10-07-18 | R.Niesten | Initial version
#==============================================================================
function log {

    # validate params
    if [[ -z $1 ]]; then
        abort "${FUNCNAME[0]}: missing parameter [level]"
    fi
    if ! [[ "$ERR $WRN $INF $DBG" = *"$1"* ]]; then
        abort "${FUNCNAME[0]}: invalid value ($1) for paramter 'level'"
    fi
    loglvl=$1
    shift
    logtxt=$@
    if [[ -z "$logtxt" ]]; then
        logtxt="<no text>"
    fi

    if [[ $loglvl -le $LOGTRESHOLD ]]; then
	if [[ $loglvl == $ERR ]]; then
            prefix="\e[31mERROR: "
            postfix="\e[0m"
	elif [[ $loglvl == $WRN ]]; then
            prefix="\e[33mWARNING: "
            postfix="\e[0m"
        else
            prefix=""
            postfix=""
        fi
        echo -e "${prefix}${logtxt}${postfix}"
    fi
}


#==============================================================================
# Copied from https://github.com/MaastrichtUniversity/dh-env/blob/master/lib-dh.sh on 7-11-2023
# Syntax        run_repo_action <git-action> <repos>
#
# Params        <action>  One of the following git-actions
#		  clone  -> clones all repos
#		  pull	 -> pulls all repos
#		  status -> show git-status for all repos
#      		<reposs>  List of repos in format <repo-name><tab><repo-location>
#
# Description   Execute the given command for the provided repos
#
# Changes
# 10-07-18 | R.Niesten | Initial version
#==============================================================================
function run_repo_action {
    log $DBG "${FUNCNAME[0]} $@"

    # validate number of params
    if [[ $# -lt 2 ]]; then
        abort "${FUNCNAME[0]}: illegal number of params"
    fi

    # split 'action' in (git)action and options
    rra_action=${1/ */}               # remove all after first space
    rra_options=${1/$rra_action/}         # remaining part is first part of options
    shift
    while [[ ${1:0:6} != "extern" ]] && [[ ${1:0:6} != "docker" ]]; do
        rra_options="$rra_options $1"
        shift
    done
    rra_options="$(echo -e "${rra_options}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"    #trim surrounding spaces
    rra_externals=$1


    # validate params
    if [[ -z $rra_action ]]; then
        abort "${FUNCNAME[0]}: missing parameter [action]"
    fi
    if [[ "$rra_externals" == "" ]]; then
        log $INF "No externals provided, so action '$1' needs nothing to do"
        return
    fi

    # determin current folder name
    baserepo=$(basename $(pwd))

    # processing
    while read -r rra_external; do
        rra_external=($rra_external)
        echo -e "\e[32m=============== $baserepo/${rra_external[0]} ======================\033[0m"
        # compose git command (depending on action this might differ)
        if [[ $rra_action == "clone" ]]; then
            cmd="git clone ${rra_external[1]} ${rra_external[0]}"
        elif [[ $rra_action == "pull" ]]; then
            cmd="git -C ${rra_external[0]} pull --rebase"
        else
            cmd="git -C ${rra_external[0]} $rra_action $rra_options"
        fi
        # execute the composed git command (and set errorcode in case it failed)
        log $DBG "executing: $cmd"
        retval=0
        $cmd || retval=$?
        log $DBG "command returned: $retval"
        # show warning in case of error!
        if [[ "$retval" -gt 0 ]]; then
            log $WRN "Issue occurred while executing command '$cmd'"
        fi
    done <<< "$rra_externals"

}

#==============================================================================
#
# Syntax        env_selector <envs>
#
# Params        <envs>  List of possible envs in format <name><tab><hostname><tab><description>
#
# Description   Set the correct value to RIT_ENV based on the host-name where
#               the script is running
#
# Changes
# 10-07-18 | R.Niesten | Initial version
#==============================================================================
function env_selector {
    log $DBG "${FUNCNAME[0]} $@"
    if [[ -z $RIT_ENV ]]; then
        RIT_ENV="local"

        set +e
        while read -r env; do
            env=($env)
            if [[ $HOSTNAME == ${env[1]} ]]; then
                RIT_ENV=${env[0]}
                log $INF "\e[32m======== Environment selector ======================"
                log $INF "Running on host ${env[1]}"
                log $INF "Setting environment for ${env[2]}"
                log $INF "RIT_ENV set to $RIT_ENV"
                log $INF "====================================================\033[0m"
            fi
        done <<< "$envs"

    fi

    export RIT_ENV
}