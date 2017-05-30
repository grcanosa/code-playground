#!/bin/bash

REPONAME="grnas"
REPOSSH="root@XXX"
REPOGENDIR="/volume1/backup/gitproyects/"



function addREPO
{
    echo "Adding remote REPO $1 in $2"
    git remote add $1 $2
}

function remoREPO
{
	echo "Removing remote $1"
	git remote rm $1	
}

function pushREPO
{
echo "Pushing all refs to repo "
expect <<-DONE
	set timeout 45
	spawn git push --all $REPONAME
	expect {
	"*?assword:*"   {send -- "$1\r";}
	}
	set timeout -1
	expect { eof {send -- "\r"} }
DONE

}


function announceREPO
{
echo "++++++++++++++++++++++++++++++++++"
echo "+ Updating $1 "
echo "++++++++++++++++++++++++++++++++++"
}


read -s -p "Password to $REPOSSH: " MYPASS
echo

#RTPS

cd RTPS_MERGE
announceREPO "RTPS"
addREPO $REPONAME $REPOSSH:$REPOGENDIR"RTPS.git"
pushREPO $MYPASS
remoREPO $REPONAME
