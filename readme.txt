
sfgiff.py - Script For Getting Images From Flickr
made by maciejgryka.com
28/11/2010

sfgiff uses YQL to process an SQL-like query and get JSON data about matching Flickr photos.
The photos are then downloaded and placed in images/ directory next to the script file. They are named as follows: owner_id_secret_suffix.jpg
To see the photo on the authors page go to http://www.flickr.com/photos/[owner]/[id]

To get the specific images you need, modify the query as well as im_from and im_to to change the number of photos returned. 

Note that: 
- YQL restrics the maximum number of results to 5000 per query - if you need more images, you will need to process multiple queries
- all the images are have a maximum dimension of 1024px; to get the original size you will need to find o-secret (original secret) and I'm not sure how

