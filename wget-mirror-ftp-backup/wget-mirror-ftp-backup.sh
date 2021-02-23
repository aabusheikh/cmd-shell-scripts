#!/bin/bash
if [ -f wget-mirror-ftp-backup.log ]; then
   mv wget-mirror-ftp-backup.log wget-mirror-ftp-backup.log.old
fi
{
    FTPHOSTNAME=
    FTPDIRNAME=
    FTPUSER=
    FTPPASS=
    if [ "$1" == "clean" ] || [ "$1" == "c" ] || [ "$1" == "--clean" ] || [ "$1" == "-clean" ] || [ "$1" == "-c" ]; then
        echo "Removing existing $FTPHOSTNAME"
        rm -rf $FTPHOSTNAME
    fi
    echo ""
    echo "Downloading files to $FTPHOSTNAME"
    wget -m ftp://$FTPUSER:$FTPPASS@$FTPHOSTNAME/$FTPDIRNAME/*
    if [ "$1" != "clean" ] && [ "$1" != "c" ] && [ "$1" != "--clean" ] && [ "$1" != "-clean" ] && [ "$1" != "-c" ]; then
        echo ""
        echo "Cleaning up backup directory"
        python3 wget-mirror-ftp-cleanup.py $(pwd)/$FTPHOSTNAME/$FTPDIRNAME/
    fi
    echo ""
    echo "Creating timestamped copy of $FTPHOSTNAME/$FTPDIRNAME"
    current_time=$(date "+%Y.%m.%d-%H.%M.%S")
    backup_name=$FTPDIRNAME-$current_time
    cp -R $FTPHOSTNAME/$FTPDIRNAME $backup_name
    echo "Copied to $backup_name"
} | tee wget-mirror-ftp-backup.log