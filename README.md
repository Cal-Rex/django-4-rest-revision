# walkthrough README
## this readme documents the steps taken in each comit to build this mock social media API

### [1. Commit 1:](#commit-1)
- Set up project
- create environment
- install django 4.0 (long-term support version)
- install cloudinary to handle static files
- install Pillow to handle image processing

### [2. Commit 2:](#commit-2)
- add a profiles app
- use django signals
    - signals explained
- create a superuser
- display a model on the admin panel

### [3. Commit 3:](#commit-3)
- add a basic serializer to the profiles app
- install rest_framework

### [4. Commit 4:](#commit-4)
- how to manually add a put request on a view
- add a detail view to the profiles app
- how to make the update form match the serializer
- info on how to use dot notation to traverse related fields in databases in serializers


<hr>

## Commit 1

1. create a new repo on [github](www.github.com)
- or, use the Codeinstitute full template: [https://github.com/Code-Institute-Org/ci-full-template](https://github.com/Code-Institute-Org/ci-full-template)
2. install Django via the CLI
    - `pip3 install django`
    - for this walkthrough, the LTS (Long Term Support) version of cjango was used. to use this, use:
        - `pip3 install 'django<4'`
3. Start a new project in the repo with django called `drf_api`, using the following command:
    - `django-admin startproject drf_api .`
        - the `.` initializes the project in the current directory
4. next, install cloudinary into the project with the following command:
    - `pip install django-cloudinary-storage`
5. install `Pillow`.
    - this library adds image processing capabilities that we need for this project. Note that it’s name starts with a capital P.
    - `pip install Pillow`
6. import the newly installed cloudinary apps (`cloudinary_storage` and `cloudinary`) into `settings.py` > `INSTALLED_APPS[]`
    - be sure to place `cloudinary_storage` **BEFORE** `django.contrib.staticfiles`
    - add `cloudinary` to the bottom of the `INSTALLED_APPS` list.
    - example of what `INSTALLED_APPS` should look like:
        ```py
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'cloudinary_storage',
            'django.contrib.staticfiles',
            'cloudinary'
        ]
        ```
7. set up `env.py` and the cloudinary environment variable
    - create a new `env.py` file
    - make sure it is included in `.gitignore`
    - add `import os` to the top of the file
    - set an environ for cloudinary using the cloudinary API key found on your cloudinary account page
        `os.environ['CLOUDINARY_URL'] = 'cloudinary://[REMOVE_THIS_AND_ADD_YOUR_API_KEY]@[REMOVE_THIS_AND_ADD_YOUR_CLOUD_NAME]'`
    - make an offline copy of your `env.py` file, incase you have to make a fresh workspace
8. next, set up a conditional in `settings.py` that if `env.py` exists, import it into settings.py
    - place this directly below `from pathlib import Path` at the tp of the file
    -   ```py
        import os

        if os.path.exists('env.py'):
            import env
        ```
9. beneath that code, retreive the cloudinary environment as an object inside a variable called `CLOUDINARY_STORAGE`:
    - `CLOUDINARY_STORAGE = {'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')}`
10. then, beneath that, define a setting for where media files will be stored:
    - `MEDIA_URL = '/media/'`
11. lastly, beneath that, add a default file storage setting:
    - `DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'`

top of `setting.py` should now look like this:
```py
from pathlib import Path
import os

if os.path.exists('env.py'):
    import env

CLOUDINARY_STORAGE = {'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')}
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SECRET_KEY_REMOVED_LOL'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary'
]
```

<br>
<hr>

## Commit 2

1. create the new app with the `startapp` command:
    - `python3 manage.py startapp profiles`
        - (`python3 manage.py startapp YOUR_APP_NAME_HERE`)
2. with the new app created, it also needs to be included in `INSTALLED_APPS` in `settings.py`:
    -   ```py
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'cloudinary_storage',
            'django.contrib.staticfiles',
            'cloudinary',

            'profiles',
        ]
        ```
3. now, in the newly created `models.py` inside `profiles.py` add a new import at the top of the file:
    - `from django.contrib.auth.models import User`
4. next, inside `models.py` create the first new database model:
    -   ```py
        class Profile(models.Model):
            owner = models.OneToOneField(User, on_delete=models.CASCADE)
            created_at = models.DateTimeField(auto_now_add=True)
            updated_at = models.DateTimeField(auto_now=True)
            name = models.CharField(max_length=255, blank=True)
            content = models.TextField(blank=True)
            image = models.ImageField(
                upload_to='images/' default='../samples/landscapes/girl-urban-view'
            )

            class Meta:
                ordering = ['-created_at']
            
            def __str__(self):
                return f"{self.owner}'s profile"
        ```

##### django signals

- event notifications
    > You can think of signals as notifications that get triggered by an event.
- can listen to the events and run a piece of code every time
    > We can listen for such Model events and have some code, usually a function, run each time that signal is received.
- we'd like to create a user profile every time a user is created
    > In our case, we would want to be notified when a user is created so that a profile can automatically be created alongside it. 
- built-in model signals:
    - pre save: `pre_save`
    - post save: `post_save`
    - pre delete: `pre_delete`
    - post delete `post_delete`

to implement:
1. import the `post_save` signal from `django.db.models.signals` at the top of `models.py`
    - `from django.db.models.signals import post_save`
2. now, beneath the `Profile` class model, add a call to `post_save`appended with the `.connect()` function, passing 2 arguments:
    - the first argument will be `create_profile`, which is the function that needs to be run every time a post is saved. 
    - the second is going to be specifiying who/what is the sender of the new data, in this case, it will be the `User` 
    - `post_save.connect(create_profile, sender=User)`
3. now, above this call, define the `create_profile` function:
    - the function has to take 4 arguments: `(sender, intance, created, **kwargs)`
    - set a conditional statement that if a profile is created, the owner of the profile should be that `User`
    - the function should look like this:
    -   ```py
        def create_profile(sender, instance, created, **kwargs):
                    # Because we are passing this function 
                    # to the post_save.connect method
                    # it requires the following arguments:
                    # 1. the sender model,
                    # 2. its instance
                    # 3. created  - which is a boolean value of 
                    #    whether or not the instance has just been created
                    # 4. and kwargs.  
                    if created:
                        # if created is True, we’ll create a profile  
                        # whose owner is going to be that user.
                        Profile.objects.create(owner=instance)
                
        # not part of the function, but this would be sitting
        # directly under it
        post_save.connect(create_profile, sender=User)
        ```
        > now every time a user is created, a signal will trigger the Profile model to be created.
4. register the `Profile` model in `admin.py` so that it will show up in the admin panel
    - `admin.site.register(Profile)`
5. before going any further, migrate the new model into the database in the CLI:
    - `python3 manage.py makemigrations`
    - `python3 manage.py migrate`
6. now, to view the model on the admin panel:
    - first create a superuser/admin
        - `python3 manage.py createsuperuser`
        - create a username and password from the command prompts
        - no need to supply an email address
7. run the server and go to admin and see if everything is working:
    - `python3 manage.py runserver`
    - append `/admin` to the url in the browser window and login with the admin credentials
    - be sure to add the workspcae url as an `ALLOWED_HOST` in `settings.py`

> Now, if we run our server, and go to /admin, we see that our first user was created. And their corresponding profile was created with a working image, well done!

8. finally, create a file containing the new project's dependencies via the CLI
    - `pip freeze > requirements.txt`
9. push the changes to github

<br>
<hr>

## Commit 3

## REST Framework Serializers

- how to write a class view to list all profiles
    - how to write a ProfileList
    - how to write an APIView
- Learn what Serializers are and why they're useful
    - what the similarities are between ModelForms and ModelSerializers
- how to write a profile model serializer

How Model Serializers work:
- similar to Django's `ModelForms`, they handle validation
- Uses similar syntax to `ModelForms`:
    - can use `Meta` class
    - can specify extra fields.
    - can use `.is_valid()` and `.save()` methods
    - Handle all the conversions between different data types

> we need a serializer to convert Django model instances to JSON. As we’ll only be working with Django Models, we’ll use model serializers to avoid data replication, just like you would use ModelForm over a regular Form. Before we write a model serializer, let’s talk a bit more about what they are: they are very similar to Django’s ModelForms, in that, they handle validation. The syntax for writing a model serializer is the same, we specify the model and fields in the  Meta class and we can specify extra fields too. We can use methods like .is_valid  and .save with serializers Additionally, they handle all the conversions between different data types.



1.  install `djangorestframework` in the CLI
    - `pip3 install djangorestframework`
    - add it to `INSTALLED_APPS` in `settings.py` below `cloudinary`, but above any manually created apps like `Profiles`
        - `'rest_framework',`
        -   ```py
            INSTALLED_APPS = [
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'cloudinary_storage',
                'django.contrib.staticfiles',
                'cloudinary',
                'rest_framework',
                
                'profiles'
            ]
            ```
2. create the first view in `views.py`, start by importing everything needed
    - import `APIView` from `rest_framework.views` at the top of `views.py`
        - `from rest_framework.views import APIView`
    -    > APIView is very similar to Django’s View  class. It also provides a few bits of extra functionality such as making sure you receive Request instances in your view, handling parsing errors, and adding context to Response objects.
    - import `Response` from `rest_framework.response`
        - `from rest_framework.response import Response`
    -    > Even though we could use Django’s HttpResponse, the Response class is specifically built for the  rest framework, and provides a nicer interface for returning content-negotiated Web API responses  that can be rendered to multiple formats.
    - import the `Profile` database model from `models.py`
         - `from .models import Profile`
3. next, use the imported `APIView` view to create a class view called `ProfileList`
    - inside it, define a get request that puts all objects in the `Profiles` table into a variable called `profiles`
    - then, in the return statement, return a `Response` with the parameter of the `profiles` variable 
    -   ```py
        class ProfileList(APIView):
            def get(self, request):
                profiles = Profile.objects.all()
                return Response(profiles)
        ```
4. map the new view to a URL in `urls.py` in the `profiles` app
    - first, import `path` from `django.urls`
    - import the `profiles` argument established in the `return Response` from `views.py`
        -   ```py
            from django.urls import path
            from profiles import views
            ```
    - next, create the `urlpatterns` list variable, and write a path for `profiles/` that renders the `ProfileList` view as a view (`as_view()`)
        -   ```py
            urlpatterns = [
                path('profiles/', views.ProfileList.as_view()),
            ]
            ```
5. map the newly made url pattern in `profiles/urls.py` into the urls of `drf_api`
    - at the top of `drf_api/urls.py` add `include` to the imports from `django.urls`
        - `from django.urls import path, include`
    - use the newly imported `include` method to write in a new path for `profiles.urls` in `drf_api/urls.py`'s `urlpatterns`
        -   ```py
            from django.contrib import admin
            from django.urls import path, include

            urlpatterns = [
                path('admin/', admin.site.urls),
                path('', include('profiles.urls')),
            ]
            ```
    > Now, if we start the server, and go to ‘profiles/’, we get an ugly error: Object of type Profile is not JSON serializable. Let's have a look at what’s happening and why we’re seeing this error. 

    > When a user posts data to our API, the following has to happen: we need that data to be deserialized, which means it needs to be converted from a data format like JSON or XML to Python native data types. 

    > Then, we have to make sure the data is valid (just like with Django forms) once it’s validated, a model  instance is saved in the database.

    > If our users are requesting data from our API, a queryset or model instance is returned from the database. It is then converted to Python native data types before the data is sent back, it is converted again, or serialized to a given format (most commonly JSON). 
    
    > This is the reason we saw the error. The profiles can’t be just thrown in as a part of the Response, we need a serializer to convert Django model instances to JSON.  

6. create a new file, `serializers.py` in the `profiles` app.
7. in the new file, import the following:
    - `serializers` from `rest_framework`
    - `Profile` from `.models`
    -    ```py
        from rest_framework import serializers
        from .models import Profile
        ```
8. create a class with the name `ProfileSerializer` that inherits from `serializers.ModelSerializer` and create a `ReadOnlyField` from `serializers` called `owner`, it should contain the parameter `source='owner.user`
    - give it a `Meta` class and specify the following fields to include in the response
        - `model = Profile`
        - `fields = []`
            - the value for fields can be determined in 2 ways:
            - > You could list them  all in an array or set to ‘__all__’ like this, however I prefer to be explicit about which  fields I am including, because I might want to add another field to my Profile model later  on, that I don’t want included in the serializer.
                1. `fields = '__all__'`
                2. `fields = ['id', 'owner', 'created_at', 'updated_at', 'name', 'content', 'image']`
                    - > Please note, that when extending Django's model class using models.models, the id field is created automatically without us having to write it ourselves. If we want it to be included in the response, we have to add it to the serializer's field array.
    -   ```py
        from rest_framework import serializers
        from .models import Profile

        class ProfileSerializer(serializers.ModelSerializer):
            owner = serializers.ReadOnlyField(source='owner.username')

            class Meta:
                model = Profile
                fields = [
                    'id',
                    'owner',
                    'created_at',
                    'updated_at',
                    'name',
                    'content',
                    'image'
                ]
        ```

9. return to `views.py` and import the newly made `ProfileSerializer` class
    - `from .serializers import ProfileSerializer`
10. then, in the `ProfileList` class in `views.py`, add a new instance called `serializer`, which makes a call to the newly imported `ProfileSerializer` class at the top of the file, it should contain 2 arguments:
    1. first should be the `profiles` variable containing `all` the `Profile` `objects`
    2. second, should be `many=True` to specify that multiple profile instances are to be serialized
11. in the return statement of `ProfileList`, update the `response` parameter with the value of `serializer.data`
    -   ```py
        from django.shortcuts import render
        from rest_framework.views import APIView
        from rest_framework.response import Response
        from .models import Profile
        from .serializers import ProfileSerializer

        class ProfileList(APIView):
            def get(self, request):
                profiles = Profile.objects.all()
                serializer = ProfileSerializer(profiles, many=True)
                # this takes the objects in profiles and runs it through the
                # ProfileSerializer defined in serializers.py
                # it takes this data, then takes the `Profile` model as a reference
                # and then renders the specified fields within the passed-in
                # dataset into JSON data
                return Response(serializer.data)
        ```
12. check this is all working by running the preview and appending the preview url with `/profiles/`
    - `python3 manage.py runserver`
    - if running correctly, a django REST page should appear, displaying JSON data objects of all the profiles existing within the app. 
    - > we can see the array being returned in a nice user  interface created by rest framework. If we click on the GET json button, we’ll see plain JSON,  which is exactly what a React application would see. Our serializer has taken the Python data and converted it into JSON, which is ready for the front end content to use! 
    
13. > Before we finish, let’s update our dependencies.
    - update `requirements.txt` in the terminal
        - `pip3 freeze > requirements.txt`

<br>
<hr>

## Commit 4

## Populating Serializer ReadOnly Field using dot notation

- The `source` attribute and its string value explained
- how to manipulate ReadOnlyFields (using dot notation)
    - targeting subfields within data models / tables

Entity relationship between the `User` table that comes with Django, and the `Profile` table created in this project:

> The User and Profile tables are connected through the owner OneToOne field.

> By default, the owner field always  returns the user’s id value.

|       US | ER      | < - > |     PRO | FILE     |
| -------: | :------ | :---: | ------: | :------- |
|          |         |       | id      | BigAuto  |
|       id | BigAuto |  -- > | owner   | OneToOne |
| username | Char    |       | name    | Char     |
| password | Char    |       | content | Text     |
|          |         |       | image   | Image    |

> For readability’s sake, however, every time we fetch a profile, it makes sense to overwrite this default behaviour  and retrieve the user’s username instead.  

|        US|ER       | < - > |      PRO|FILE      |
| -------: | :------ | :---: | ------: | :------- |
|       id | BigAuto |       | id      | BigAuto  |
| username | Char    |  -- > | owner   | OneToOne |
| password | Char    |       | name    | Char     |
|          |         |       | content | Text     |
|          |         |       | image   | Image    |

> To access this field, we use dot notation.

**inside serializers.py, in the `ProfileSerializer` class**
```py
owner = serializers.ReadOnlyField(
    source='owner.username'
)
```
> In this case, the “owner” in “owner.username”  stands for the user instance, so any time we want to access a field we simply use dot notation.  

basically `owner` can act as a direct call to that specific user, and using dot notation from `owner` would be the same as `User.AWAYTOIDENTIFYASPECIFICUSER.WHATEVERFIELD`

Now, lets add a 3rd table for `posts`

|        US|ER       | < - > |       PO|ST           | < - > |      PRO|FILE      |
| -------: | :------ | :---: | ------: | :---------- | :---: | ------: | :------- |
|       id | BigAuto |       |      id | BigAuto     |       | id      | BigAuto  |
| username | Char    | < - > |   owner | Foreign Key | < - > | owner   | OneToOne |
| password | Char    |       |   title | Char        |       | name    | Char     |
|          |         |       | content | Text        |       | content | Text     |
|          |         |       |   image | Image       |       | image   | Image    |

> Let’s assume we are working  on PostSerializer instead of ProfileSerializer like we did in the previous video.

In these tables, `Post.owner` is a `ForeignKey` field, this means if the there was a serializer serializing information from `Post`, the name of a user could be found by dot notation, by going through `owner`(which is targeting the user through it being na instance) then `Profile`, so the dot notation would be `owner.Profile.name`.

```py
class PostSerializer(serializers.ModelSerializer):
    profile_image = serializers.ReadOnlyField(
        source='owner.profile.name'
    )
```

> One last challenge. Let’s say we wanted to add the profile image field to each post.

|        US|ER       | < - > |       PO|ST           | < - > |      PRO|FILE      | subfields |
| -------: | :------ | :---: | ------: | :---------- | :---: | ------: | :------- | :-------: |
|       id | BigAuto |       |      id | BigAuto     |       | id      | BigAuto  |           |
| username | Char    | < - > |   owner | Foreign Key | < - > | owner   | OneToOne |           |
| password | Char    |       |   title | Char        |       | name    | Char     |           |
|          |         |       | content | Text        |       | content | Text     |           |
|          |         |       |   image | Image       |       | image   | Image    | url       |

Because the `profile.image` field comtains a "subfield" housing the `url` for the image, that needs to be targeted directly in the dot notation.

```py
class PostSerializer(serializers.ModelSerializer):
    profile_image = serializers.ReadOnlyField(
        source='owner.profile.image.url'
    )
```

______________________________________________________________________

## GET and PUT requests (Profile Details view)

Profiles CRUD Table:
> Let’s have a look at our CRUD table. It shows what kind of HTTP request our users have to make and to which URL in order to list all profiles, create, read, update or delete the profile. 

| HTTP           | URI           | CRUD Operation                                                                   | View Name         |
| :------------: | :-----------: | :------------------------------------------------------------------------------: | :---------------: |
| **a**.GET / **b**.POST | /profiles     | **a**.list all profiles / **b**.create a profile                         | LIST              |
| **c**.GET / **d**.PUT / **e**.DELETE | /profiles/:id | **c**.retrieve a profile by id / **d**.update a profile by id / **e**.delete a profile by id | DETAIL           |

quick recap reference to the ProfileList view to help write the next code:
```py
class ProfileList(APIView):
    """
    List All profiles
    No Create view (POST method), as profile creation is
    handles by Django signals
    """
    def get(self, request):
        profiles = profile.objects.all()
        serializer = ProfileSerializer(profles, many=True)
        return Response(serializer.data)
```
while this class handles `GET`ting a list of all profiles, it doesn't `POST` data/create new profiles.
This is because profile creation is handled by [django signals](#django-signals), referenced earlier.

there is still no: 
- `GET` method to retreive a specific profile by id
- view or methods to utulise `PUT`, which updates data (a profile) by id

### creating the `ProfileDetail` view

the view needs to:
1. fetch the profile by id
2. serialize the profile model instance
3. return serializer data in the response
    - ([serializer](#rest-framework-serializers) needed to turn the data into JSON format)


#### Retreiving an existing profile
steps:
1. Go to `views.py`
2. create a new class called `ProfileDetail` that inherits from the [imported `APIView`](#rest-framework-serializers)
3. create a `get_object` request that takes `self` and `pk` (PrimaryKey) as arguments
    - this function not only has to try and retreive a data record by the parameters above, it also needs to handle the instance of when a record doesnt exist
    - because of this, add an except/exception block by using the `try` keyword
    - inside the block, add a variable called profile that queries the `objects` of `Profile` to `get` a record where `pk` = the `pk` entered in the request.
    -   ```py
        class ProfileDetail(APIView):
            def get_object(self, pk):
                try:
                    profile = Profile.objects.get(pk=pk)
                    return profile
        ```
    - this handles the instance of where the record exists, now the code needed to handle the exception needs to be added 
4. Create the code that handles the event of a record not existing
    - at the top of the file (`views.py`), import `Http404` from `django.http`
        - `from django.http import Http404`
    - then, back in the `ProfileDetail` class, add an `except` statement to the `try` statement.
        - this is structured like `if`/`else`
        - the `except`ion should handle the event of `Profile.DoesNotExist`
        - the action it takes in this event is to `raise` a call to `Http404`
        -   ```py
            class ProfileDetail(APIView):
                def get_object(self, pk):
                    try:
                        profile = Profile.objects.get(pk=pk)
                        return profile
                    except Profile.DoesNotExist:
                        raise Http404
            ```
5. now that the records have been checked to make sure the profile exists, the queried profile now needs to be serialized:
    - beneath the `get_object` request, write a new `get` request that takes `self`, the `request`, and `pk` (primary key) as arguments
    - create a variable called `profile` with the value being the `get_object` function declared above, being called on it`self`, taking the `pk` as the argument
        - `profile = self.get_object(pk)`
    - create a variable called `serializer`, its value should be a call to the [`ProfileSerializer`](#rest-framework-serializers) with the `profile` variable as its argument
        - > unlike in `ProfileList` No need to pass in many=True, as unlike last time, we’re dealing with a single profile model instance and not a queryset.
    - with the profile now serialized, return it in the `Response` for the `get` request:
    -   ```py
        class ProfileDetail(APIView):
            def get_object(self, pk):
                try:
                    profile = Profile.objects.get(pk=pk)
                    return profile
                except Profile.DoesNotExist:
                    raise Http404
            
            def get(self, request, pk):
                profile = self.get_object(pk)
                serializer = ProfileSerializer(profile)
                return Response(serializer.data)
        ```
6. test that this code is working by adding the `DetailView` to the `urlpatterns` in `urls.py`:
    - under the list view, add a new `path` that takes the arguments of:
        - the path for the url as a string value that calls the the `profiles` path, but then in `<>` the `pk` as an `int`eger, suffixed with a `/`
            - `'profiles/<int:pk>/'`
        - the `ProfileDetail` view from `views` as a view, using `as_view()`
            - `views.ProfileDetail.as_view()`
    -   ```py
        urlpatterns = [
            path('profiles/', views.ProfileList.as_view()),
            path('profiles/<int:pk>/', views.ProfileDetail.as_view())
        ]
        ```
    - run the app to see if it all works.
        - `python3 manage.py runserver`


#### Updating an existing profile
process:
1. fetch the profile by it's id
    - > First, we’ll have to retrieve the  profile using the get_object method. 
2. call the serializer with the profile and request data
    - > Next, we’ll have to call our serializer with that instance and data that’s being sent in the request.
3. if data is valid, save and return the instance
    - > Then, we’ll call .is_valid on our serializer, just like we would on a form, to make sure the data is valid. If it is, we’ll save the updated profile to the database and return it in the Response. In case it isn’t, we’ll have to return a 400 BAD REQUEST error.

steps:
1. inside the `profileDetail` class in `views.py`, define a `put` request that takes `self`, the `request` and the `pk` (PrimaryKey) as arguments
    - define the `profile` variable again like in the `get` request, where the variable's value is running the `get_object` function on it`self`, taking the `pk` as an argument
    - define the serializer variable again using the `ProfileSerializer` as its value, this time though, it should take 2 arguments:
        - `profile`
        - `data=request.data` which is taking the form data from the request passed in
    - now check `if` the value of `serializer` `is_valid()`, with an `if statement`, if it is, `save()` `serializer`
    - `return` a `Response` with the parameter of the `serializer`'s `data`
    - instead of an `else` statement, add a `return` statement in place of an `else` statement, which `return`s a `Response` with 2 arguments:
        1. any `errors` created by the `serializer`
        2. a `status` parameter imported from `rest_framework`, that has the value of `status.HTTP_400_BAD_REQUEST`
            - be sure to - `from rest_framework import status` - at the top of `views.py`
    -   ```py
        def put(self, request, pk):
            profile = self.get_object(pk)
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ```

> Ok, that's all! Let’s make sure our new  view is working! If we go to ‘profiles/id/’, we’ll see PUT among the allowed HTTP methods.  We’ll also have a text area in which we could write raw JSON to update the profile. But wouldn’t it be better to have a nice form instead?

2. make the newly created form in the ProfileDetail view contextual by setting the `serializer_class` to `ProfileSerializer` in the `ProfileDetail` class, as the first line under the class definition:
    - this tells the `APIView` template being used by `ProfileDetail` to follow the field structure of the `ProfileSerializer` for its forms
    -   ```py
        class ProfileDetail(APIView):
            # establish the form structure for the data
            serializer_class = ProfileSerializer

            def get_object(self, pk):
                """
                the function that checks the validity
                of a profile request, returns an error if
                invalid
                """
                try:
                    profile = Profile.objects.get(pk=pk)
                    return profile
                except Profile.DoesNotExist:
                    raise Http404
            def get(self, request, pk):
                """
                uses the function above to get a profile by id
                serializes it using the ProfileSerializer
                """
                profile = self.get_object(pk)
                serializer = ProfileSerializer(profile)
                return Response(serializer.data)

            def put(self, request, pk):
                """
                updates a retreived profile with data receieved
                from a request via a form contextualised by
                serializer_class at the top of this view
                handles BAD_REQUEST errors too
                """
                profile = self.get_object(pk)
                serializer = ProfileSerializer(profile, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ```