#!/bin/sh

run_py()
{
    echo "${@:2}" | xargs python3
}

run_rust()
{
    $action=$0
    if [ "$action" = 'run' ]
    then
        echo "${@:3}" | rustc --out-dir=./bin/
    else
        echo "${@:2}" | rustc --out-dir=./bin/
    fi
}

lang=$1
case $lang in
    "rust") echo "${@:2}" | xargs rustc --out-dir=./bin/
        ;;
    "py") echo "${@:2}" | xargs python3
        ;;
    *) echo "Language not recognized";
        ;;
esac
