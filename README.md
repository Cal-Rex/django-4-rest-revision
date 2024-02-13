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

### [5. Commit 5:](#commit-5)
- serializing new fields onto a view using serializer method fields
- adding authentication / logging in and out
- adding custom authentication and restrictions to data

### [6. Commit 6:](#commit-6)
- create the post app
    - create the model
    - create the list view
    - create the serializer
- add authentication and ability to post as an authenticated user

### [7. Commit 7:](#commit-7)
- create the PostDetail view
- retrieve a record by id (get)
- update a record by id (put)
- delete a record by id (delete)

### [8. Commit 8:](#commit-8)
- setting up the entire comments app using previous methods
- views made using generic views instead

### [9. Commit 9:](#commit-9)

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
<br>
<hr>

## Commit 5:

## Authentication, authorization and serializer method fields
##### https://youtu.be/bDfQdBL70oM

This section covers:
- add in-browser login/logout feature
    - > make it possible to log in and log out of our API in-browser interface
- write custom permissions
    - > write the IsOwnerOrReadOnly permission
- add an extra field to an existing serailizer
    - > add an extra field to our Profile Serializer

> We’ll do all this so that only the owner of  a profile can edit it and not just any user.


before getting started on the steps above, create another superuser, so that there are 2 accounts to work with:
- in the terminal:
    1. `python3 manage.py createsuperuser`
    2. follow terminal prompts

user created:

| Username | Password |
| -------: | :------- |
| admin2   | guest    |


with that done, begin creating the login/logout views:

These come as part of the native REST framework package:
1. add a new path to `drf_api/urls.py` that takes `api-auth/` as the path name, and uses the `include` import to include `'rest_framework.urls'`
    -   ```py
        from django.contrib import admin
        from django.urls import path, include

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('api-auth/', include('rest_framework.urls')),
            path('', include('profiles.urls')),
        ]
        ```
2. run the server and check to see if the new path works:
    - on the `/profiles/` page, there should now be a dorpdown in the top right of the page allowin users to logout/login

however, regardless of who is logged in, any user can update a record, which is not ideal.

> Luckily, not only does the rest framework come with a set of commonly used permissions, like `AllowAny`, `IsAuthenticated`, `IsAdminUser`, `IsAuthenticatedOrReadOnly` and more; it also makes it very easy to write custom permissions (`BasePermission` - used to write custom permissions)


### Creating a Custom permission

requirements for a custom permission:
1. > It has to be an object-level permission, which means we’ll have to check a Profile model instance object and see if its ‘owner’ field is  pointing to the same user who’s making the request.
2. > If the user is requesting read-only access using the so-called safe http  methods, like GET, return True.
3. > If the user is making a PUT or PATCH request, return True only if that user owns the profile object.

**steps:**
1. create a new file in `drf_api` called `permissions.py`
2. at the top of the file, import `permissions` from `rest_framework`
    - `from rest_framework import permissions`
3. then, create a new class called `IsOwnerOrReadOnly` that inherits from `permisssions.BasePermission`
    - `class IsOwnerOrReadOnly(permissions.BasePermissions):`
4. overwrite the pre-existing function `has_object_permission` supplied by the inherited import. it takes 4 arguments `(self, request, view, obj)`
    - this is done by just writing it as a new function
5. in the function:
    - add an `if` statement that checks if the `method` in the `request` argument is `in` the `SAFE_METHODS` of `permissions`. If it is, `return` a value of `True`
        - this checks to see if the user accessing the record is only requetsing Read-Only access, and if they are, the `True` result is returned
    - directly under it, in lieu of an `else` statement, add a `return` statement that has a conditional checking that `owner` in the `obj` argument matches the `request`ing `user`
        - this checks to see if the user owns that record and will return a `True` value if they match.
    -   ```py
        class IsOwnerOrReadOnly(permissions.BasePermisssions):
            def has_object_permission(self, request, view, obj):
                if request.method in permissions.SAFE_METHODS:
                    return True
                return obj.owner == request.user
        ```
