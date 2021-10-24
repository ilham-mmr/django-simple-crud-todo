# Repo Info
- this repo is used to store my django study notes from django practical guide course
- this repo has a simple django crud app implementing class based views
  
## Django Notes
to create a django project | django-admin startproject "project name"

extensions of vs code : python, pylance, django ( must follow the configuration rules first)

to run the server | python [manage.py](http://manage.py/) runserver

to create a django app | python [manage.py](http://manage.py/) startapp "app name"

reverse() to dynamically generete url
django shell | python [manage.py](http://manage.py) shell


### django templating language

#### features

1. filter or | [https://docs.djangoproject.com/en/3.2/ref/templates/builtins/](https://docs.djangoproject.com/en/3.2/ref/templates/builtins/)
2. tags e.g. for tag, if tag

### django models

1. django fields
2. Migrations
3. python [manage.py](http://manage.py) makemigrations | to create migration
4. python [manage.py](http://manage.py) migrate | to migrate 

- ##### to save model

e.g. harry_potter = Book(title="Harry Potter 1 - The philosopher's Stone", rating=5)

- ##### to delete

harry_potter.delete()

- ##### to get one

Book.objects.get(id=1)

- ##### filter 

Book.objects.filter(rating__lt=6, title_contains='story')

- ##### filter is like "and" to use "or" query we must wrap the attribute with Q class

Book

e.g. 

> from django.db.models import Q
Book.objects.filter(Q(rating__lt=3) | Q(is_bestselling=True))
> 

combining with "and". just put ","

e.g

Book.objects.filter(Q(rating__lt=3) | Q(is_bestselling=True), title="Harry Potter 1")

- to create slug
    - use models.SlugField
- order by. - means descending. without - means ascending
    - Book.objects.all().order_by('-title')

- tip
    - for generating url detail
    
    def get_absolute_url(self):
    
    *return* reverse("book-detail", args=[self.slug])
    

### Django Admin

to register the created app in admin

*from* django.contrib *import* admin

*from* .models *import* Book

*# Register your models here.*

admin.site.register(Book)

The admin can be configured

```jsx
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("author","rating")
    list_display = ("title", "author")

admin.site.register(Book, admin_class=BookAdmin)
```

### Django Relationship

- One to many e.g. Author has many books. a book belongs to author

```jsx
author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
```

- to query books from author

> jkr = Author.objects.get(first_name="J.K.")
jkr.book_set.all()
> 

- to change the related name. we need to mody the author field in the book model

```jsx
author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name="books")
```

- One to one e.g. one author has one address, one address belongs to one author

```jsx
address = OneToOneField(Address,on_delete=models.SET_NULL)
```

TIPS: to configure the behavior of the model. create a nested Meta class

```python
class Address(models.Model):
    street = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.postal_code}, {self.city}"
    
    class Meta:
				# to change the plural name
        verbose_name_plural = "Address Entries"
```

-) Many to many. a book can be published in many countreis. country can publish many books

```python
published_countries = models.ManyToManyField(Country)
```

it will create a mapping table between country and book.

> germany = Country(name="Germany", code="DE")
germany.save()
hp1.published_countries.add(germany)
> 

the inverse relation

```python
germany.book_set.all()
```

to change the default name, we can add the related_name

### Django Form

```python
if request.method == 'POST':
        entered_username = request.POST['username']
        print(entered_username)
        return redirect('/thank-you')
```

the [request.POST](http://request.POST) holds a dictionary

we can define built in form

```python
from django import forms
class ReviewForm(forms.Form):
    user_name = forms.CharField()

views.py
form = ReviewForm()
    return render(request, "reviews/review.html", {"form": form})
```

instead manually validating the incoming request from form. we can do the following

```python
if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return redirect('/thank-you')
```

to override the default behaviour of form, simply add arguments

```python
user_name = forms.CharField(label="Your Name",max_length=100, error_messages={
        "required" : "Your name must not be empty",
        "max_length" : "please enter a shorter name"
    })
```

we can iterate the form if it has many fields in the html

```python
{% for field in form %}
          <div class="form-control {% if field.user_name.errors %}errors{% endif %}" >
            {{ field.label_tag}}
            {{ field }}
            {{ field.errors }}
        </div>
        {% endfor %}
```

Instead of creating form and model separtely we can do it together

inherit the class from ModelForm

```python
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'review_text', 'rating']
				# to select all fields
				# fields = '__all__'
				# to exlude fields
				# exclue = ['user_name']

				# to configure auto infered labels
				labels = {
            'user_name': "Your Name",
            'review_text': 'Your Feedback',
            'rating' : 'Your Rating'
        }
				# to configure error message
				error_messages = {
            'user_name': {
                'required': "Your name must not be empty",
                'max_length': 'please entere a shorter name'
            }
        }
```

saving data with modelform

simply call form.save() after validating the form instead of manually saving the model separately

```python
if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/thank-you')
```

to update modelform with django

```python
if request.method == 'POST':
				existing_data = Review.objects.get(pk=1)
        form = ReviewForm(request.POST, instance=existing_data)
        if form.is_valid():
            form.save()
            return redirect('/thank-you')
```

### Class Based Views

you can get and post method 

```python
from django.views import View
class ReviewView(View):
    def get(self,request):
        form = ReviewForm()
        return render(request, "reviews/review.html", {"form": form})
    def post(self, request):
        form = ReviewForm(request.POST)
        if form.ids_valid():
            form.save()
            return redirect('/thank-you')
in urls.py
path('', views.ReviewView.as_view()),
```

VIEWS Module

-Template Views

-List & detail views

-Form View & Create/ update / delete views

CLASS BASED VIEWS

- template view
    - no need to  call render. only set the template_name
    
    ```python
    class ThankYouView(TemplateView):
        template_name = "reviews/thank_you.html"
    ```
    
    if we want to pass data e.g 'message' to the template we can overided the get_context_data
    

```python
def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'This works!'
        return context
```

- List View
    - from django.views.generic import ListView
    
    ```python
    class ReviewsListView(ListView):
        template_name = 'reviews/review_list.html'
        model = Review
    
    # the default name thats exposed to the template is object_list
    {% for review in object_list %}
        <li>{{review.user_name}} (Rating: {{ review.rating }})</li> 
    {% endfor %}
    
    # to change the name 
    context_object_name = 'reviews'
    ```
    
    - to adjust the query behavior
        
        ```python
        def get_queryset(self):
                base_query =  super().get_queryset()
                return  base_query.filter(rating__gt=2)
        ```
        
- Detail View
    - from django.views.generic import  DetailView
    
    ```python
    class SingleReviewView(DetailView):
        template_name = 'reviews/single_review.html'
        model = Review
    # django will use 'review' to expose the data to the html
    ```
    
- Form View
    - from django.views.generic.edit import FormView
    
    ```python
    class ReviewView(FormView):
        form_class = ReviewForm
        template_name = 'reviews/review.html'
        success_url = '/thank-you'
    
        def form_valid(self, form):
            form.save()
            return super().form_valid(form)
    ```
    
- Create View
    - from django.views.generic.edit import CreateView
    - no need form
    
    ```python
    class ReviewView(CreateView):
        model = Review
        form_class = ReviewForm
        template_name = 'reviews/review.html'
        success_url = '/thank-you'
    ```
    
- update view and delete view

### FILE UPLOADS

- request.FILES['image']
- adding a form with the filefield

```python
from django import forms

class ProfileForm(forms.Form):
    user_image = forms.FileField()
```

we need to configure where we wanna store the files in settings.py

```python
MEDIA_ROOT = BASE_DIR/'uploads'
```

then we create the model

```python
class UserProfile(models.Model):
    image = models.FileField(upload_to='images')
```

in the views

```python
class CreateProfileView(View):
    def get(self, request):
        form = ProfileForm()
        return render(request, "profiles/create_profile.html",{
            'form': form
        })

    def post(self, request):
        submitted_form = ProfileForm(request.POST, request.FILES)
        if submitted_form.is_valid():
             profile = UserProfile(image=request.FILES['user_image'])
             profile.save()
        return HttpResponseRedirect('/profiles/')
```

USING IMAGEFIELD instead of FileField. it will validate images only

when we use imagefield, we need to install pillow

```python
python -m pip install Pillow"
```

```python
models.py
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    image = models.ImageField(upload_to='images')
forms.py
from django import forms

class ProfileForm(forms.Form):
    user_image = forms.ImageField()
```

using create view for file upload

```python
class CreateProfileView(CreateView):
    template_name = 'profiles/create_profile.html'
    model =UserProfile
    fields = '__all__'
    success_url ='/profiles'
```

serving uploaded files

- the model's property has image.path

```python
{% for profile in profiles %}
        <li>
            <img src="{{ profile.image.url }}" alt="">
        </li>
        {% endfor %}
```

atm, no photos are publicly accessible. to expose them to public do this

1. setting media_url in settings.py
    
    ```python
    # the url that public should see
    MEDIA_URL = '/user-media/'
    ```
    
2. next configure the [urls.py](http://urls.py) in project level

```python
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviews.urls')),
     path("profiles/", include("profiles.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

3. in the url, it looks like this src="/user-media/images/tech_team.png"

### SESSIONS

session is an ongoing connection between a client and server

alter session age in settings.py. by default two weeks

SESSION_COOKIE_AGE = 120

dont store object in session

```python
class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST['review_id']
        request.session['favorite_review'] = review_id  
        return HttpResponseRedirect('/reviews/'+review_id)
```

to expose it in html we override the following method. hence in html we can use the is_favorite

```python
def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object
        request = self.request
        favorite_id = request.session.get('favorite_review')
        context['is_favorite'] = favorite_id == str(loaded_review.id)
        return context
```
