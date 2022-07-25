#!/bin/bash
echo "----- start run.sh ----"
source env/Scripts/activate
python main.py >> system.log
echo "----- end run.sh ----"
echo ""

$SHELL