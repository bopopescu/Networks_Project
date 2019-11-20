#!/bin/bash
## Build engine
sudo grunt build
## Start the AppRTC dev server from the out/app_engine directory by running the Google App Engine SDK dev server,
/home/osboxes/Documents/Networks_Project/google-cloud-sdk-271.0.0-linux-x86_64/google-cloud-sdk/bin/dev_appserver.py ./out/app_engine 
