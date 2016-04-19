#!/usr/local/cs/bin/bash
D=$1

#Separate hidden and non-hidden regular files
RESULT=`ls -a $D | sort` #Store all the files including hidden words into a 
#variable "RESULT" and sort them

declare -a ARRAY 
count=0

IFS=$'\n' #Every newline stands for a new file. IFS ignores sequences of spaces
#and tabs, and it treats them as part of the same file.

for FILE in $RESULT
do 
    #Check if readable
    if [ ! -r "$D/$FILE" ]
    then
	echo "Cannot read $D/$FILE" #Give error message if file is not readable
    fi

    #Check if symbolic link or hard link
    if [ ! -L "$D/$FILE" ] #if not a symbolic link (represented by -L)
    then
    
	if [ -f "$D/$FILE" ] #-f checks if it is a file
	then	    
	    ARRAY[$count]="$D/$FILE" #move file into array
	    echo "${ARRAY[$count]} is a regular file"
	    let count=count+1
	else
	    echo "$D/$FILE is not regular file" #Give an error message 
	fi
    fi
done

#Once we get all the files in the array, I will remove the duplicates in 
#lexographic order
for i in "${ARRAY[@]}"    #@ is the common syntax for an array index
do
    for j in "${ARRAY[@]}"    
    do
	if [ "$i" != "$j" ] #Check if array indices are not equal
	then
	    cmp -s -- "$i" "$j"  #"--" prevents errors with special starting 
#characters #i.e. "*", " ", "#", etc.
	    if [ $? -eq 0 ] #cmp returns 0 if identical, and "$?" evaluates the
#previous executed line. This means to check if the previous line equals 0
	    then
		ln -f -- "$i" "$j"   #Deletes previous file link and replaces 
#it with a hard link
	    fi
	fi
    done
done