6. with the permission written, it can now be used in `views.py`, import it at the top of the `views.py file`:
    - `from drf_api.permissions import IsOwnerOrReadOnly`
7. now that it is imported, permissions classes can be added to views by using the variable `permission_classes` which passes an array of all of the necessary permissions. In this case, there is only one, so pass it in as a single entry within an array/list. Add the following variable to the `ProfileDetail` view, below the `serializer_class` variable:
    - `permission_classes = [IsOwnerOrReadOnly]`
8. next, inside the `ProfileDetail` view, the `get_object` function now needs to be amended to make the function check the permissions of the accessing user:
    - > if the user doesn’t own the profile, it will throw the 403 Forbidden  error and not return the instance.
    - in the `try` statement, beneath the profile variable, run the function `check_object_permissions` on `self` with the arguments of `request` made by `self` and the `profile` variable established directly above it
        - `self.check_object_permissions(self.request, profile)`
    -   ```py
        class ProfileDetail(APIView):
        # establish the form structure for the data
        serializer_class = ProfileSerializer
        # establish the permissions for the data
        permission_classes = [IsOwnerOrReadOnly]

        def get_object(self, pk):
            """
            the function that checks the validity
            of a profile request, returns an error if
            invalid
            """
            try:
                profile = Profile.objects.get(pk=pk)
                self.check_object_permissions(self.request, profile)
                return profile
            except Profile.DoesNotExist:
                raise Http404
        def get(self, request, pk):
        ```

> now, if we don’t own the profile, we aren’t allowed to make changes to it.


### adding custom fields depending on the authentication of the user using a serializer

1. go to `profiles/serializers.py`
    - > We’re going to use the  SerializerMethodField, which is read-only. It gets its value by calling a method on the serializer class, named `get_<field_name>` (in this case, it will be `get_is_owner`).
2. in the `ProfileSerializer` class, add a new variable called `is_owner` under the `owner` variable
    - this variable will house the `SerializerMethodField` from the `serializers` import with no parameters.
        - `is_owner = serializers.SerializerMethodField()`
            - `SerializerMethodField()` is read-only
3. this new variable is then run like a function by prefixing the variable name with `get_` and defining it like a function, it will take `self` and `obj` as parameters

> we’d like to do something similar to what we did in our permission file, that is: check if request.user is the same as the object's owner. But there’s a problem. The currently logged in user is a part of the request object.

This information isn't currently directly available to the serializer in this file. So it needs to be passed into the serializer from `views.py`

> inside views.py, we’ll have to pass it in as part of the context object when we call our ProfileSerializer inside our view. We’ll have to do it every time we call it.

4. first, add a new variable into the `get_is_owner` function called `request`, its value should be `self`'s `context`, where it targets the array value of `'request'` within itself
    - this `context` needs to be created as a parameter when the serializer is called in `views.py`, but this can be added after the rest of the function is built to save jumping back and forth
5. with the `request` variable now housing the `context`ual `request` from the `user`, this can be checked against the target object to see if the `user` matches the `obj`'s `owner`
    - under the `request` write a `return` statement that has a conditional statement to reflect this:
        -   ```py
            def get_is_owner(self, obj):
                request = self.context['request']
                return request.user == obj.owner
            ```
6. now, as mentioned before, the request information needs to be sent in the `context` value from `views.py` every time this serializer is called. to do that, go to `views.py`
7. wherever `serializer = ProfileSerializer(...)` is classed as a variable, a parameter of `context` needs to be added to the parameters, its value needs to be an object KVP with a key of `'request'` with the value of `request`
    - `serializer = ProfileSerializer(profiles, many=True, context={'request': request})` (for accessing multiple records)
    - `serializer = ProfileSerializer(profiles, context={'request': request})` (for accessing a single record)
    - example:
        -   ```py
            def put(self, request, pk):
                """
                updates a retreived profile with data receieved
                from a request via a form contextualised by
                serializer_class at the top of this view
                handles BAD_REQUEST errors too
                """
                profile = self.get_object(pk)
                # serailizer updated below
                serializer = ProfileSerializer(
                    profile,
                    data=request.data,
                    context={'request': request}
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            ```
8. Lastly, include the new `'is_owner'` field in the `fields` array listed in the `Meta` class of `ProfileSerializer`
9. test that it all works

