import time
import os
import datetime
import itertools
import cookielib
import urllib2
import urllib

# Logins Must be Premium Crossword Logins
# http://www.nytimes.com/subscriptions/games/lp3FUQQ.html
USERNAME = 'NYTIMES LOGIN EMAIL'
PASSWORD = 'NYTIMES LOGIN PASSWORD'


def login(opener):
	postData = {
                "is_continue" : False,
                "expires" : int(time.time()+300), # 5 minutes from now
                "userid" : USERNAME,
                "password" : PASSWORD,
                "remember" : True,
              }

	data = urllib.urlencode(postData)

	# Sets Login Cookies
	login_url = 'https://myaccount.nytimes.com/auth/login'
	resp = opener.open(login_url, data)
	return


def scrape_crosswords(opener, start_day=0, end_day=100):
	now = datetime.datetime.utcnow() - datetime.timedelta(days=start_day)
	date_generator = (now - datetime.timedelta(days=x) for x in itertools.count())

	# Download Last (end_day-start_day) crosswords
	for x in xrange(start_day, end_day):

		# get previous day
		d = date_generator.next()

		file_name = '%s.pdf' % (d.strftime('%b%d%y'))
		save_dir = os.path.join('crosswords', '%s' % d.strftime('%A'))
		if not os.path.exists(save_dir):
			os.makedirs(save_dir)
		file_path = os.path.join(save_dir, file_name)

		# create and fetch URL
		url = 'http://www.nytimes.com/premium/xword/%(year)d/%(month)s/%(day)s/%(name)s'
		target_url = url % {  'year': d.year, 'month':str(d.month).zfill(2), 
							  'day' :  str(d.day).zfill(2), 'name' : file_name}
		resp = opener.open(target_url)
		
		# write pdf
		with open(file_path, 'w') as fp:
			# TODO verify that this is actually a crossword being returned
			fp.write(resp.read())
		
		print "Saved %s" % file_path

		# Add some intervals so it doesnt get blocked
		time.sleep(2)


def main():
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	login(opener)
	scrape_crosswords(opener, 0, 100)

main()

