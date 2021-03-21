from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import FeedbackForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from .models import ReviewMovie, ReviewSeries

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from tmdbv3api import TMDb, Movie, TV

from keras.datasets import imdb
import re
from keras.models import load_model


tmdb = TMDb()
tmdb.api_key = '9ab4b2025cfde942c159fa3dd7787eba'
tmdb.language = 'en'
tmdb.debug = 'True'

model = load_model('model.h5')

# This function will generate movie rating.
def getRatingMovie(movieid):
    total_count = ReviewMovie.objects.filter(movieid=movieid).count()
    if total_count == 0:
        return 0
    positive_count = ReviewMovie.objects.filter(movieid=movieid).filter(sentiment=1).count()
    return round((positive_count/total_count)*100, 2)

# This function will generate series rating.
def getRatingSeries(seriesid):
    total_count = ReviewSeries.objects.filter(seriesid=seriesid).count()
    if total_count == 0:
        return 0
    positive_count = ReviewSeries.objects.filter(seriesid=seriesid).filter(sentiment=1).count()
    return round((positive_count/total_count)*100, 2)

#This function returns the sentiment and its probability.
def getSentiment(text):

    max_review_length = 500
    word_to_id = imdb.get_word_index()
    removeSC = re.compile("[^A-Za-z0-9 ]+")

    text = text.lower().replace("<br />", " ")
    text = re.sub(removeSC, "", text.lower())

    words = text.split()
    x = [word_to_id[word] if (word in word_to_id and word_to_id[word] <= 5000) else 0 for word in words]

    return model.predict(x)[0][0], model.predict_classes(x)[0][0]

# This function takes movie id as input and returns its name and poster.
def getMovieNamePoster(movie_id):
    id = int(movie_id)
    movie = Movie()
    s = movie.details(id)
    return s.original_title, s.poster_path

# This function takes series id as input and returns its name and poster.
def getSeriesNamePoster(series_id):
    id = int(series_id)
    series = TV()
    s = series.details(id)
    return s.name, s.poster_path

# User profile view
def profile(request):

    data = {}

    # Collecting all the reviews user have done.
    moviereviews = ReviewMovie.objects.filter(userid=request.user.username)
    seriesreviews = ReviewSeries.objects.filter(userid=request.user.username)
    count = moviereviews.count() + seriesreviews.count()

    userreviews = []
    for i in moviereviews:
        name, poster = getMovieNamePoster(i.movieid)
        temp = {'review': i.review, 'date': i.date, 'id': i.movieid, 'movieName': name, 'poster':poster, 'type': 'movie'}
        userreviews.append(temp)
        del temp

    for i in seriesreviews:
        name, poster = getSeriesNamePoster(i.seriesid)
        temp = {'review': i.review, 'date': i.date, 'id': i.seriesid, 'movieName': name, 'poster':poster, 'type': 'series'}
        userreviews.append(temp)
        del temp

    # Generating level of user
    if count > 0 and count <= 20:
        data['level'] = 'Iron'
    elif count > 20 and count <= 50:
        data['level'] = 'Bronze'
    elif count > 50 and count <= 100:
        data['level'] = 'Silver'
    elif count > 100 and count <= 250:
        data['level'] = 'Gold'
    elif count > 250 and count <= 500:
        data['level'] = 'Platinum'
    elif count > 500 and count <= 1000:
        data['level'] = 'Diamond'
    elif count > 1000 and count <= 10000:
        data['level'] = 'Immortal'
    elif count > 10000:
        data['level'] = 'Radient'
    else:
        data['level'] = 'Un-Ranked'
    

    data['reviews'] = userreviews
    data['count'] = count

    return render(request, 'rhub/profile.html', {'data': data})

# Create your views here.
def register(request):

    # This part runs if some post request is done.
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        # Checking if the form is valid or not.
        if form.is_valid():

            # If the form is valid, then we are saving the form and redirecting user to home page.
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            messages.success(request, 'Account was created for '+ username)
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect(home)
    else:
        form = CreateUserForm()
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)

