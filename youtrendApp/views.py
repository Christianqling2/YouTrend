from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render, redirect

from youtrendApp.forms import CreateUserForm
from youtrendApp.decorators import unauthenticated_user

from tensorflow.keras.models import load_model
from nltk.tokenize import word_tokenize
import pickle
import re
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.stem import PorterStemmer, WordNetLemmatizer
import numpy as np

model = load_model('./youtrendApp/my_model.h5')

with open('./youtrendApp/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('./youtrendApp/topics.pkl', 'rb') as f:
    topics = pickle.load(f)
    topics = np.array(topics)


def kl_divergence(p, q):
    return np.sum(np.where(p != 0, p * np.log(p / q), 0))


def process(text):
    text = text.strip()
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'(\d+)([a-zA-Z])', '\g<1> \g<2>', text)
    text = re.sub(r'(\d+) (th|st|nd|rd) ', '\g<1>\g<2> ', text)
    text = re.sub(r'(\d+),(\d+)', '\g<1>\g<2>', text)
    text = re.sub(r'(\d+)(e)(\d+)', '\g<1> \g<3>', text)
    text = re.sub(r"\b(I|i)(I|i)+ng\b", "ing",
                  text)  # this one is causing few issues(fixed via monkey patching in other dicts for now), need to check it..
    text = re.sub(r"(-+|\.+)", " ", text)

    text = text.strip()
    text = re.sub('\s+', ' ', text)

    # 1- Stemming
    porter_stemmer = PorterStemmer()
    wordnet_lemmatizer = WordNetLemmatizer()

    words_stem = porter_stemmer.stem(text)

    text = wordnet_lemmatizer.lemmatize(words_stem)

    stop_words = stopwords.words('english')
    # stopwords_dict = Counter(stop_words)

    blacklist = ["lil", "ft", "got", "get", "mv", "first", "vs", "highlights", "channel", "new", "official", "best",
                 "check", "latest", "also", "thanks", "join", "»", "new", "video", "content", "thanks", "»", "tiktok",
                 "s", "’", "–", '“', "im", '”', "v", "—", "w", "g", "‘", "u", "►", "m", "i", "t", "de", "us",
                 "instagram", "twitter", "videos", "subscribe", "go", "la", "every", "facebook", "watch", "youtube",
                 "follow", "like"]
    blacklist2 = ["thi", "tak", "mo", "jo", "b", "minut", "mo", "ksi", "fnaf", "j", "vs", "x", " x", "x ", "back",
                  "short", "official", "el", "ofici", "gets", "l", "n", "v", "r", "el", "music"]
    text = ' '.join([word for word in text.split() if word not in stop_words])
    text = word_tokenize(text)
    list = []
    for i in text:
        if i not in blacklist:
            if i not in blacklist2:
                list.append(i)
    text = list
    sentence = ""
    for word in text:
        sentence = sentence + " " + word
    text = sentence

    max_length = 132
    text = [text]
    data = tokenizer.texts_to_sequences(text)
    data = pad_sequences(data, maxlen=max_length, padding='post')
    return data


def How_trend(video_title, description):
    data = process(video_title + " " + description)
    data = model.predict(data)
    return np.dot(data, topics) * 10 + 1, np.argmax(data)


def Similar(v1, v2):
    v1 = process(v1)
    v2 = process(v2)
    v1 = model(v1)
    v2 = model(v2)
    return np.exp(-kl_divergence(v1, v2))


def dict_fetch_all(cursor):
    # return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def base_view(request):
    return render(request, 'base.html')


@login_required(login_url='login')
def home(request):
    search_results = []
    query_string = None

    if request.method == "POST":
        query_string = request.POST['query']

        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM production.Video WHERE video_title LIKE '%{query_string}%'"
            )
            search_results = dict_fetch_all(cursor)

    return render(request, 'home.html', {
        'search_results': search_results,
        'query_string': query_string
    })


