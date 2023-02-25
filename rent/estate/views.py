from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.db.models.query_utils import Q
from django.template import loader
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from .forms import SignupForm  
from django.utils import timezone
from django.views.generic import TemplateView
from .models import User, Annoucement, Picture, Favorite, Compilation, Chat, Message
from django.db.models import F, Q, TextField, Value
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse


class UserLoginAdd(LoginView):
    template_name = 'estate/login.html'
    extra_context = {'warning': 'Войдите, чтобы добавлять объявления'}

class UserLoginFavorite(LoginView):
    template_name = 'estate/login.html'
    extra_context = {'warning': 'Войдите, чтобы добавлять в избранное'}

class UserLoginChat(LoginView):
    template_name = 'estate/login.html'
    extra_context = {'warning': 'Войдите, чтобы отправлять сообщения'}

def main(request):
    annoucements = Annoucement.objects.all()

    user = request.user
    try:
        compilations = Compilation.objects.filter(creator=user)
    except: 
        compilations = []
    content = {"annoucements": annoucements, "compilations": compilations}
    template = loader.get_template('estate/main.html')
    return HttpResponse(template.render(content, request))  

def authorize(request):
    content = {}
    template = loader.get_template('estate/login.html')
    return HttpResponse(template.render(content, request))  

def account(request):
    content = {}
    template = loader.get_template('estate/account.html')
    template_error = loader.get_template('estate/main.html')
    if request.user.is_authenticated:
        return HttpResponse(template.render(content, request))  
    else: 
        return HttpResponse(template_error.render(content, request))