# This view is for home page.
def home(request):

    # This method runs when post request is done.
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        # If form is valid then it saves it.
        if form.is_valid():
            form.save()

    data = {}

    #setting up movies
    movie = Movie()
    latest = movie.popular()
    upcoming = movie.upcoming()

    context = {}
    count = 0

    for l in latest:
        c = {'id':l.id, 'poster':l.poster_path}
        context["m_id" + str(count)] = c
        count += 1

    data['latest_movies'] = context

    context = {}
    count = 0

    for up in upcoming:
        c = {'id':up.id, 'poster':up.poster_path}
        context["m_id" + str(count)] = c
        count += 1

    data['upcoming_movies'] = context

    #setting up series
    tv = TV()
    popular = tv.popular()
    top_rated = tv.top_rated()
    
    count = 0
    context = {}
    
    for p in popular:
        c = {'id':p.id, 'poster':p.poster_path}
        context["m_id" + str(count)] = c
        count += 1
    
    data['latest_series'] = context

    count = 0
    context = {}
    
    for tr in top_rated:
        c = {'id':tr.id, 'poster':tr.poster_path}
        context["tr_id" + str(count)] = c
        count += 1
    
    data['top_series'] = context

    #setting up feedback form
    form = FeedbackForm()

    data['form'] = form

    return render(request, 'rhub/home.html', data)

# This view is for about page.
def about(request):
    
    context = {}
    return render(request, 'rhub/about.html', context)

# This view will display movie gallery.
def movies(request):

    movie = Movie()

    context = {}
    data = {}
    data['page'] = 1
    data['query'] = ""

    if request.method == 'POST':

        if 'submit-btn' in request.POST:

            if request.POST['search'] == "":
                return redirect(movies)

            query = request.POST['search']
            search = movie.search(query)
    
            count = 0
            for p in search:
                c = {'id':p.id, 'title':p.title, 'poster':p.poster_path, 'overview':p.overview, 'vote': getRatingMovie(int(p.id))}
                context["m_id" + str(count)] = c
                count += 1

            data['data_movies'] = context
            data['page'] = 1
            data['query'] = query
        
        if 'next' in request.POST:

            page = int(request.POST['page'])

            if request.POST['search'] == "":

                popular = movie.popular(page=page + 1 )
                count = 0
                for p in popular:
                    c = {'id':p.id, 'title':p.title, 'poster':p.poster_path, 'overview':p.overview, 'vote': getRatingMovie(int(p.id))}
                    context["m_id" + str(count)] = c
                    count += 1
                page_count = int(movie.total_pages)

            else:
                query = request.POST['search']
                search = movie.search(query, page+1)
                if len(search) > 0:
                    count = 0
                    for p in search:
                        c = {'id':p.id, 'title':p.title, 'poster':p.poster_path, 'overview':p.overview, 'vote': getRatingMovie(int(p.id))}
                        context["m_id" + str(count)] = c
                        count += 1
                page_count = int(movie.total_pages)
                    
            data['data_movies'] = context
            data['page'] = page+1
            data['total_pages'] = page_count
            data['query'] = request.POST['search']

        if 'prev' in request.POST:
            page = int(request.POST['page'])
            if request.POST['search'] == "":
                popular = movie.popular(page=page-1)
                count = 0
                for p in popular:
                    c = {'id':p.id, 'title':p.title, 'poster':p.poster_path, 'overview':p.overview, 'vote': getRatingMovie(int(p.id))}
                    context["m_id" + str(count)] = c
                    count += 1
                page_count = int(movie.total_pages)
            
            else:
                query = request.POST['search']
                search = movie.search(query, page-1)
                if len(search) > 0:
                    count = 0
                    for p in search:
                        c = {'id':p.id, 'title':p.title, 'poster':p.poster_path, 'overview':p.overview, 'vote': getRatingMovie(int(p.id))}
                        context["m_id" + str(count)] = c
                        count += 1
                page_count = int(movie.total_pages)

            data['data_movies'] = context
            data['page'] = page -1
            data['total_pages'] = page_count
            data['query'] = request.POST['search']

        return render(request, 'rhub/movies.html', data)
    
    else:

        popular = movie.popular()
    
        count = 0
        for p in popular:
            c = {'id':p.id, 'title':p.title, 'poster':p.poster_path, 'overview':p.overview, 'vote': getRatingMovie(int(p.id))}
            context["m_id" + str(count)] = c
            count += 1

        data['data_movies'] = context
        
        data['page'] = 1
        return render(request, 'rhub/movies.html', data)

