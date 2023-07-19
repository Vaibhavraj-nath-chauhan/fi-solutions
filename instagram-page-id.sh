token=###
fb_page_id=$(sh fb-pageid.sh $token)
GRAPH_URL=####
curl -i -X GET "$GRAPH_URL/$fb_page_id?fields=instagram_business_account&access_token=$token" | tail -n 1 | jq '.instagram_business_account.id' | tr -d '"'