@login_required(login_url='login')
def predict(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM production.User WHERE auth_user_id=%s",
            (request.user.id,)
        )
        user_id = dict_fetch_all(cursor)[0]['id']

    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        tags = request.POST['tags']

        trend, category_id = How_trend(title, description + " " + tags)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT category_name FROM production.Category WHERE id=%s", (category_id,))
            result = cursor.fetchone()
        if result:
            category_name = result[0]
        else:
            category_name = "Normal video"

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO production.VideoProposal (title, category_id, description, tags, user_id, trend_index)"
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (title, category_id, description, tags, user_id, float(trend))
            )
        return render(request, 'prediction.html', {
            'trend_index': trend, 'category_name': category_name})

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, category_name FROM production.Category"
        )
        categories = dict_fetch_all(cursor)

        cursor.execute(
            "SELECT id, region_name FROM production.Region"
        )
        regions = dict_fetch_all(cursor)

        cursor.execute(
            "SELECT vp.id, title, category_name, tags, description, trend_index FROM production.VideoProposal vp JOIN production.Category C on C.id = vp.category_id WHERE user_id=%s",
            (user_id,)
        )
        previous_ideas = dict_fetch_all(cursor)

    return render(request, 'predict.html', {
        'previous_ideas': previous_ideas,
        'categories': categories,
        'regions': regions
    })


def visualize_view(request):
    comparison_results = []
    region1 = None
    region2 = None
    comparison_text = ""
    comp_winner = ""
    top15 = []

    if request.method == "POST":
        region1 = request.POST['region1']
        region2 = request.POST['region2']

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT region_name, AVG(likes) FROM production.Video V JOIN production.Region R on R.id=V.region_id "
                "WHERE R.id in (%s, %s) GROUP BY region_name",
                (region1, region2)
            )
            comparison_results = dict_fetch_all(cursor)
        comp_winner = comparison_results[0]
        if len(comparison_results) > 1 and comparison_results[1]['AVG(likes)'] > comparison_results[0]['AVG(likes)']:
            comp_winner = comparison_results[1]
        comparison_text = "Videos from the " + comp_winner[
            'region_name'] + " region generally have more likes, with an average of " + str(
            comp_winner['AVG(likes)']) + " likes."
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, region_name FROM production.Region"
        )
        regions = dict_fetch_all(cursor)

    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT * FROM production.Video ORDER BY likes DESC LIMIT 15"
        )
        top15 = dict_fetch_all(cursor)

    return render(request, 'visualize.html', {
        'regions': regions,
        'comparison': comparison_results,
        'comparison_text': comparison_text,
        'top15': top15
    })


def like_video(request, video_id):
    pass


def unlike_video(request, video_id):
    pass


@login_required(login_url='login')
def update_prediction(request, prediction_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM production.User WHERE auth_user_id=%s",
            (request.user.id,)
        )
        user_id = dict_fetch_all(cursor)[0]['id']

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT vp.id, title, category_id, category_name, tags, description FROM production.VideoProposal vp JOIN production.Category C on C.id = vp.category_id WHERE user_id=%s and vp.id=%s",
            (user_id, prediction_id,)
        )
        previous_idea = dict_fetch_all(cursor)[0]

        cursor.execute(
            "SELECT id, category_name FROM production.Category"
        )
        categories = dict_fetch_all(cursor)

    if request.method == "POST":
        title = request.POST['title']
        category_id = request.POST['category']
        description = request.POST['description']
        tags = request.POST['tags']

        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE production.VideoProposal SET title = %s, description = %s, tags = %s, category_id = %s WHERE id = %s;",
                (title, description, tags, category_id, prediction_id,)
            )
            return redirect('predict')

    return render(request, "update_prediction.html", {
        'prediction_id': prediction_id,
        'previous_idea': previous_idea,
        'categories': categories
    })


@login_required(login_url='login')
def delete_prediction(request, prediction_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM production.VideoProposal WHERE id=%s",
            (prediction_id,)
        )
    return redirect('predict')


@login_required(login_url='login')
def explore_tags(request):
    search_results = []
    query_string = None

    if request.method == "POST":
        query_string = request.POST['query']
        param = f'|{query_string}|'

        with connection.cursor() as cursor:
            cursor.execute(
                "CALL tag_videos(%s)", (param,)
            )
            search_results = dict_fetch_all(cursor)
            print(search_results)

    return render(request, 'explore_tags.html', {
        'search_results': search_results,
        'query_string': query_string
    })



################################################################################
# login, logout, register functions
################################################################################
@unauthenticated_user  # user will redirect to home if already logged in
def register_user(request):
    """
    Creates a new user account.

    :param request: The django request object
    :return: render of registration page, redirect to login page on user creation
    """
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO production.User (username, email, auth_user_id) VALUES (%s, %s, %s)",
                (username, email, form.instance.id,)
            )
        messages.success(request, 'User ' + username + ' created successfully')
        return redirect('login')

    return render(request, 'register.html', {'form': form})


@unauthenticated_user
def login_user(request):
    """
    Login a user using username and password.

    :param request: The django request object
    :return: render of login page, redirect to home page on user login
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    context = {}
    return render(request, 'login.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')