code should look like this:
```py
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
        # this variable above is used to house 
        # the requisite serializer it is called 
        # as a function below by prefixing the variable's 
        # name with 'get_'

    def get_is_owner(self, obj):
        """
        passes the request of a user into the serializer
        from views.py
        to check if the user is the owner of a record
        """
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
            'name',
            'content',
            'image',
            'is_owner'
        ]
```

<br>
<hr>

## Commit 6

### Creating a new App
run the command in the terminal to make a new app, name it `posts`
    - `python3 manage.py startapp posts`

### Creating a post model
1. in `posts/models.py` import the following:
    - `models` from `django.db`
    - `User` from `django.contrib.auth.models`
    ```py
    from django.db import models
    from django.contrib.auth.models import User
    ```

2. create a class called `Post`, it should inherit from `models.Model`
3. the new `Post` class needs the following fields:
    - owner, which should be a `ForeignKey` using the `User` as its value, it should also `CASCADE` delete any related sub-items if deleted
    - created_at, which should be a `DateTimeField` which should be automatically assigned a new value upon record creation by using the parameter `auto_now_add=True`
    - updated_at, same as above, except its paramater is `auto_now=True`, not `auto_add_now` as it updates every time the post is edited, not when it is `add`ed
    - title, should be a `CharField` with a `max_length`
    - content, should be a `TextField` to house post content, it should be `blank` initially
    - image, which should be an `ImageField`. 
        - upon a successful upload, the image should be `upload`ed`_to` `'images/'` 
        - it should also have a default value from the cloudinary database using a static filepath
        - it should also be `blank` on the form
4. add a `Meta` class that orders posts by the `DateTime` they were `created_at`, with the most recent entry being first
5. define a dunder `str` methos that returns a python `f` string that contains the `id` and `title` of each post through the use of `this`

the post model should look like this:
```py
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Post model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../samples/landscapes/girl-urban-view', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'
```

6. Migrate the completed model into the database
    1. `python3 manage.py makemigrations`
    2. `python3 manage.py migrate`


### creating a serializer

1. create a new file in `posts` called `serializers.py`
2. inside the new `serailizers` import:
    - `serializers` from `rest_framework`
    - the `Post` model from `.models`
3. create a class called `PostSerializer` which inherits from `serializers.ModelSerializer`
4. establish the following serailizer fields:
    - owner: a `ReadOnlyField` that's `source` is the `username` of the `owner` specified in the `Post` model
    - profile_id: a `ReadOnlyField` that's `source` is the `id` of the `owner` specified in the `Post` model (`id`'s are automatically created by django)
    - profile_image: a `ReadOnlyField` that's `source` is the `url` of the `image` field beonging to the `owner`, specified in the `Post` model
    - is_owner: a variable which houses the `SerializerMethodField` for the `serializer`
5. use the `is_owner` field to create a method (prefix it with `get_`) with the following parameters: `self` and `obj` for object in question
    - the function should then take a `context`ual `request` from whatever calls it (`this`), and then checks if the `user` that made the `request` matches the `obj`'s `owner`, `return`ing a voolean value depending on the outcome
6. add a `Meta` class that:
    - determines the `model` the serializer its basing its structure from, n this case it is `Post`
    - determine the `fields` it serializes and displays in a list variable as strings, they should be:
        - id
        - owner
        - created_at
        - updated_at
        - title
        - content
        - image

finished serializer shuold look like this:
```py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.id')
    profile_image = serializers.ReadOnlyField(source='owner.image.url')
    is_owner = serializers.SerializerMethodField()
        # this variable above is used to house 
        # the requisite serializer it is called 
        # as a function below by prefixing the variable's 
        # name with 'get_'
    
    def get_is_owner(self, obj):
        """
        passes the request of a user into the serializer
        from views.py
        to check if the user is the owner of a record
        """
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Post
        fields = [
            'id',
            'owner',
            'profile_id',
            'profile_image',
            'created_at',
            'updated_at',
            'title',
            'content',
            'image',
            'image_filter',
            'is_owner',
        ]
```

