import urllib
import json
import os
import sys
import time
from datetime import date

from IPython.Debugger import Tracer; debug_here = Tracer()

# how may images should we get?
im_from = '0'
im_to = '20'

yql_url = 'http://query.yahooapis.com/v1/public/yql?'

# the YQL yery - change it to reflect the images you want
query = 'SELECT id, secret, farm, server '\
		'FROM flickr.photos.search(' + im_from + ',' + im_to + ') '\
		'WHERE text = "shadow" '\
		'AND license = "1,2,4,5,7" '\
#		'AND min_taken_date = "' + date(2001, 05, 05).isoformat() + '"'
		
query_url = yql_url + 'q=' + urllib.quote(query) + '&format=json'

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

print 'downloading %s files to finish in approximately...'%(n_images)
t_total = 0
for i, im in enumerate(jsonresult['query']['results']['photo']):
	t0 = time.time()
	i += 1	# first image should have index 1 etc.
	im_url = "http://farm" + im['farm'] + '.static.flickr.com/' + im['server'] + '/' + im['id'] + '_' + im['secret'] + '_b.jpg'
	image = urllib.URLopener()
	image.retrieve(im_url, 'images\\' + im['id'] + '_' + im['secret'] + '_b.jpg')
	t_total += time.time() - t0							# total time spent downloading so far
	secs_left = int(int(n_images) - i) * t_total/(i)	# number of images left * average download time
	if ((i-1) % 5 == 0):
		m = secs_left / 60
		print '%im %.0fs'%(m, secs_left%60)
