import urllib
import json
import os
import sys
from datetime import date

from IPython.Debugger import Tracer; debug_here = Tracer()

# how may images should we get?
im_from = '0'
im_to = '15'

yql_url = 'http://query.yahooapis.com/v1/public/yql?'

# the YQL yery - change it to reflect the images you want
query = 'SELECT id, secret, farm, server '\
		'FROM flickr.photos.search(' + im_from + ',' + im_to + ') '\
		'WHERE text = "shadow" '\
		'AND license = "1,2,4,5,7" '\
		'AND min_taken_date = "' + date(2005, 01, 01).isoformat() + '"'
		
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

print 'downloading %s files...'%(n_images)
avgTime = 0
for i, im in enumerate(jsonresult['query']['results']['photo']):
	print '.',
	im_url = "http://farm" + im['farm'] + '.static.flickr.com/' + im['server'] + '/' + im['id'] + '_' + im['secret'] + '_b.jpg'
	image = urllib.URLopener()
	image.retrieve(im_url, 'images\\' + im['id'] + '_' + im['secret'] + '_b.jpg')
