#!/bin/bash
beth 2>&1 log.txt &
PID=$!
echo $PID > pid.txt