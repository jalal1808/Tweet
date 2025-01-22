from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-creation_time')
    return render(request, 'tweet_list.html', {'tweets':tweets})

@login_required
def tweet_create(request):
    if request.method == "POST":
      form = TweetForm(request.POST, request.FILES)
      if form.is_valid():
          tweet = form.save(commit=False)
          tweet.user = request.user
          tweet.save()
          return redirect('tweet_list')
    else:
        form =TweetForm()
        print("Tweet Is Created....")
    return render(request, 'tweet_form.html', {'form':form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form':form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    else:
        return render(request, 'tweet_confirm_delete.html', {'tweet':tweet})
    
def register(request):
     if request.method == "POST":
         form =UserCreationForm(request.POST)
         if form.is_valid():
             user = form.save(commit=False)
             user.set_password(form.cleaned_data['password1'])
             user.save()
             login(request, user)
             return redirect('tweet_list')

     else:
         form = UserCreationForm()    

     return render(request, 'registration/register.html', {'form':form})

def tweet_search(request):
    username = request.GET.get('username', '')
    tweets = Tweet.objects.filter(user__username__icontains=username) if username else []
    return render(request, 'tweet_search.html', {'tweets': tweets, 'username': username})
