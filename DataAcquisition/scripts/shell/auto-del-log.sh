#!/bin/bash
find /usr/local/DataCollection/logs/*/ -mtime +3 -name "*.log" -exec rm -rf {} \;
find /usr/local/xxl-client/logs/jobhandler/*/*.log  -mtime +1 -name "*.log" -exec rm -rf {} \;