def back(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def register(request, args=''):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('registered')
    else:
        form = SignupForm()
    if request.user.is_authenticated:
        return render(request, 'estate/main.html')
    else: 
        return render(request, 'estate/register.html', {'form': form})

def register_block(request, url_id):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('registered')
    else:
        form = SignupForm()
    if request.user.is_authenticated:
        return render(request, 'estate/main.html', {'url_id': url_id})
    else: 
        return render(request, 'estate/register.html', {'form': form, 'url_id': url_id})

@login_required
def registered(request):
    annoucements = Annoucement.objects.all()

    user = request.user
    try:
        compilations = Compilation.objects.filter(creator=user)
    except: 
        compilations = []
    content = {"annoucements": annoucements, "compilations": compilations}
    template = loader.get_template('estate/main.html')
    return HttpResponse(template.render(content, request))

def logout_view(request):
    logout(request)  
    return redirect(reverse('register'))

def reset_password(request):
    content = {}
    template = loader.get_template('estate/reset_password.html')
    return HttpResponse(template.render(content, request))  

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "estate/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="estate/password_reset.html", context={"password_reset_form":password_reset_form})

def confirm_reset(request):
    content = {}
    template = loader.get_template('estate/reset_password_done.html')
    return HttpResponse(template.render(content, request))  

def change_data(request):
    name = request.POST.get('first_name')
    surname = request.POST.get('last_name')
    user = request.user
    user.username = str(name + ' ' + surname)
    user.save()
    return redirect(reverse('account'))

class myview(TemplateView):

    def myfunction(self,request, object_id, **kwargs):
        model = kwargs['model']

def favorite(request):
    try:
        user = request.user
        favorites = Favorite.objects.filter(user=user)
        compilations = Compilation.objects.filter(creator=user)
    except: 
        return redirect(reverse('login_warning_favorite'))
    content = {"favorites": favorites, "compilations": compilations}
    template = loader.get_template('estate/favorite.html')
    return HttpResponse(template.render(content, request))  

def show_compilation(request, arg):
    user = request.user
    all_favorites = Favorite.objects.all()
    favorites = Favorite.objects.filter(user=user)
    compilations = Compilation.objects.filter(creator=user)
    chosen_compilation = Compilation.objects.get(id=arg)
    chosen_elements = chosen_compilation.favorite.all()

    content = {"favorites": favorites, "compilations": compilations, "chosen_compilation": chosen_compilation,
               "chosen_elements": chosen_elements, 'all_favorites': all_favorites}
    template = loader.get_template('estate/favorite.html')
    return HttpResponse(template.render(content, request))  

def add_post(request, warning=''):
    content = {'warning': warning}
    template = loader.get_template('estate/add_post.html')
    return HttpResponse(template.render(content, request))  

def adding(request, warning=''):
    user = request.user
    if user.is_anonymous:
        return redirect(reverse('login_warning_chat'))

    date = timezone.now()
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    category = request.POST.get('category')
    title = request.POST.get('title')
    price = request.POST.get('price')
    address = request.POST.get('address')
    area = request.POST.get('area')
    ceil = request.POST.get('ceil')
    ceilings = request.POST.get('ceilings')
    description = request.POST.get('description')
    if description == '':
        description = 'Пустое описание'
    building_year = request.POST.get('building_year')
    type = request.POST.get('type')
    heating = request.POST.get('heating')
    images = request.FILES.getlist('upload')

    try:
        main_image = request.FILES.getlist('upload')[0]
    except: pass

    district_list = ['Центральный', 'Индустриальный', 'Октябрьский', 'Железнодорожный', 'Ленинский']
    district = district_list[0]
    for place in district_list:
        if place in address:
            district = place
            break

    for index, image in enumerate(images):
        if index == 0:
            main_image = image

    try:
        new_annoucement = Annoucement(creator=user, date=date, phone=phone, email=email, category=category, title=title, 
                                    price=price,address=address, area=area, ceil=ceil, ceilings=ceilings,
                                    description=description, main_image=main_image, building_year=building_year, type=type, 
                                    heating=heating, district=district)
    except: 
        new_annoucement = Annoucement(creator=user, date=date, phone=phone, email=email, category=category, title=title, 
                                    price=price,address=address, area=area, ceil=ceil, ceilings=ceilings,
                                    description=description, building_year=building_year, type=type, 
                                    heating=heating, district=district)
    
    try:
        new_annoucement.save()
    except: 
        return redirect(reverse('add_post', kwargs={'warning': 'Проверьте корректность ввода!'}))

    for index, image in enumerate(images):
        Picture.objects.create(annoucement=new_annoucement, image=image)

    annoucements = Annoucement.objects.all()

    content = {"annoucements": annoucements}
    template = loader.get_template('estate/main.html')
    return HttpResponseRedirect(reverse('main'))

def add_favorite(request, arg):
    user = request.user
    if user.is_anonymous:
            return redirect(reverse('login_warning_favorite'))
    annoucement = Annoucement.objects.get(id=arg)
    favorite = Favorite(annoucement=annoucement, user=user)
    try: 
        favorite.save()
    except: 
        return redirect(reverse('annoucement_item', args=[arg]))
    content = {}
    template = loader.get_template('estate/add_post.html')
    return redirect(reverse('annoucement_item', args=[arg]))

def add_favorite_from_main(request, arg):
    user = request.user
    if user.is_anonymous:
            return redirect(reverse('login_warning_favorite'))
    annoucement = Annoucement.objects.get(id=arg)
    favorite = Favorite(annoucement=annoucement, user=user)
    try: 
        favorite.save()
    except: 
        return redirect(reverse('main'))
    content = {}
    template = loader.get_template('estate/add_post.html')
    return redirect(reverse('main'))

def remove_favorite(request, arg):
    user = request.user
    favorite = Favorite.objects.get(id=arg)
    try: 
        favorite.delete()
    except: 
        return redirect(reverse('favorite'))
    content = {}
    template = loader.get_template('estate/favorite.html')
    return redirect(reverse('favorite'))

def add_compilation(request):
    title = request.POST.get('title')
    user = request.user
    compilation = Compilation(creator=user, title=title)
    try: 
        compilation.save()
    except: 
        return redirect(reverse('favorite'))
    content = {}
    template = loader.get_template('estate/add_post.html')
    return redirect(reverse('favorite'))

def remove_compilation(request, arg):
    compilation = Compilation.objects.get(id=arg)

    try: 
        compilation.delete()
    except: 
        return redirect(reverse('favorite'))
    content = {}
    template = loader.get_template('estate/add_post.html')
    return redirect(reverse('favorite'))

def save_compilation(request, arg):
    annoucements = Annoucement.objects.all()
    specify_annoucement = Annoucement.objects.get(id=arg)
    auto_popup = True
    content = {'annoucements': annoucements, 'specify_annoucement': specify_annoucement, 'auto_popup': auto_popup}
    template = loader.get_template('estate/main.html')
    return HttpResponse(template.render(content, request))  

def add_in_compilation(request):
    annoucements = Annoucement.objects.all()
    user = request.user
    id_annoucement = request.POST.get('best_field')
    id_compilation = request.POST.get('compilation')
    
    annoucement = Annoucement.objects.get(id=id_annoucement)
    
    try:
        compilations = Compilation.objects.filter(creator=user)
    except: 
        compilations = []
    user_compilations = Compilation.objects.filter(creator=user)
    compilation = Compilation.objects.get(id=id_compilation)
    compilation.favorite.add(annoucement)
    favorite = Favorite(annoucement=annoucement, user=user)
    try: 
        favorite.save()
    except: 
        return redirect(reverse('favorite'))

    content = {'annoucements': annoucements, 'id_compilation': id_compilation, 'compilations': compilations}
    template = loader.get_template('estate/main.html')
    return HttpResponse(template.render(content, request))

def annoucement_item(request, arg):
    annoucement = Annoucement.objects.get(id=arg)
    creator = annoucement.creator
    content = {"annoucement": annoucement, "creator": creator}
    template = loader.get_template('estate/annoucement.html')
    return HttpResponse(template.render(content, request))  

def about(request):
    content = {}
    template = loader.get_template('estate/about.html')
    return HttpResponse(template.render(content, request))  

def contacts(request):
    content = {}
    template = loader.get_template('estate/contacts.html')
    return HttpResponse(template.render(content, request))

def searched(request):
    estate_category = request.POST.getlist('category')
    square1 = request.POST.get('square1')
    square2 = request.POST.get('square2')
    price1 = request.POST.get('price1')
    price2 = request.POST.get('price2')
    district = request.POST.get('district')
    owner = request.POST.getlist('from_owner')
    usability = request.POST.getlist('usability')
    conditions = request.POST.getlist('conditions')
    from_ceiling = request.POST.get('from_ceiling')
    to_ceiling = request.POST.get('to_ceiling')
    from_year = request.POST.get('from_year')
    to_year = request.POST.get('to_year')
    estate_type = request.POST.get('type')
    trash = request.POST.getlist('trash')
    search_text = request.POST.get('search')
    user = request.user

    annoucements = Annoucement.objects.all()
    if estate_category != []:
        filtered_data = annoucements.filter(category__in=estate_category)

    try:
        filtered_data
        if square1 and square2:
            filtered_data = filtered_data.filter(area__gte=square1, area__lte=square2)
        if square1:
            filtered_data = filtered_data.filter(area__gte=square1)
        if square2:
            filtered_data = filtered_data.filter(area__lte=square2)
    except: 
        filtered_data = annoucements
        if square1 and square2:
            filtered_data = filtered_data.filter(area__gte=square1, area__lte=square2)
        if square1:
            filtered_data = filtered_data.filter(area__gte=square1)
        if square2:
            filtered_data = filtered_data.filter(area__lte=square2)

    try:
        filtered_data
        if price1 and price2:
            filtered_data = filtered_data.filter(price__gte=price1, price__lte=price2)
        if price1:
            filtered_data = filtered_data.filter(price__gte=price1)
        if price2:
            filtered_data = filtered_data.filter(price__lte=price2)
    except: 
        filtered_data = annoucements
        if price1 and price2:
            filtered_data = filtered_data.filter(price__gte=price1, price__lte=price2)
        if price1:
            filtered_data = filtered_data.filter(price__gte=price1)
        if price2:
            filtered_data = filtered_data.filter(price__lte=price2)

    try:
        filtered_data
        if district != 'Любой':
            filtered_data = filtered_data.filter(district=district)
    except: 
        filtered_data = annoucements
        if district != 'Любой':
            filtered_data = filtered_data.filter(district=district)

    try:
        filtered_data
        if from_ceiling and to_ceiling:
            filtered_data = filtered_data.filter(ceil__gte=from_ceiling, ceil__lte=to_ceiling)
        if from_ceiling:
            filtered_data = filtered_data.filter(ceil__gte=from_ceiling)
        if to_ceiling:
            filtered_data = filtered_data.filter(ceil__lte=to_ceiling)
    except: 
        filtered_data = annoucements
        if from_ceiling and to_ceiling:
            filtered_data = filtered_data.filter(ceil__gte=from_ceiling, ceil__lte=to_ceiling)
        if from_ceiling:
            filtered_data = filtered_data.filter(ceil__gte=from_ceiling)
        if to_ceiling:
            filtered_data = filtered_data.filter(ceil__lte=to_ceiling)

    try:
        filtered_data
        if from_year and to_year:
            filtered_data = filtered_data.filter(building_year__gte=from_year, building_year__lte=to_year)
        if from_year:
            filtered_data = filtered_data.filter(building_year__gte=from_year)
        if to_year:
            filtered_data = filtered_data.filter(building_year__lte=to_year)
    except: 
        filtered_data = annoucements
        if from_year and to_year:
            filtered_data = filtered_data.filter(building_year__gte=from_year, building_year__lte=to_year)
        if from_year:
            filtered_data = filtered_data.filter(building_year__gte=from_year)
        if to_year:
            filtered_data = filtered_data.filter(building_year__lte=to_year)
    
    try:
        filtered_data
        if estate_type != 'Любой':
            filtered_data = filtered_data.filter(type=estate_type)
    except: 
        filtered_data = annoucements
        if estate_type != 'Любой':  
            filtered_data = filtered_data.filter(type=estate_type)

    try:
        filtered_data
        if trash != []:
            filtered_data = filtered_data.filter(ceilings__gte=10)
    except: 
        filtered_data = annoucements
        if trash != []:
            filtered_data = filtered_data.filter(ceilings__gte=10)


    try:
        filtered_data
        if search_text:
            filtered_data = filtered_data.filter(title__icontains=search_text)

    except: 
        filtered_data = annoucements
        if search_text:
            filtered_data = filtered_data.filter(Q(article_text__contains=F(search_text)))

    try:
        compilations = Compilation.objects.filter(creator=user)
    except: 
        compilations = []

    content = {'estate_category': estate_category, 'square1': square1, 'square2': square2, 'price1': price1, 'price2': price2,
               'district': district, 'owner': owner, 'usability': usability, 'conditions': conditions, 'from_ceiling': from_ceiling,
               'to_ceiling': to_ceiling, 'from_year': from_year, 'to_year': to_year, 'estate_type': estate_type, 'trash': trash,
               'filtered_data': filtered_data, 'compilations': compilations, 'search_text': search_text}
    template = loader.get_template('estate/searched.html')
    return HttpResponse(template.render(content, request))

def flats(request):
    annoucements = Annoucement.objects.all()
    flats = annoucements.filter(category='Квартира')
    content = {'flats': flats}
    template = loader.get_template('estate/category_page.html')
    return HttpResponse(template.render(content, request))

def houses(request):
    annoucements = Annoucement.objects.all()
    houses = annoucements.filter(category='Дом')
    content = {'houses': houses}
    template = loader.get_template('estate/category_page.html')
    return HttpResponse(template.render(content, request))

def rooms(request):
    annoucements = Annoucement.objects.all()
    rooms = annoucements.filter(category='Комната')
    content = {'rooms': rooms}
    template = loader.get_template('estate/category_page.html')
    return HttpResponse(template.render(content, request))

def chat(request):
    content = {}
    template = loader.get_template('estate/chat.html')
    return HttpResponse(template.render(content, request))

def open_chat(request, arg=''):
    try:
        annoucement = Annoucement.objects.get(id=arg)
        creator = annoucement.creator
        user = request.user
        creator_id = creator.id
        user_id = user.id
        my_chats = Chat.objects.filter(sender=user_id)
        reciever_chats = Chat.objects.filter(reciever=user_id)

        if user.is_anonymous:
            return redirect(reverse('login_warning_chat'))

        if reciever_chats:
            my_chats = my_chats | reciever_chats

        try:
            current_chat = Chat.objects.filter(sender=user_id).filter(reciever=creator_id)[0]
        except:
            current_chat = ''

    except:
        annoucement = creator = current_chat = '' 
        user = request.user
        user_id = user.id
        my_chats = Chat.objects.filter(sender=user_id)
        reciever_chats = Chat.objects.filter(reciever=user_id)
        if reciever_chats:
            my_chats = my_chats | reciever_chats

        if user.is_anonymous:
            return redirect(reverse('login_warning_chat'))

    content = {'annoucement': annoucement, 'creator': creator, 'my_chats': my_chats, 'current_chat': current_chat,
               'reciever_chats': reciever_chats}
    template = loader.get_template('estate/open_chat.html')
    return HttpResponse(template.render(content, request))

def change_chat(request, chat, arg=''):
    try:
        annoucement = Annoucement.objects.get(id=arg)
    except: annoucement = 'change'
    new_chat = Chat.objects.get(id=chat)
    creator = new_chat.reciever
    reciever = new_chat.sender
    user = request.user
    creator_id = creator.id
    creator_id2 = new_chat.sender.id
    user_id = user.id
    my_chats = Chat.objects.filter(sender=user_id)
    reciever_chats = Chat.objects.filter(reciever=user_id)
    if reciever_chats:
        my_chats = my_chats | reciever_chats
    try:
        current_chat = Chat.objects.filter(sender=user_id).filter(reciever=creator_id)[0]
    except:
        current_chat = Chat.objects.filter(sender=creator_id2).filter(reciever=user_id)[0]
    content = {'annoucement': annoucement, 'new_chat': new_chat, 'creator': creator, 'my_chats': my_chats, 
               'current_chat': current_chat, 'creator_id': creator_id, 'user_id': user_id, 'creator_id2': creator_id2, 
               'reciever': reciever, 'reciever_chats': reciever_chats}
    template = loader.get_template('estate/open_chat.html')
    return HttpResponse(template.render(content, request))

def send_first_message(request, arg):
    annoucement = Annoucement.objects.get(id=arg)
    message = request.POST.get('message')
    date = timezone.now()
    creator = annoucement.creator
    user = request.user
    user_id = user.id
    creator_id = creator.id
    try:
        existed_chat = Chat.objects.filter(sender=user_id).filter(reciever=creator_id)[0]
    except: existed_chat = []
    chat = Chat(sender=user, reciever=creator, creation_date=date)
    my_chats = Chat.objects.filter(sender=user_id)
    reciever_chats = Chat.objects.filter(reciever=user_id)
    if reciever_chats:
        my_chats = my_chats | reciever_chats

    if existed_chat != []:
        sender = user
        reciever = creator
        message = Message(chat=existed_chat, writer=user, message=message, date=date)
        message.save()
        current_chat = existed_chat
    else: 
        sender = user
        reciever = creator
        chat = Chat(sender=sender, reciever=reciever, creation_date=date)
        chat.save()
        message = Message(chat=chat, writer=user, message=message, date=date)
        message.save()
        current_chat = chat
    
    content = {'annoucement': annoucement, 'creator': creator, 'existed_chat': existed_chat, 'current_chat': current_chat, 
               'my_chats': my_chats}
    template = loader.get_template('estate/open_chat.html')
    return redirect(request.META['HTTP_REFERER'])

def send_message(request, chat, arg=''):
    try:
        annoucement = Annoucement.objects.get(id=arg)
    except: annoucement = 'change'
    new_chat = Chat.objects.get(id=chat)
    message = request.POST.get('message')
    date = timezone.now()
    creator = new_chat.reciever
    reciever = new_chat.sender
    user = request.user
    user_id = user.id
    creator_id = creator.id
    current_chat = new_chat
    my_chats = Chat.objects.filter(sender=user_id)
    reciever_chats = Chat.objects.filter(reciever=user_id)
    if reciever_chats:
        my_chats = my_chats | reciever_chats
    try:
        message = Message(chat=new_chat, writer=user, message=message, date=date)
        message.save()
    except:
        pass
    
    content = {'new_chat': new_chat, 'creator': creator, 'current_chat': current_chat, 'my_chats': my_chats, 
               'annoucement': annoucement, 'reciever': reciever}
    template = loader.get_template('estate/open_chat.html')
    return redirect(request.META['HTTP_REFERER'])