## Creating the PostList View
##### https://youtu.be/BIaoKcYvr_M


overview:
- create the PostList view and write two methods 
    1. ‘get’, to list all posts
    2. ‘post’ to create a user post


### Creating the PostList view
1. go to `posts/views.py`
2. import the following:
    -   ```py
        from django.shortcuts import render
        from rest_framework import status
        from rest_framework.response import Response
        from rest_framework.views import APIView
        from .models import Post
        from .serializers import PostSerializer
        ```
3. create the `PostList` class, it should inherit from `APIView`

### define the get method to list all posts
1. `def`ine the `get` method, which whould take 2 arguments: `self` and `request`
2. inside the `get` request, create a variable called `posts` that retrieves `all()` `objects` from `Post`
3. create the `serializer` variable that houses the `PostSerializer` established in `serializers.py`. pass it:
    - the `posts` variable
    - the `many` parameter, set to `True`
    - `context`, which has a {K: V} Pair of K: `'request'` V: `request`
4. have the function `return` a `response`, its parameter being the serialized `data` of the `serializer` variable
    ```py
    from django.shortcuts import render
    from rest_framework import status
    from rest_framework.response import Response
    from rest_framework.views import APIView
    from .models import Post
    from .serializers import PostSerializer


    class PostList(APIView):
        def get(self, request):
            posts = Post.objects.all()
            serializer = PostSerializer(
                posts,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data)
    ```

5. create a new `urls.py` file in the `posts` app
    - import:
        - `path` from `django.urls`
        - `views` from `posts` (`views.py` from the posts app)
    - create the `urlpatterns` list.
        - add a `path` for `'posts/'` that takes `Postlist` from `views` `as_view()`

    ```py
    from django.urls import path
    from posts import views

    urlpatterns = [
        path('posts/', views.PostList.as_view()),
    ]
    ```
6. in `drf_api/urls.py` `include` the `urls` from `posts`
    ```py
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api-auth/', include('rest_framework.urls')),
        path('', include('profiles.urls')),
        path('', include('posts.urls')),
    ]
    ```
7. run the server, check the get request works so far (add /posts/ to the browser window url)

### Define the Post Method

> To actually have posts appear, we have to make it possible for our users to create them. To achieve that, we have to define the post method inside the PostList view.

the `post` method needs to achieve the following:
1. deserialize request data
2. if the data is valid, save the post with the user as the owner
3. return the post with the 201 CREATED code
4. if the data is invalid, return the ERROR: 400 BAD REQUEST code

steps:
1. in the `PostList` class in `posts/views.py`, `def`ine the `post` method, passing it in the arguments of `self` and `request`:
2. inside the `post` method, create the `serializer` variable, its value being the `PostSerializer`, which will in-turn, handle the following parameters:
    - `data`, which will have the value of `data` from the `request`
    - `context`, which has a {K: V} Pair of K: `'request'` V: `request`
3. inside the function, below the `serializer`, write an `if` statement that checks if the `serializer` `is_valid()`
    - if it is, make the `serializer` `save()` the post, passing a parameter to `save()` that defines the `owner` of the post to be the `user` that made the `request`
    - then, close the `if` statement by `return`ing a `Response` that contains the `data` from `serializer` and a `status` that has a value of `HTTP_201_CREATED` from `status` codes
4. below the `if` statement, in lieu of an `else` statement, `return` a `Response` that takes any `errors` raised by `serializer` and pass a `status` of `HTTP_400_BAD_REQUEST` from `status`
5. > To have a nice create post form rendered in the preview window, let’s also set the serializer_class attribute to PostSerializer on our PostList class.
    - at the top of the class, add a variable called `serializer_class`, its value should be `PostSerializer`

