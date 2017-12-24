from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .models import Product #, HashTag
from .models import UserProfile
from .forms import ProductForm, ContactForm, SubscribeForm, EditProfileForm
from django.views import generic

# edit / delete views
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView, DeleteView

from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from . import forms

from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.views import LoginView


class LoginView(LoginView):

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])


class DesignersView(generic.TemplateView):
    template_name = 'designers.html'

    def get_context_data(self,**kwargs):
        context = super(DesignersView,self).get_context_data(**kwargs)
        context['object_list'] = User.objects.all()
        context['designer_products'] = Product.objects.all().order_by('?')[:4]
        return context


class HomePage(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        context=super(HomePage, self).get_context_data(*args, **kwargs)
        context['form'] = ContactForm
        return context


def products(request):
    product_list = Product.objects.get_queryset().order_by('id')
    page = request.GET.get('page', 1)
    username = request.GET.get('username',None)
    user = None
    if username:
        try:
            user = User.objects.get(username=username)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            pass
    if user:
        return Product.objects.filter(user=user)
    else:
        products = Product.objects.get_queryset().order_by('id')
    form = ProductForm()

    paginator = Paginator(products, 8)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'products.html', {'products': products, 'form':form})


class ProductListView(ListView):
    template_name = 'product_list.html'
    context_object_name = 'product_list'
    paginate_by = None

    def get_queryset(self):
        username = self.request.GET.get('username',None)
        user = None
        if username:
            try:
                user = User.objects.get(username=username)
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                pass
        if user:
            return Product.objects.filter(user=user)
        return Product.objects.none()


def post_product(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProductForm(data = request.POST, files = request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            product = form.save(commit = False)
            product.user = request.user
            product.likes = 0
            product.save()
        # redirect to a new URL:
            return HttpResponseRedirect('/products')
        else:
            context = {"form": form}
            return render(request, "products.html", context)


def detail(request, product_id):
    product = Product.objects.get(id=product_id)
    #hashtags = HashTag.objects.filter(product=product_id)
    return render(request, 'detail.html', {'product': product})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    products = Product.objects.filter(user=user)
    if not request.user == user:
        return redirect('profile', username=request.user.username)
    else:
        return render(request, 'profile.html', {'user':user,'products': products})


@login_required
def edit_profile(request):
    user = request.user
    products = Product.objects.filter(user=user)
    userprofile, created = UserProfile.objects.get_or_create(user=user)
    form = EditProfileForm(initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'biography': userprofile.biography,
        'tagline': userprofile.tagline,
        'image': userprofile.image
    })

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']  # use cleaned_data
            user.last_name = form.cleaned_data['last_name']
            userprofile.biography = form.cleaned_data['biography']
            userprofile.tagline = form.cleaned_data['tagline']
            userprofile.image = form.cleaned_data['image']
            userprofile.save()  # save Biography object
            user.save()  # save User object
            return render(request, 'profile.html', {'user':user,'products': products})  #  always redirect after successful POST.

    context = {'form': form}
    return render(request, 'edit_profile.html', context)


def like_product(request):
    product_id = request.POST.get('product_id', None)

    likes = 0
    if (product_id):
        product = Product.objects.get(id=int(product_id))
        if product is not None:
            likes = product.likes + 1
            product.likes = likes
            product.save()

    return HttpResponse(likes)


class PostUpdateView(UpdateView):
   model = Product
   form_class = ProductForm
   template_name = 'edit_product.html'

   def form_valid(self, form):
      self.object = form.save(commit=False)
      self.object.save()
      return redirect('detail', self.object.pk)

   @method_decorator(login_required)
   def dispatch(self, request, *args, **kwargs):
     return super(PostUpdateView, self).dispatch(request, *args, **kwargs)


class PostDeleteView(DeleteView):
   model = Product
   template_name = 'product_confirm_delete.html'

   def get_success_url(self):
      return reverse ('products')

   @method_decorator(login_required)
   def dispatch(self, request, *args, **kwargs):
      return super(PostDeleteView, self).dispatch(request, *args, **kwargs)

User = get_user_model()

def subscribe(request):
    form_class = SubscribeForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')

            # Email the profile with the
            # contact information
            template = get_template('contact/subscribe_template.txt')
            context = dict({'contact_name': contact_name, 'contact_email': contact_email,})

            content = template.render(context)

            email = EmailMessage(
                "New subscribe form submission",
                content,
                "Your website" +'',
                ['steve@steve-shead.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return render(request, 'contact/thank_you_subscribe.html')

    return render(request, 'contact/subscribe.html', {
        'form': form_class,
    })

def contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('contact/contact_template.txt')
            context = dict({'contact_name': contact_name, 'contact_email': contact_email, 'form_content': form_content,})

            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['steve@steve-shead.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return render(request, 'contact/thank_you.html')

    return render(request, 'contact/contact.html', {
        'form': form_class,
    })
