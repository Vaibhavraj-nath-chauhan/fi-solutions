#!/bin/bash

# Used to fetch the facebook id for the further usage
token=$1
GRAPH_URL=####
curl -i -X GET "$GRAPH_URL/me/accounts?access_token=$token" | tail -n 1 | jq '.data[0].id' | tr -d '"'