#!/usr/bin/env bash
# wait-for-it.sh

TIMEOUT=15
QUIET=0

echoerr() {
  if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi
}

usage() {
  exitcode="$1"
  cat << USAGE >&2
Usage:
  $0 host:port [-t timeout] [-- command args]
  -q | --quiet                        Do not output any status messages
  -t TIMEOUT | --timeout=timeout      Timeout in seconds, zero for no timeout
  -- COMMAND ARGS                     Execute command with args after the test finishes
USAGE
  exit "$exitcode"
}

wait_for() {
  for i in `seq $TIMEOUT` ; do
    nc -z "$HOST" "$PORT" > /dev/null 2>&1
    
    result=$?
    if [[ $result -eq 0 ]] ; then
      if [[ $QUIET -ne 1 ]] ; then echo "Wait success"; fi
      return 0
    fi
    sleep 1
  done
  echo "Operation timed out" >&2
  return 1
}

while [[ $# -gt 0 ]]
do
  case "$1" in
    *:* )
    HOST=$(printf "%s\n" "$1"| cut -d : -f 1)
    PORT=$(printf "%s\n" "$1"| cut -d : -f 2)
    shift 1
    ;;
    -q | --quiet)
    QUIET=1
    shift 1
    ;;
    -t)
    TIMEOUT="$2"
    if [[ $TIMEOUT == "" ]]; then break; fi
    shift 2
    ;;
    --timeout=*)
    TIMEOUT="${1#*=}"
    shift 1
    ;;
    --)
    shift
    break
    ;;
    --help)
    usage 0
    ;;
    *)
    echoerr "Unknown argument: $1"
    usage 1
    ;;
  esac
done

if [[ "$HOST" == "" || "$PORT" == "" ]]; then
  echoerr "Error: you need to provide a host and port to test."
  usage 2
fi

wait_for

RESULT=$?
if [[ $RESULT -ne 0 ]]; then
  exit $RESULT
fi

if [[ $# -gt 0 ]]; then
  exec "$@"
fi