# This view will display series gallery.
def series(request):

    tv = TV()

    context = {}
    data = {}
    data['page'] = 1
    data['query'] = ""

    if request.method == 'POST':

        if 'submit-btn' in request.POST:

            query = request.POST['search']
            search = tv.search(query)
    
            count = 0
            for p in search:
                c = {'id':p.id, 'title':p.name, 'poster':p.poster_path, 'overview':p.overview, 'vote':getRatingSeries(int(p.id))}
                context["m_id" + str(count)] = c
                count += 1
            page_count = int(tv.total_pages)

            data['data_series'] = context
            data['page'] = 1
            data['query'] = query
            data['total_pages'] = page_count
        
        if 'next' in request.POST:

            page = int(request.POST['page'])

            if request.POST['search'] == "":

                popular = tv.popular(page = page + 1 )

                count = 0
                for p in popular:
                    c = {'id':p.id, 'title':p.name, 'poster':p.poster_path, 'overview':p.overview, 'vote':getRatingSeries(int(p.id))}
                    context["m_id" + str(count)] = c
                    count += 1

                page_count = int(tv.total_pages)

            else:

                query = request.POST['search']
                search = tv.search(query, page+1)

                if len(search) > 0:

                    count = 0
                    for p in search:
                        c = {'id':p.id, 'title':p.name, 'poster':p.poster_path, 'overview':p.overview, 'vote':getRatingSeries(int(p.id))}
                        context["m_id" + str(count)] = c
                        count += 1
                
                page_count = int(tv.total_pages)
                    
            data['data_series'] = context
            data['page'] = page+1
            data['total_pages'] = page_count
            data['query'] = request.POST['search']

        if 'prev' in request.POST:
            page = int(request.POST['page'])
            if request.POST['search'] == "":
                popular = tv.popular(page=page-1)
                count = 0
                for p in popular:
                    c = {'id':p.id, 'title':p.name, 'poster':p.poster_path, 'overview':p.overview, 'vote':getRatingSeries(int(p.id))}
                    context["m_id" + str(count)] = c
                    count += 1
                page_count = int(tv.total_pages)
            
            else:
                query = request.POST['search']
                search = tv.search(query, page-1)
                if len(search) > 0:
                    count = 0
                    for p in search:
                        c = {'id':p.id, 'title':p.name, 'poster':p.poster_path, 'overview':p.overview, 'vote':getRatingSeries(int(p.id))}
                        context["m_id" + str(count)] = c
                        count += 1
                page_count = int(tv.total_pages)

            data['data_series'] = context
            data['page'] = page -1
            data['total_pages'] = page_count
            data['query'] = request.POST['search']

        return render(request, 'rhub/series.html', data)
    
    else:

        popular = tv.popular()
    
        count = 0
        for p in popular:
            c = {'id':p.id, 'title':p.name, 'poster':p.poster_path, 'overview':p.overview, 'vote':getRatingSeries(int(p.id))}
            context["m_id" + str(count)] = c
            count += 1
        page_count = int(tv.total_pages)

        data['data_series'] = context
        data['total_pages'] = page_count
        data['page'] = 1
        return render(request, 'rhub/series.html', data)

