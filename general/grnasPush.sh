#!/bin/bash

REPONAME="grnas"
REPOSSH="root@grcanosa.synology.me"
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

echo "Entering thirdparty"
cd thirdparty

announceREPO "IDL"
cd idl
addREPO $REPONAME $REPOSSH:$REPOGENDIR"eprosima-common/idl.git"
pushREPO $MYPASS
remoREPO $REPONAME
cd ..
announceREPO "FASTCDR"
cd fastcdr
addREPO $REPONAME $REPOSSH:$REPOGENDIR"fastcdr.git"
pushREPO $MYPASS
remoREPO $REPONAME
cd ..

announceREPO "COMMON CODE"
cd eprosima-common-code
addREPO $REPONAME $REPOSSH:$REPOGENDIR"eprosima-common/code.git"
pushREPO $MYPASS
remoREPO $REPONAME
cd ..

announceREPO "DEV ENV"
cd dev-env
addREPO $REPONAME $REPOSSH:$REPOGENDIR"eprosima-common/dev-env.git"
pushREPO $MYPASS
remoREPO $REPONAME
cd ..

cd .. #RTPS
cd .. # workspace
#fastbuffers
cd idt
announceREPO "IDT"
addREPO $REPONAME $REPOSSH:$REPOGENDIR"idt.git"
pushREPO $MYPASS
remoREPO $REPONAME
cd ..

#fastbuffers
cd fastbuffers
announceREPO "FASTBUFFERS"
addREPO $REPONAME $REPOSSH:$REPOGENDIR"fastbuffers.git"
pushREPO $MYPASS
remoREPO $REPONAME
cd ..

#ddsrecorder
announceREPO "DDSRECORDER"
cd ddsrecorder
addREPO $REPONAME $REPOSSH:$REPOGENDIR"ddsrecorder.git"
pushREPO $MYPASS
remoREPO $REPONAME
cd ..

#ddsrecorder
announceREPO "BMS"
cd bms
addREPO $REPONAME $REPOSSH:$REPOGENDIR"BMS.git"
pushREPO $MYPASS
remoREPO $REPONAME
cd ..
