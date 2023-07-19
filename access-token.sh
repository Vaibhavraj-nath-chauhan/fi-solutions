#! /bin/bash
# creating long token from the temp token 
FB_APP_ID=####
FB_APP_SECRET=####
TEMP_TOKEN=####
GRAPH_URL=#####
curl -i -X GET "$GRAPH_URL/oauth/access_token?grant_type=fb_exchange_token&client_id=$FB_APP_ID&client_secret=$FB_APP_SECRET&fb_exchange_token=$TEMP_TOKEN"