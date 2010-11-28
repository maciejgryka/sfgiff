
sfgiff.py - Script For Getting Images From Flickr
made by maciejgryka.com
28/11/2010

sfgiff uses YQL to process an SQL-like query and get JSON data describing matching Flickr photos.
The photos are then downloaded and placed in images/ directory next to the script file.

To get the images you want modify the query as well as im_from and im_to limit the number of photos you want. 

Note that: 
- YQL restrics the maximum number of results to 5000 - if you want more, you will need to process separate queries.
- all the images are have a maximum dimension of 1024px; to get the original size you need to find o-secret (original secret) and I'm not sure how

