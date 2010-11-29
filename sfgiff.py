# Disclaimer: this script uses the Flickr API but is not endorsed or certified by Flickr.
# It was made for research purposes only.
#
# If you run it make sure to only use the downloaded images according to their license:
# 1	Attribution-NonCommercial-ShareAlike License 	http://creativecommons.org/licenses/by-nc-sa/2.0/
# 2	Attribution-NonCommercial License 				http://creativecommons.org/licenses/by-nc/2.0/
# 3	Attribution-NonCommercial-NoDerivs License		http://creativecommons.org/licenses/by-nc-nd/2.0/
# 4	Attribution License								http://creativecommons.org/licenses/by/2.0/ 
# 5	Attribution-ShareAlike License					http://creativecommons.org/licenses/by-sa/2.0/
# 6	Attribution-NoDerivs License					http://creativecommons.org/licenses/by-nd/2.0/
# 7	No known copyright restrictions					http://flickr.com/commons/usage/
#
# maciejgryka.com
#

import urllib
import json
import os
import sys
import time
# from datetime import date

from IPython.Debugger import Tracer; debug_here = Tracer()

# how may images should we get? (maximum 5000 with a single query)
im_from = '0'
im_to = '20'

if (int(im_to) - int(im_from) > 5000):
	print 'error: maximum of 5000 images per query!'
	sys.exit(0)

# suffix controlling the size of the image
# _s	small square 75x75
# _t	thumbnail, 100 on longest side
# _m	small, 240 on longest side
#  	 	(empty) medium, 500 on longest side
# _z	medium 640 on longest side
# _b	large, 1024 on longest side
# _o	(needs special secret) original image, either a jpg, gif or png, depending on source format
im_suffix = '_b'

yql_url = 'http://query.yahooapis.com/v1/public/yql?q='

# the YQL yery - change it to reflect the images you want
query = 'SELECT id, secret, farm, server, owner '\
		'FROM flickr.photos.search(' + im_from + ',' + im_to + ') '\
		'WHERE text = "shadow" '\
		'AND license = "1,2,4,5,7" '\
#		'AND min_taken_date = "' + date(2001, 05, 05).isoformat() + '"'

query_url = yql_url + urllib.quote(query) + '&format=json'

print 'getting JSON response...'
jsonfile = urllib.urlopen(query_url)

print 'reading JSON...'
jsonresult = json.loads(jsonfile.read())

n_images = jsonresult['query']['count']
if (n_images == '0'):
	print 'no images returned by the query - exiting'
	sys.exit(0)

if (not(os.path.exists('images/'))):
	os.mkdir('images')

print 'downloading %s files...'%(n_images)
t_total = 0
for i, im in enumerate(jsonresult['query']['results']['photo']):
	t0 = time.time()
	im_url = "http://farm" + im['farm'] + '.static.flickr.com/' + im['server'] + '/' + im['id'] + '_' + im['secret'] + im_suffix + '.jpg'
	image = urllib.URLopener()
	image.retrieve(im_url, 'images\\' + im['owner'] + '_' + im['id'] + '_' + im['secret'] + im_suffix + '.jpg')
	t_total += time.time() - t0		# total time spent downloading so far + time taken by last download
	secs_left = (int(n_images) - i+1) * t_total/(i+1)	# number of images left * average download time
	time_left_str = ''
	if (i % 10 == 0):
		h = int(secs_left) / 3600
		if (h > 0):
			time_left_str += '%ih '%(h)
			secs_left = secs_left - h*3600
			
		m = int(secs_left) / 60
		if (m > 0):
			time_left_str += '%im '%(m)
			secs_left = secs_left - m*60

		print time_left_str + '%.0fs'%(secs_left)
print 'done!'