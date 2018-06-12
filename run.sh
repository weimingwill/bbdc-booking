#!/bin/bash
echo "----- start run.sh ----"
cd ~/bbdc-booking
source env/bin/activate
python main.py >> system.log
echo "----- end run.sh ----"
echo ""