# This view will display specific movie details, it takes movie id as input.
def singleMovie(request, movie_id):

    data = {}
    id = int(movie_id)

    # Fetching all the reviews of that movie.
    reviews = ReviewMovie.objects.filter(movieid=id)

    userReviews = []
    if reviews != None:
        temp = {}
        for review in reviews:
            userReviews.append({'review': review.review, 'date': review.date, 'userid': review.userid})
        data['userReview'] = userReviews
    else:
        data['userReview'] = None

    # Checking if the logged in user has reviewed it or not.
    check = ReviewMovie.objects.filter(movieid=id).filter(userid=request.user.username)

    if check.exists():
        data['check'] = True
    else:
        data['check'] = False

    # If user send review request this part is executed.
    if request.method == 'POST':
        username = request.user.username
        text = request.POST['review']

        # calling getSentiment function to get probability and sentiment of reviews.
        prob, sen = getSentiment(text)


        r = ReviewMovie(
            userid = username,
            movieid = movie_id,
            review = request.POST['review'],
            sentiment = sen,
            probability= prob
        )
        #form.data['sentiment'], form.data['probability'] = sentiment.getsentiment(form.cleaned_data['review'])

        # Saving the review and sending a confirmation message.
        r.save()
        messages.success(request, 'Your review has been saved successfully.')
        return redirect(singleMovie, id)


    # Setting movie details
    movie = Movie()
    s = movie.details(id)

    # Arranging Movie data
    cast = []
    temp = s.casts.cast
    length = min(len(temp),20)
    for i in range(length):
        if temp[i].known_for_department == "Acting":
            cast.append({'original_name': temp[i].original_name, 'character': temp[i].character, 'photo': temp[i].profile_path})

    crew = []
    temp = s.casts.crew
    length = min(len(temp),20)
    for i in range(length):
        crew.append({'department': temp[i].department, 'name': temp[i].original_name, 'photo': temp[i].profile_path})
    del temp

    data['title'] = s.original_title
    data['description'] = s.overview
    data['release_day'] = s.release_date
    data['status'] = s.status
    data['country'] = s.production_countries[0].name
    data['runtime'] = s.runtime
    data['budget'] = s.budget
    data['revenue'] = s.revenue
    if s.trailers.youtube == []:
        data['trailer'] = 'None'
    else:
        data['trailer'] = s.trailers.youtube[0].source
    data['adult'] = s.adult
    data['poster'] = s.poster_path
    data['votes'] = getRatingMovie(movieid=id)
    data['negative'] = 100 - data['votes']
    data['cast'] = cast
    data['crew'] = crew

    context = {}
    context['data'] = data


    return render(request, 'rhub/info.html', context)

# This view will display specific series details, it takes series id as input.
def singleSeries(request, series_id):

    data = {}
    id = int(series_id)
    
    # Fetching all the reviews of that series
    reviews = ReviewSeries.objects.filter(seriesid=id)

    userReviews = []
    if reviews.exists():
        temp = {}
        for review in reviews:
            userReviews.append({'review': review.review, 'date': review.date, 'userid': review.userid})
        data['userReview'] = userReviews
    else:
        data['userReview'] = None

    # Checking if the logged in user has reviewed it or not.
    check = ReviewSeries.objects.filter(seriesid=id).filter(userid=request.user.username)

    if check.exists():
        data['check'] = True
    else:
        data['check'] = False

    # If user send review this part is executed.
    if request.method == "POST":
        username = request.user.username
        series_id = int(series_id)
        text = request.POST['review']
        
        # Calling getSentiment function to get probability and sentiment of review.
        prob, sen = getSentiment(text)

        x = ReviewSeries(
            userid = username,
            seriesid = series_id,
            review = text,
            sentiment = sen,
            probability = prob
        )

        # Saving the review and sending a conformation message.
        x.save()
        messages.success(request, 'Your review has been saved successfully.')
        return redirect(singleSeries, id)

    # setting series details
    series = TV()
    s = series.details(id)

    # Arranging series data
    cast = []
    temp = s.credits.cast
    length = min(len(temp),20)
    for i in range(length):
        if temp[i].known_for_department == "Acting":
            cast.append({'original_name': temp[i].original_name, 'character': temp[i].character, 'photo': temp[i].profile_path})

    crew = []
    temp = s.credits.crew
    length = min(len(temp),20)
    for i in range(length):
        crew.append({'department': temp[i].department, 'name': temp[i].original_name, 'photo': temp[i].profile_path})
    del temp

    data['title'] = s.name
    data['homepage'] = s.homepage
    data['networks'] = [{'name': x.name, 'logo': x.logo_path} for x in s.networks]
    data['description'] = s.overview
    data['tagline'] = s.tagline
    data['languages'] = s.languages
    data['seasons'] = s.seasons
    data['created_by'] = [{'name': x.name, 'photo': x.profile_path} for x in s.created_by]
    data['status'] = s.status
    data['country'] = s.origin_country
    data['trailer'] = s.videos.results[0].key
    data['type'] = s.type
    data['cast'] = cast
    data['crew'] = crew
    data['runtime'] = s.episode_run_time
    data['release_date'] = s.first_air_date
    data['votes'] = getRatingSeries(seriesid=id)
    data['negative'] = 100 - data['votes']
    data['poster'] = s.poster_path

    context = {}
    context['data'] = data

    return render(request, 'rhub/seriesInfo.html', context)