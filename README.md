App Engine application for the Udacity training course.

## Platform
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [Google Cloud Endpoints][3]

## Setup Instructions
1. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
2. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][4].
3. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
4. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
5. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][5].)
6. (Optional) Generate your client library(ies) with [the endpoints tool][6].
7. Deploy your application.

## Implementations
- Task 1:

	+ `Session`:
	
 			class Session(ndb.Model):
	   			name = ndb.StringProperty(required=True)
		    	hightlights = ndb.StringProperty()
			    speaker = ndb.StringProperty(required=True)
    			duration = ndb.IntegerProperty()
		    	typeOfSession = ndb.StringProperty()
	    		date = ndb.DateProperty()
		    	startTime = ndb.TimeProperty()

		Since we need to query for property `speaker` later, it is marked as required. `speaker` is implemented as a string because only the name of a speaker matters. `duration` is just an integer that refers to the number of hours a session will last. `startTime` means the beginning hour of a session. For example. value `14` refers to 2 pm. It doesn't involve minutes or seconds, since they are less important than hours and they seldom appear in the start time of a session. Based on `startTime` and `duration`, the start time and the end time of a session are well defined.
	
	+ `SessionForm`:
		
			class SessionForm(messages.Message):
				name = messages.StringField(1)
			    hightlights = messages.StringField(3)
			    speaker = messages.StringField(4)
			    duration = messages.IntegerField(5, variant=messages.Variant.INT32)
			    typeOfSession = messages.StringField(6)
			    date = messages.StringField(7)
			    startTime = messages.StringField(8)
			    websafeKey = messages.StringField(9)
	
		Compared with `Session`, `SessionForm` has an additional attribute `websafeKey` which is necessary to be specified in user requests. `date` and `startTime` are `StringField`s to easily accept string inputs from users. They will be converted to `Date` or `Time` objects during endpoint methods.
	
	+ `Conference` is implemented as ancestor of `Session` for fast query for all sessions in a given conference(`getConferenceSessions`). `SessionForm` tells what type the endpoints related to `Session` takes in the requests.

- Task 2:

	+ The wishlist is implemented as `sessionKeysWishlist = ndb.StringProperty(repeated=True)` in `Profile` class. `sessionKeysWishlist` consists of all session keys in a user's wishlist.

- Task 3:

	+ Two additional queries:
		1. Query for sessions by name: `getSessionsByName`
		2. Query for sessions by date: `getSessionsByDate`

    + Problem with the provided query: 
   			
   		The inequality filter involves two properties, which is not supported by the datastore. 
   		
    + Solution:
    
    	Query by typeOfSession first, then use a projection query to get around this. Please refer to the  endpoint `getSessionsYouLike`.([Reference](http://stackoverflow.com/questions/22176586/optimizing-a-inequality-query-in-ndb-over-two-properties))
   
- Task 4:

	When a new session is added to conference and there is more than one session by its speaker at this conference, a new Memcache entry `<websafeConferenceKey, [speaker, sessionNames]>` will be generated. Then the `getFeaturedSpeaker` endpoint retrieves this entry by calling `memcache.get()`.



[1]: https://developers.google.com/appengine
[2]: http://python.org
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://console.developers.google.com/
[5]: https://localhost:8080/
[6]: https://developers.google.com/appengine/docs/python/endpoints/endpoints_tool
