# Fixing updates

The fleebmarket db is built by parsing posts on `/r/mechmarket`. But since posts on `/r/mecharket` are often updated to reflect the current status of the trade, parsing the subreddit's new posts is only half of the job.

Each post needs to be regularly fetched, parsed and then updated in the db to reflect the possible changes, either updating it, deleting it. All the fetching and parsing is done by an external process, which communicates with fleebmarket through an API. As mentioned in the previous post, I initially wrote the API using Django Rest Framework.

At first, all went as well as they could. But as this often happens, it turned out my update process was bugged.

----

I tried iterating fixes with DRF, but I had just experimented with FastAPI at worked, and going back to DRF made me feel like I was wasting my time: 
 
 - too many different ways to build views and routers, which made it hard to choose the right one
 - non explicit argument handling, which requires more testing
 - tests harder to write
 
After switching to FastAPI, a lot of boilerplate code was removed, which made the code easier to reason with, and allowed me to spot bugs much more easily (but I recon, having to carefully reread the code in order to port it was also a good way to catch bugs in itself).

I can now safely say that ads on fleebmarket are up to date with their counterpart on `/r/mechmarket` ! (Of course, there can be some delay. The rule of thumb that I use is that a post `X` days old should be updated every `X` hours).
