#!/bin/bash
beth 2&> /dev/null &
PID=$!
echo $PID > pid.txt