"""
# HOW A SERVER CAN SERVE INFORMATION USING DJANGO

    if the responsibility of generating webpages falls on the client,
    the server only needs to serve the data,
    that can be accessed by the client via endpoints

    the server thus provides an Application Programming Interface (API)
    for the client to get or save data.

    django is a back-end server framework, so
    you can use angle, react for your front-end together


# PREPARING DEV ENV

    download pipenv (prevents conflict with other application dependencies)

    activate the pipenv using source <venv-name>/bin/activate

    why? -> imagine your project needs v2.1 of a library, and another v3.1.

        v3.1 does not work on the project using v2.1. So, you need to run the 2.1
        project in a venv to test it, while using the native env for the 3.1 project.

# GETTING INTO DJANGO, PROPERLY

    The MVT model structure

        Urls -> Views (buisness logic)
        -> Models (databases) +
        Templates (presentation layer)

        Data + Layout is combined in Views to display the webpage

    basic context (main commands)

        makemigrations - preps database for migration
        migrations - execute migrations to create a blueprint of how the database looks like
        runserver - turn on web server
        startproject - create django project
        startapp - create apps

    settings.py

        the commmand center of your project, what to include, etc

    urls.py

        routes the user depending on the URL given

    django apps

        the website consists of seperate apps that come together
        each app has its own URL routing, DB models & templates

    urlpatterns in the main urls.py

        urlpatterns = [
            path("admin/", admin.site.urls),
            path("home/", getHomePage),
            path("projects/", getProjects),
        ]

    when a path is accessed, the function mentioned will be run, either to
    fetch data or send data

    dynamic URLs

        example usage

        path("project/<str:pk>/", project, name="project")

        pk is the name of the key provided, pass into your function to use

    views.py

        it is where you store the functions to be run when the user is
        routed to the specified URL.

# DJANGO COMMANDS

    key ideas

    makemigrations

        generates a list of items to be migrated to your database

    migrate

        executes the migrations created by makemigrations to your database

    after making migrations, you can modify and view the database using the django admin panel,
    using the route stated in urlpatterns

# DJANGO VIEWS

    combines templates and models (aka databases) together to render a webpage

        contained in views.py

# DJANGO MODELS

    a fancy word for DATABASES

    allows you to define databases in python,
    and apply them to sqlite, mySQL, any db language

    HOW TO QUERY INFO FROM DATABASES?

    syntax
        queryset = ModelName.objects.all()

        .get(), -> single object
        .filter(), -> return ALL objects with a condition (can add multiple)
        .exclude() -> inverse of filter()

        filter subfunctions
        .filter(attribute__startswith="")
        .filter(attribute__contains="")
        .filter(attribute__icontains="") -> ignore case "i"
        .filter(attribute__gt="") -> greater than
        .filter(attribute__gte="") -> greater than or equal to
        .filter(attribute__lt="")
        .filter(attribute__lte="")

    CRUD'ing Models (databases) using django

    CREATE
        item_to_add = ModelName.objects.create(attribute='value')

    READ
        item_to_read = ModelName.objects.get(attribute='value')

    UPDATE
        item_to_update = ModelName.objects.get(attribute='value')
        item_to_update.title = 'new_value'
        item_to_update.save()

    DELETE
        # get last item from the ModelName database
        item_to_delete = ModelName.objects.last()
        item_to_delete.delete()

    ACCESS CONENCTED FOREIGN (CHILD) DATABASE
        item_to_find = ParentModelName.ChildModelName_set.all()

        example syntax
            reviews = Project.object.get(title="Ecommerce Website").review_set.all()

            - Parent Model: "Project.object.get(title="Ecommerce Website")"
            - Chlid Model Name: Review (when calling it, use lowercase)

    ACCESS A ManyToMany FIELD
        a_database = ModelName.objects.get(AttributeName="<string>")
        a_database.relationshipname.all()


# DJANGO FORMS

    thanks to the use of the django database API, we can use django to create
    auto-generated forms by doing "from django.forms import ModelForm"

    example syntax of a ModelForm class
    # syntax: "<nameOfModel>Form(conforms_to_modelform superclass)"
    class ProjectForm(ModelForm):
        class Meta:
            # tells the superclass to use the Project model
            model = Project
            # can create a list or use fields='__all__'
            fields = ["title", "description", "demo_link", "source_link", "tags"]
    # Q: what is django doing when you declare field?
        # A: it is taking all the required fields from the project model
        # and turning them into input fields (less those with attribute editable=False
        # and auto_now_add=True) (aka non-editable fields)

    After creating the form, pass it into a view and render it to a template.

    In your jinja template, be sure to add the CSRF token to submit the form you made

    example: "{% csrf_token %}"

    this is a security measure to ensure that POST requests were
    received from the website itself and not a foreign website


# DJANGO STATIC FILES

    they are css, javascript and asset files that do not change

    Static Files the Django way
        create a new folder called "static" and add your files

    adding images to your Models

        you may add an Image to your model using models.ImageField

        in your html form template, add  enctype="multipart/form-data"  to the
        form tag, so that you can send files via the reuqest

        be sure to add request.FILES when you create the form object to include the file

        however, the image file itself will be saved to the project root directory,
        and the path to it is stored in the database. To avoid clutter, you need to
        let django know where to upload the image file in settings.py

            configure:
            MEDIA_ROOT = os.path.join(BASE_DIR, "static/images")

    serving images to your Views

        to serve images, use the filepath in your model by calling

        "ModelName.NameOfYourImgField.url" in your html template

        this will create a URL endpoint.

        An image will be shown if you add the image paths to urlpatterns,
        using "urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"

# DJANGO SIGNALS

    What are they?
        Set multiple events when a user performs an action
        (eg. add the user to database and redirect to his profile once you complete the signup sheet)



        Consists of senders and receivers

            1 Sender (the User Model) -> >= 1 Receiver (Can be triggered before, during and after the Sender) -> >= 1 Actions

            The receiver function just needs to be called by a signal, no need to write the code within the View function.

            Signals can come from Models, or Management

            Some examples of Model signals:
                pre_init
                post_init
                pre_save
                post_save
                pre_delete
                post_delete
                m2m_changed
                class_prepared

# DJANGO AUTHENTICATION

    # authentication vs authorisation

    authentication refers to verifying if someone is a user of the app

    authorisation refers to permissions that a user has within the app

    # HOW TO AUTHENTICATE AND LOGIN

    # Step 1: create a html file with a form to login
    # Step 2: create a view that links to the html file
    # Step 3: within the view, use authenticate() and login() to allow a user to log in and edit information

    example usage

    from django.contrib.auth import login, authenticate, logout
    from django.contrib.auth.models import User

    def loginUser(request):
    # if a form was submitted
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            print("Username does not exist")

        # queries database for the username and password entered, returns None
        # if the user does not exist or password is incorrect
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # creates session for user in the database
            # add the session token into browser cookies
            login(request, user)
            return redirect('profile')
        else:
            print('Username or password incorrect')

    return render(request, "users/login_onboarding.html")

# DJANGO MESSAGES

    # FLASH MESSAGES

        one time messages that you can render in your template. Messages rendered go
        away once you refresh the page

        messages have different methods you can use "debug", "info", "warning", "error", etc
        (see documentation)

        example syntax

            messages.error(request, "<state-error-here>")

        to render the message in all your websites, be sure to include this in your main template:

          {% if messages %}
        <ul class="messages">
            {% for message in messages %}
            <li {% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
            {% endfor %}
        </ul>

        this will ensure that you can render messages in every website.
        








































"""