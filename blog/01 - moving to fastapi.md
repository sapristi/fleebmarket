Disclaimer: I have very little experience with Django Rest Framework, so it's very likely that I missed some of it's subleties.

-----

Fleebmarket needs some maintenance API; it is mostly used to keep the database up to date with posts from `/r/mechmarket`. Since I was using Django, I initially used Django Rest Framework to implement the API. The experience was OKish:

Pros: 

 - plays nicely with django models and forms

And... that was pretty much all that I really appreciated in it. Since the API was very custom, it did not play very nicely with any of the predefined ViewSets / ModelViewSets. I ended up with a ViewSet aggremented with some additional views, which would have been almost OK, was it not for another pretty bad experience with testing. It seemed to me every testcase needed some extra codelines for the sake of it, clunky arrangement with routing in order to match the testclient with endpoints, and so on.

-----

In contrast, switching to FastAPI felt like a breeze: 

 - explicit arguments for views, instead of manually extracting arguments from query parameters
 - autocompletion coming from Pydantic models
 - easy and clear testing with very little overhead
 - human readable description of the API thanks to the OpenAPI docs generation (that you can even use as a maintenance API, from your browser !)
 
The only « not so great » thing with FastAPI / Pydantic is the way the different models are defined. In Django, you define a model, and then you can derive models / forms / views and whatnot by specifying which fields you are interested in. This is the other way around with FastAPI / Pydantic, since typing / autocompletion needs models to be defined explicitely. This leads to end-models (the ones you actually use) not having most of their fields in their definition, but instead inheriting from other base models.

Note: It should not be too hard to implement a way to derive Pydantic models from a base model and a subset of it's fields, but then you'd loose the nice integration with editors and type checking.

In order to integrate FastAPI with Django, I took inspiration from [https://github.com/kigawas/fastapi-django][1]. It turned out to be much easier than I first thought:

 - inside a local Django app, instead of writing django views, declare some fastapi router, with your API views. Since I used syncronous views, I could mostly copy/paste my previous code. The Django ORM "just works" ! (with some quirks, see below).
 - in the `asgi.py` file (should be created by default in django 3.2), add a FastAPI app, with the router from your app.
 - mount the Django app into the FastAPI app
 - serve your app with uvicorn
 
There were two issues, not so difficult to handle:
 
 - in order to run the app in development mode, you cannot use `manage.py runserver` anymore. This could be an issue when serving staticfiles, but `whitenoise` handles this pretty well
 - It seems there is an issue with database connections not being properly closed (see [https://github.com/tiangolo/fastapi/issues/716][2]). The problem was solved with calling `django.db.close_old_connections()` in a router dependency (so that it gets called before each view).


  [1]: https://github.com/kigawas/fastapi-django
  [2]: https://github.com/tiangolo/fastapi/issues/716