```py
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    serializer_class = PostSerializer

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

the Post List view has now been created, however, at this point, if an unauthenticated user tries to create a post, django will throw an error. 

this can be mitigated using the `permissions` framwork from rest

6. add `permissions` as an import from `rest_framework` at the top of `views.py`
7. at the top of the `PostList` class, below the `serializer_classes` variable, add the `permission_classes` list variable, giving it a single entry in the list of:
    - `permissions.IsAuthenticatedOrReadOnly`

```py
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

go back to the preview and check it all works.

<br>
<hr>

## Commit 7:

this section covers:
- create the PostDetail view
- retrieve a record by id (get)
- update a record by id (put)
- delete a record by id (delete)

Post CRUD Table:
> Let’s have a look at our CRUD table. It shows what kind of HTTP request our users have to make and to which URL in order to list all posts, create, read, update or delete a post. 

| HTTP           | URI           | CRUD Operation                                                                   | View Name         |
| :------------: | :-----------: | :------------------------------------------------------------------------------: | :---------------: |
| **a**.GET / **b**.POST | /posts     | **a**.list all posts / **b**.create a post                         | LIST              |
| **c**.GET / **d**.PUT / **e**.DELETE | /posts/:id | **c**.retrieve a post by id / **d**.update a post by id / **e**.delete a post by id | DETAIL           |

### Create the PostDetail view
steps:
1. go to `posts/views.py`, start by importing the following:
    - `from django.Http import Http404`
    - the custom made permission `IsOwnerOrReadOnly` from `permissions.py` in `drf_api`
        - `from drf_api.permissions import IsOwnerOrReadOnly` 
2. create a new class called `PostDetail` that inherits from `APIView`
3. add the `permission_classes`, there should only be one in the list for now, the `IsOwnerOrReadOnly` permission
    - `permission_classes = [IsOwnerOrReadOnly]`
4. To format the edit form right out the gate, add the `serializer_class` too, which will be `PostSerializer`
    - `serializer_class = PostSerializer`

#### `get` request
5. write the `get_object` method for the view, it should take `self` and `pk` as arguments
    - add in a `try` statement which creates a variable called `post` which `get`s an `object` from `Post` that has a `pk` that matches the `pk` passed in as the argument for the method
        -`post = Post.objects.get(pk=pk)`
    - then, check the permissions of the post and if the accessing user has permission to edit it by using `check_object_permissions` on the instance(`this`), passing it the arguments of `self.request` and the `post` variable
        - `self.check_object_permissions(self.request, post)`
    - `return` the `post` variable
    - then, add an `except`ion for in the event that a `Post` `DoesNotExist`, in which case, the `Http404` error should be `raise`d
6. now, ceate the actual `get` method of the view, passing it `self`, `request` and `pk` as arguments
    - create a variable called `post` that uses the just-defined `get_object` method on the instance thats calling it (`self`) and pass it an argument containing the `pk`
    - beneath that, add a `serailizer` variable that takes the `PostSerializer` and runs the newly-defined `post` variable through it as a parameter, in addition to a `context` parameter with a {Key: Value}Pair of `'request': request`
    - `return` a `Response` containing the `data` from the `serializer`

    ```py
    from django.shortcuts import render
    from django.http import Http404
    from rest_framework import status, permissions
    from rest_framework.response import Response
    from rest_framework.views import APIView
    from .models import Post
    from .serializers import PostSerializer
    from drf_api.permissions import IsOwnerOrReadOnly

    ...

    class PostDetail(APIView):
        permission_classes = [
            IsOwnerOrReadOnly
        ]
        serializer_class = PostSerializer

        def get_object(self, pk):
            try:
                post = Post.objects.get(pk=pk)
                self.check_object_permissions(self.request, post)
                return post
            except Post.DoesNotExist:
                raise Http404
        
        def get(self, request, pk):
            post = self.get_object(pk)
            serializer = PostSerializer(
                post,
                context={'request': request}
            )
            return Response(serializer.data)
    ```

7. now, add the path for the new view in `posts/urls.py`:
    - in `urlpatterns` add a new `path` for `posts/<int:pk>`, where the `PostDetail` from views is rendered `as_` a `view()`

    ```py
    from django.urls import path
    from posts import views

    urlpatterns = [
        path('posts/', views.PostList.as_view()),
        path('posts/<int:pk>/', views.PostDetail.as_view()),
    ]
    ```

#### `put` request
more detailed explanation on how to do this in the [profile](#updating-an-existing-profile), **although be sure to add `context` to the `serializer` as it isn't done in that part of the tutorial yet**

8.  ```py
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    ```

#### `delete` request

9. in the class, `def`ine a `delete` method that takes `self`, `request` and `pk` as parameters
    - define the `post` variable and give it a value using the `get_object` method on the instance(`this`) by using the `pk`
        - `post = self.get_object(pk)`
    - run the `delete()` action on the `post` variable
        - `post.delete()`
    - `return` a `Response` containing a `status` parameter with the value of `HTTP_204_NO_CONTENT` from `status`
        - `return Response(status=status.HTTP_204_NO_CONTENT)`

    ```py
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    ```
10. check it all works

finished view code:

```py
from django.shortcuts import render
from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly

...

class PostDetail(APIView):
    permission_classes = [
        IsOwnerOrReadOnly
    ]
    serializer_class = PostSerializer

    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post,
            context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
```
<br>
<hr>

## Commit 8:

## Setting up the Comments App resources
##### [challenge page](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+DRF+2021_T1/courseware/601b5665c57540519a2335bfbcb46d93/10d957d204794dbf9a4410792a58f8eb/?child=first)

1. run the command in the terminal to make a new app, name it `comments`
    - `python3 manage.py startapp comments`
2. add it to `INSTALLED_APPS` in settings.py

### Creating a comments model
1. in `comments/models.py` import the following:
    - `models` from `django.db`
    - `User` from `django.contrib.auth.models`
    - `Post` from `posts.models`
    ```py
    from django.db import models
    from django.contrib.auth.models import User
    from posts.models import Post
    ```

2. create a class called `Comment`, it should inherit from `models.Model`
3. the new `Comment` class needs the following fields:
    - owner, which should be a `ForeignKey` using the `User` as its value, it should also `CASCADE` delete any related sub-items if deleted
    - post, which should be a `ForeignKey` using the `Post` as its value, it should also `CASCADE` delete any related sub-items if deleted
    - created_at, which should be a `DateTimeField` which should be automatically assigned a new value upon record creation by using the parameter `auto_now_add=True`
    - updated_at, same as above, except its paramater is `auto_now=True`, not `auto_add_now` as it updates every time the post is edited, not when it is `add`ed
    - content, should be a `TextField` to house post content
   
4. add a `Meta` class that orders posts by the `DateTime` they were `created_at`, with the most recent entry being first
5. define a dunder `str` method that returns the `content` of `self`

the post model should look like this:
```py
from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Comment(models.Model):
    """
    Comment model, related to User and Post
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
```

6. Migrate the completed model into the database
    1. `python3 manage.py makemigrations`
    2. `python3 manage.py migrate`


### creating the comment serializer

1. create a new file in `comments` called `serializers.py`
2. inside the new `serailizers` import:
    - `serializers` from `rest_framework`
    - the `Comment` model from `.models`
3. create a class called `CommentSerializer` which inherits from `serializers.ModelSerializer`
4. establish the following serailizer fields:
    - owner: a `ReadOnlyField` that's `source` is the `username` of the `owner` specified in the `Comment` model
    - profile_id: a `ReadOnlyField` that's `source` is the `id` of the `owner` specified in the `Comment` model (`id`'s are automatically created by django)
    - profile_image: a `ReadOnlyField` that's `source` is the `url` of the `image` field beonging to the `owner`, specified in the `Comment` model
    - is_owner: a variable which houses the `SerializerMethodField` for the `serializer`
