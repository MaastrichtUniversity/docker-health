#!/usr/bin/env bash
###############################################################################
#
#   Name:   retention.sh
#
#   Usage:  retention.sh -i <index-prefix> -r <retention-time> [options]
#
#   Description:
#           This script removes indices with the given index-prefix that are
#           older than <retention-time> months. Expected index format is: prefix-YYYY.MM
#
###############################################################################


### Local variables and constants #############################################
ELK_HOST=localhost
ELK_PORT=9200
RESPONSE=$(mktemp)
COUNT_OK=0
COUNT_ERR=0

OPTIONS=i:r:v:d
LONGOPTS=index-prefix,retention-time,verbose,display-logs
#log levels
ERR=1
WRN=2
INF=3
FIN=4
FNR=5
FST=6
DBG=9


LOGFILE="/var/log/retention_$(date +%Y%m%d).log"
LOGLEVEL=WRN
DISPLAY_LOGS=0

### LOCAL FUNCTONS ############################################################

#
# function: syntax [errormsg] [returnvalue]
#
# descr:    prints the syntax of this script
#
function syntax {

    if [[ -n $1 ]];then
        LOG $ERR "$1"
        echo ""
        echo "ERROR: $1"
        echo ""
    fi

    echo "SYNTAX: $0 <options>

    Remove indices with given prefix that are older than the retention time.

    Options:
        -i --index-prefix=      ; affected index prefix
        -r --retention-time=    ; number of months that this index should be retained
        -h --help               ; show this help
        -v --verbose=<ERR|WRN|INF|FIN|FNR|FST|DBG|TRC>
                                ; define the logging level (default=INF)
        -d --display-logs       ; display logs on standard output

    Example:

        $0 -i filebeat- -r 6    ; delete all indices older than 6 months with format filebeat-YYYY.MM
"
    if [[ -n $2 ]];then
        exit $2
    fi
}


#
# function:     log <LVL> <TXT>
#
# description:  writes info to the logfile, depending on logging level
#
function LOG {
    #TODO: parameter checks
    LVL=$1
    TXT=$2
    RET=$3
    LVLARR=(DUMMY ERROR  WARNING INFO   FINE   FINER  FINEST DEBUG  DEBUG  DEBUG  )
#echo -e "\e[34m(comparing entry level ($LVL) against current LOGLEVEL ($LOGLEVEL)\e[0m"
    # write to logfile
    if [[ ${LVL} -le ${LOGLEVEL} ]];then
        if [[ ${DISPLAY_LOGS} -lt 2 ]];then
            echo -e "$(date) | ${LVLARR[$LVL]}| ${TXT}" >>${LOGFILE}
        fi
        if [[ $DISPLAY_LOGS -gt 0 ]];then
            echo -e "$(date) | ${LVLARR[$LVL]}| ${TXT}"
        fi
    fi

    # in case of fatal error (returvalue set), write to output and exit
    if [[ ${LVL} == ${ERR} ]];then
        if [ ! -z ${RET} ];then
            echo -e ${TXT}
            exit ${RET}
        fi
    fi
}


#
# function:     exec <command>
#
# description:  executes a shell command with appropriate logging
#
function exec {
    cmd="$1"
    LOG $FIN "Executing command: $cmd"
    eval $cmd
    LOG $FNR "Return value: $?"
}


### Validate commandline arguments ############################################

# In case the provided logfile is not accessible for writing, write the logs to output
if [ ! -w "${LOGFILE}" ];then
    DISPLAY_LOGS=2
    echo "Cannot write to logfile ${LOGFILE}. Writing to standard out instead."
fi

# First pass command line args
! getopt --test > /dev/null
if [[ ${PIPESTATUS[0]} -ne 4 ]]; then
    LOG $ERR "I’m sorry, `getopt --test` failed in this environment." 1
fi

# -use ! and PIPESTATUS to get exit code with errexit set
# -temporarily store output to be able to check for errors
# -activate quoting/enhanced mode (e.g. by writing out “--options”)
# -pass arguments only via   -- "$@"   to separate them correctly
! PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTS --name "$0" -- "$@")
if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
    # e.g. return value is 1
    #  then getopt has complained about wrong arguments to stdout
    exit 2
fi
# read getopt’s output this way to handle the quoting right:
eval set -- "$PARSED"

# now enjoy the options in order and nicely split until we see --
while true; do
    case "$1" in
        -i|--index-prefix)
            INDEX_PREFIX="$2"
            shift 2
            ;;
        -r|--retention-time)
            RETMONTHS="$2"
            shift 2
            ;;
        -h|--help)
            syntax "" 0
            ;;
        -v|--verbose)
#            if [[ "$2" =~ "^-.*" ]];then
                case "$2" in
                    1|ERR|Err|err|ERROR|Error|error)
                        LOGLEVEL=1
                        ;;
                    2|WRN|Wrn|wrn|WARNING|Warning|warning)
                        LOGLEVEL=2
                        ;;
                    3|INF|Inf|inf|INFO|Info|info)
                        LOGLEVEL=3
                        ;;
                    4|FIN|Fin|fin|FINE|Fine|fine)
                        LOGLEVEL=4
                        ;;
                    5|FNR|Fnr|fnr|FINER|Finer|finer)
                        LOGLEVEL=5
                        ;;
                    6|FST|Fst|fst|FINEST|Finest|finest)
                        LOGLEVEL=6
                        ;;
                    7|8|9|DBG|Dbg|dbg|DEBUG|Debug|debug)
                        LOGLEVEL=9
                        ;;
                esac
                shift
#            fi
            shift
            ;;
        -d|--display-logs)
            DISPLAY_LOGS=1
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            LOG $ERR "Programming error" 3
            ;;
    esac
done

if [ -z ${INDEX_PREFIX} ]; then
    syntax "Index prefix (-i or --index-prefix) is a required parameter!" 1
fi
if [ -z ${RETMONTHS} ]; then
    syntax "Retention time (-r or --retention-time) is a required parameter!" 1
fi


### Get year and month ($YEAR, $MONTH) of last month to be deleted ############
let DIFF=${RETMONTHS}+1
YYYY=$(date +%Y --date="${DIFF} month ago")
MM=$(date +%m --date="${DIFF} month ago")


### Remove index (and repeat until beginning of that year) ####################
LOG $FIN "==========================================================="
LOG $INF "Staring retention script for ElasticSearch indexes"
LOG $FIN "  index-prefix   : ${INDEX_PREFIX}"
LOG $FIN "  retention-time : ${RETMONTHS} month(s)"
LOG $INF "Removing indexes in year ${YYYY} up to index '${INDEX_PREFIX}-${YYYY}.${MM}'"
LOG $FIN "-----------------------------------------------------------"


while [ ${MM} -gt 0 ]; do
    # generate index name
    if [ ${#MM} -eq 1 ]; then
        MM="0${MM}"
    fi
    INDEX="${INDEX_PREFIX}-${YYYY}.${MM}"

    # verify if index exist
    LOG $INF "Verify existence of index '${INDEX}'"
    RESPONSE=$(mktemp)
    exec "curl -s --head \"http://${ELK_HOST}:${ELK_PORT}/${INDEX}\" 2>&1 >${RESPONSE}"
    LOG $FIN "Response in ${RESPONSE}: \n $(cat ${RESPONSE})"

    if [[ $(grep 'HTTP/1.1 200 OK' ${RESPONSE}) ]]; then

        # index exist, so let's remove it
        LOG $INF "Removing index ${INDEX}..."
        RESPONSE=$(mktemp)
        exec "curl -s -XDELETE \"http://${ELK_HOST}:${ELK_PORT}/${INDEX}\" 2>&1 >${RESPONSE}"
        LOG $FIN "Response ($RESPONSE): \n$(cat ${RESPONSE})"

        if [[ $(grep '{"acknowledged":true}' ${RESPONSE}) ]]; then
            # successfully removed
            LOG $INF "...done"
            let COUNT_OK+=1
        else
            # failure, let's display the error
            LOG $ERR "\e[31mIndex removal FAILED:\n$(cat ${RESPONSE})\n\e[0m"
            let COUNT_ERR+=1
        fi
    else
        # this should never happen as we checked before whether the index exist...
        LOG $FIN "index ${INDEX} doesn't exist, so nothing to remove"
    fi
    LOG $FNR "reducing month value to check previous month."
    # substract one to check for indices in previous month
    let MM=${MM#0}-1
    if [ ${#MM} -eq 1 ]; then
        MM="0${MM}"
    fi
done

### Print summary and exit ####################################################
LOG $FIN "-----------------------------------------------------------"
LOG $INF "Summary of removed indices:"
LOG $INF " - \e[32m${COUNT_OK} removed succesfully\e[0m"
LOG $INF " - \e[31m${COUNT_ERR} failed\e[0m"
LOG $FIN "==========================================================="

exit 0
