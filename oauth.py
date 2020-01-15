import random
import string
import time
import urllib
import urllib2
from urlparse import urlparse

import hmac
import hashlib

"""

I tested this script on Python 2.7.1.  I am quite a Python beginner, so I apologize if it doesn't work on your setup.
The goal was to make OAuth simple, without having crazy dependancies and setup, which was difficult for someone on their
second day of Python.

Instructions:

	1) Just fill in the consumer_token, consumer_token_secret, access_token, and access_token_secret.  You can find all of these on Twitter.
	2) Create a dictionary containing all of the request parameters, from GET and POST.  Here is an example:
		
		params = {

			"status": 'hi%20there.',
			"in_reply_to_status_id": '14564648'

		};

		** Make sure to encode all of the values (and keys?)

	3) Decide on your URL (feel free to include GET variables and whatnot, the full URL works), and method.
	4) Call oauth.headerStringForRequest(url, params, method) to receive the string that you should use for the Authorization header.  Here's an example:
		
		params = {

			"status": 'hi%20there.',
			"in_reply_to_status_id": '14564648'

		};

		authHeaderString = oauth.headerStringForRequest('https://api.twitter.com/1/statuses/update.json', params, 'post');

	5) Use that header string in your request.  Here's an example with urllib2:

		# every parameter in your request, including GET and POST values
		params = {
			
			"status": 'hi%20there.'

		};

		post_params = {
			
			"status": 'hi there.'

		};

		url = "https://api.twitter.com/1/statuses/update.json";
		method = 'post';

		authHeader = oauth.headerStringForRequest(url, params, method);
		headers = { "Authorization": authHeader };

		post_params = urllib.urlencode(post_params);

		request = urllib2.Request(url, post_params, method);
		response = urllib2.urlopen(request);
		response_string = response.read();
		response.close();

		print response_string;

** If something is not working for you, create a sample signature in the Twitter OAuth interface at dev.twitter.com.  Then,
   override the timestamp() and generateNonce() methods with what Twitter generates, and see what the differences are.  Here
   is what I log for testing, and then compare against what Twitter gives me:

   print '\n';
   print oauth.signatureBaseForRequest(url, params, method);
   print '\n';
   print oauth.headerStringForRequest(url, params, method);
   print '\n';

Enjoy!
~ Aaron

"""

consumer_token         = "tmbIPo9juHGBksKr4R1wnQ";
consumer_token_secret  = "BCp4BFuPoD5NOqNPYKb7qfcs5NsYpeKCsBDQFuPNOKE";

access_token           = "625999961-2V4CPYiUJ4YgHnVoYDZ0fDxYBruWBRZ33O9OdFeb";
access_token_secret    = "QbUcb4JHOebNl352oWPagzXL95ZGIAJimovBDCqa0";

def timestamp():

	return int(round(time.time()));

def generateNonce():

	nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32));

	return nonce;

def signatureBaseForRequest(url, params, method):

	param_string = "";

	sorted_keys = sorted(params.iterkeys());
	for key in sorted_keys:
		
		string = key + "=" + params[key];
		if param_string.__len__() > 0: param_string += "&" + string;
		else: param_string = string;

	params = urllib.quote_plus(param_string);

	url = urlparse(url);
	url = "https://api.twitter.com" + url.path;
	url = urllib.quote_plus(url);

	method = method.upper();

	signature_base = method + "&" + url + "&" + params;

	return signature_base;

def signingKey():

	return consumer_token_secret + "&" + access_token_secret;

def signSignature(signature_base, signing_key):

	digest = hmac.new(signing_key, signature_base, hashlib.sha1).digest();

	signature = digest.encode('base64','strict');
	signature = signature[:-1]; # remove newline

	return signature;

def signatureForRequest(url, params, method):

	signature_base = signatureBaseForRequest(url, params, method);

	signature = signSignature(signature_base, signingKey());

	return signature;

def headerDictionaryWithoutSignature():

	headers = {};
	headers["oauth_consumer_key"] = consumer_token;
	headers["oauth_nonce"] = generateNonce();
	headers["oauth_signature_method"] = "HMAC-SHA1";
	headers["oauth_timestamp"] = str(timestamp());
	headers["oauth_token"] = access_token;
	headers["oauth_version"] = "1.0";

	return headers;

def headerStringForRequest(url, params, method):

	headers = headerDictionaryWithoutSignature();

	for key in headers.iterkeys():
		params[key] = headers[key];

	headers["oauth_signature"] = signatureForRequest(url, params, method);
	headers_keys = sorted(headers.iterkeys());

	headerString = "OAuth ";

	for key in headers_keys:

		value = headers[key];

		string = urllib.quote_plus(key) + "=\"" + urllib.quote_plus(value) + "\", ";
		headerString += string;

	headerString = headerString[:-2]; # remove the ", "

	return headerString;