5. use the `is_owner` field to create a method (prefix it with `get_`) with the following parameters: `self` and `obj` for object in question
    - the function should then take a `context`ual `request` from whatever calls it (`this`), and then checks if the `user` that made the `request` matches the `obj`'s `owner`, `return`ing a boolean value depending on the outcome
6. add a `Meta` class that:
    - determines the `model` the serializer its basing its structure from, n this case it is `Comment`
    - determine the `fields` it serializes and displays in a list variable as strings, they should be:
        - id
        - owner
        - profile_id
        - profile_image
        - post
        - created_at
        - updated_at
        - content
        - is_owner

finished serializer shuold look like this:
```py
from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.id')
    profile_image = serializers.ReadOnlyField(source='owner.image.url')
    is_owner = serializers.SerializerMethodField()
        # this variable above is used to house 
        # the requisite serializer it is called 
        # as a function below by prefixing the variable's 
        # name with 'get_'
    
    def get_is_owner(self, obj):
        """
        passes the request of a user into the serializer
        from views.py
        to check if the user is the owner of a record
        """
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Comment
        fields = [
            'id',
            'owner',
            'profile_id',
            'profile_image',
            'created_at',
            'updated_at',
            'post',
            'content',
            'is_owner',
        ]
```

___________________________________________________________

## Creating the CommentDetailSerializer
#### Creating a Serializer that inherits from another

1. in `comments/serializers.py`, create a new class called `CommentDetailSerializer`. make it inherit from the previously created `CommentSerializer` class
2. give it a variable of `post`: a `ReadOnlyField` that's `source` is the `id` of the `post` specified in the `Comment` model

```py
class CommentDetailSerializer(CommentSerializer):
    post = serializers.ReadOnlyField(source='post.id')
```
> Because CommentDetailSerializer inherits from CommentSerializer, all its methods and attributes are already included e.g. Meta.

___________________________________________________________

## CommentList and CommentDetail generic views
##### https://youtu.be/Xw6qDGQSbqs
##### [more info on Generics](https://www.django-rest-framework.org/api-guide/generic-views/#attributes/)
##### [more info on filtering](https://www.django-rest-framework.org/api-guide/filtering/)

how to write `CommentList` and `Detail` views using generics.

> The Django Documentation states that generic views were developed as a shortcut for common usage patterns. What this means is that we can achieve all the same functionality of the get, post, put and other class based view methods without having to repeat ourselves so much.

steps:
1. go to `views.py` in the `comments` app. 
2. import the following:
    - `generics` from `rest_framework`
    - `IsOwnerOrReadOnly` from `permissions` in `drf_api`
    - `Comment` from `.models`
    - `CommentSerializer` and `CommentDetailSerializer` from `.serializers`

#### Create the CommentList View

3. create a class called `CommentList` that inherits from `generics.ListCreateAPIView`
    - > As we want to both [list] and [create] comments in the ListView, instead of explicitly defining the post and get methods like we did before, I’ll extend generics’ [List][Create]APIView. Extending the [List]APIView means we won’t have to write the get method and the [Create]APIView takes care of the post method.
    - **list** covers the get request
    - **create** covers the post request
