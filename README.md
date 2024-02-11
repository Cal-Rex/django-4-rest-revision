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
            'profiles'
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