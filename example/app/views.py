from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template import Context
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from forms import ArticleForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.http import HttpResponse
from app.models import Article
from django.template.loader import get_template

from social_auth import __version__ as version


def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('home.html', {'version': version},
                                  RequestContext(request))


@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return render_to_response('done.html', ctx, RequestContext(request))


def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


def form(request):
    if request.method == 'POST' and request.POST.get('username'):
        request.session['saved_username'] = request.POST['username']
        backend = request.session['partial_pipeline']['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('form.html', {}, RequestContext(request))


def form2(request):
    if request.method == 'POST' and request.POST.get('first_name'):
        request.session['saved_first_name'] = request.POST['first_name']
        backend = request.session['partial_pipeline']['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('form2.html', {}, RequestContext(request))


def close_login_popup(request):
    return render_to_response('close_popup.html', {}, RequestContext(request))


def create(request):
    if request.POST:
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return  HttpResponseRedirect('/articles/all')

    else:
        form = ArticleForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('create_article.html', args)


def create1(request):

    import csv
    import sqlite3


    """

    @type request: object
    """



    with open('uploaded_files/test.csv', 'rb') as csvfile:
        if request.POST:
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                filename123 = request.FILES['thumbnail'].name


                # Create the database
                connection = sqlite3.connect('test.db')
                cursor = connection.cursor()

                # Create the table
                #cursor.execute('DROP TABLE IF EXISTS prices')
                #cursor.execute('CREATE TABLE  prices ( Code text, Description text, Price integer) ')
                #connection.commit()



                # Load the CSV file into CSV reader
                csvfile = open('uploaded_files/_'+filename123, 'rb')

                #csvfile = request.FILES['id_thumbnail'].name
                creader = csv.reader(csvfile, delimiter=',', quotechar='|')

                # Iterate through the CSV reader, inserting values into the database
                for t in creader:
                    cursor.execute('INSERT INTO  prices VALUES (?,?,?)', t )

                # Close the csv file, commit changes, and close the connection
                csvfile.close()
                connection.commit()
                connection.close()




                return  HttpResponseRedirect('/search/')

        else:
            form = ArticleForm()

            args = {}
            args.update(csrf(request))

            args['form'] = form

            return render_to_response('create_article.html', args)


def search_page(request):
	name = 'Rohit'
	t = get_template('search.html')
	nl_table = Article.search()
	html = t.render(Context({'nl_table' : nl_table}))
	return HttpResponse(html)


def search_page_old(request):

    import sqlite3
    t = get_template('search.html')
    connection = sqlite3.connect('test.db')
    cur = connection.cursor()
    cur.execute('''Select description from prices''')
    nl_table = cur.fetchall()
    connection.commit()
    connection.close()
    c = RequestContext({"my_name": "Adrian"})
    #html=t.render(RequestContext({'nl_table' : nl_table  }))
    #html = ''
    html = t.render(c)
    return HttpResponse(html)