4. set the `serailizer_class` to `CommentSerializer`
5. set the `permission_classes` to `[permissions.IsAuthenticatedOrReadOnly]`
6. Add a queryset variable that `get`s `all()` the `objects` in the `Comment` table
    - > Instead of specifying only the model we’d like  to use, in DRF we set the queryset attribute. This way, it is possible to filter  out some of the model instances. This would make sense if we were  dealing with user sensitive data like orders or payments where we would need to  make sure users can access and query only their own data. In this case however, we want all the  comments.
    - [**Learn more about attribute and data filtering here**](https://www.django-rest-framework.org/api-guide/filtering/)

code so far:

    ```py
    from rest_framework import generics, permissions
    from drf_api.permissions import IsOwnerOrReadOnly
    from .models import Comment
    from .serializers import CommentSerializer, CommentDetailSerializer

    class CommentList(generics.ListCreateAPIView):  # step 3
        serializer_class = CommentSerializer  # step 4
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # step 5
        queryset = Comment.objects.all()  # step 6
    ```
> Before we test the view, we’ll have to make sure comments are associated with a user upon creation. We do this with generics by defining the perform_create method

7. `def`ine a method called `perform_create` which takes the arguments of `self` and `serializer`
    - > the `perform_create` method takes in `self` and `serializer` as arguments. Inside, we pass in the user making the request as owner into the serializer’s save method, just like we did in the regular class based views.
8. call the `save()` command on the `serializer`, in the argument of `save` define the `owner` as the `user` making the `request`
    - views using generics:
        ```py 
        from rest_framework import generics, permissions
        from drf_api.permissions import IsOwnerOrReadOnly
        from .models import Comment
        from .serializers import CommentSerializer, CommentDetailSerializer

        class CommentList(generics.ListCreateAPIView):  # step 3
            serializer_class = CommentSerializer  # step 4
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # step 5
            queryset = Comment.objects.all()  # step 6

            def perform_create(self, serializer):  # step 7
                serializer.save(owner=self.request.user)  #step 8
        ```
    - views manually written equivalent:
        ```py
        class PostList(APIView):
            serializer_class = PostSerializer
            permission_classes = [
                permissions.IsAuthenticatedOrReadOnly
            ]

            def get(self, request):
                posts = Post.objects.all()
                serializer = PostSerializer(
                    posts,
                    many=True,
                    context={'request': request}
                )
                return Response(serializer.data)

            def post(self, request):
                serializer = PostSerializer(
                    data=request.data, context={'request': request}
                )
                if serializer.is_valid():
                    serializer.save(owner=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ```

    > More good news is that with generics, the request  is a part of the context object by default. What this means is that we no longer have to pass it manually,  like we did in the regular class based views.

9. now, create the `urls` for the comments. create the `urls.py` file in the `comments app`
10. import the following into `comments/urls.py`:
    - `from django.urls import path`
    - `from comments import views`
11. next, create the `urlpatterns` list beneath the imports, it should contain the following paths:
    - `'comments/'` which should take the `CommentList` `view` and render it `as_view()`

```py
urlpatterns = [
    path('comments/', views.CommentList.as_view()),
]
```

12. then, in `drf_api/urls` add the `'comments.urls'` to a `path` by using the `include` method
    ```py
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api-auth/', include('rest_framework.urls')),
        path('', include('profiles.urls')),
        path('', include('posts.urls')),
        path('', include('comments.urls')),  # step 12
    ]
    ```

#### create the CommentDetail view

13. go back to `comments/views` and create a class called `CommentDetail` and have it inherit from `generics.RetrieveUpdateDestroyAPIView`
    - from generics, the following methods are pulled in the inherited model name to automatically streamline the coding for the following types of requests:
        - `Retrieve` data
        - `Update` data
        - `Destroy` data
        - jump back up [here](#create-the-commentlist-view) for a fuller explanataion
        - [documentation on generics](https://www.django-rest-framework.org/api-guide/generic-views/#attributes/)
14. set the `permission_classes` list of the new class to the imported `[IsOwnerOrReadOnly]` permission
15. set the `serializer_class` for the class to `CommentDetailSerializer`
    - > Our serializer still needs to access the request, but as mentioned before, we don’t really need to do anything, as the request is passed in as part of the context object by default.
16. define the `queryset` for the class, querying `all()` the `objects` in the `Comment` table

```py
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):  # step 13
    permission_classes = [IsOwnerOrReadOnly]  # step 14
    serializer_class = CommentDetailSerializer  # step 15
    queryset = Comment.objects.all()  # step 16
```

17. with the class created, head back to `comments/urls.py` and add a new path to the `urlpatterns` list, this time it should be for `comments/<int:pk>/`, (<int:pk>: the primary key is being told to be handled as an integeter). It should render the `CommentDetail` `view` `as_view()`

```py
urlpatterns = [
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>', views.CommentDetail.as_view()),  # step 17
]
```

<br>
<hr>

## Commit 9:
