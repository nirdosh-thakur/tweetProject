from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit = False) # WE dont want to save it in db at this point of time
            tweet.user = request.user         # with every form user is attached
            tweet.save()
            return redirect('tweet_list')
    else:
        # Give Empty Form to User
        form = TweetForm()
    return render(request, "tweet_form.html", {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user) # Check at Tweet Model/Table at pk tweet_id
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance = tweet)
        if form.is_valid():
            tweet = form.save(commit = False) # WE dont want to save it in db at this point of time
            tweet.user = request.user         # with every form user is attached
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance = tweet)
    return render(request, "tweet_form.html", {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user) # Check at Tweet Model/Table at pk tweet_id
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_conirm_delete.html', {'tweet': tweet})



# User

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False) # WE dont want to save it in db at this point of time
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # Directly do login once register successfully
            login(request, user)

            # Redirect to landing Page
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})