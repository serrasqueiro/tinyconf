#!/bin/sh
# (c)2020  Henrique Moreira (h@serrasqueiro.com)

# Call cvcommitinfo.py
# Author: Henrique Moreira, h@serrasqueiro.com

#
#	Basic wrapper for CVS commitinfo/ verifymsg
#

#MY_DIR=$(pwd -P)
MY_DIR=$(pwd)
CVS_R=$CVSROOT
CDIR=$(dirname $0)
BNAME=$(basename $0 .sh).py

[ "$CDIR" = "" ] && exit 0
[ "$CVS_R" = "" ] && CVS_R="."

python3 $CDIR/$BNAME --dir "$MY_DIR" --cvsroot $CVS_R --Repository $MY_DIR/CVS/Repository $*
RES=$?
[ "$QUIET" != "y" ] && echo "Ran $BNAME, exit status: $RES"

if [ $RES != 0 ]; then
	echo -n "::: You are trying to commit here: $MY_DIR, file: $*

press 'f' to force..."
	while :; do
		read -n 1 k <& 1
		[ "$k" = "q" ] && break
		[ "$k" = "f" ] && exit 0
		echo
		echo -n "Press 'f' to force..."
	done
	echo
	echo "Cowardly quitting."
fi

# Exit status
exit $RES
