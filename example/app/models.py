# Define a custom User class to work with django-social-auth
from django.db import models
from django.db import connection
from time import time

def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % ('', filename)

class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        return self.model._default_manager.create(username=username)


class CustomUser(models.Model):
    username = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    def is_authenticated(self):
        return True

class Article(models.Model) :
    title = models.CharField(max_length=200)
    body = models.TextField()
    thumbnail = models.FileField(upload_to=get_upload_file_name)

    def __unicode__(self):
        return self.title


    @staticmethod
    def searchdetail(tid):
        # create a cursor
		arguments=(tid)
        #cur = connection.cursor()
		cur=connection.cursor()
		#cur.execute("{call PROC_Detail(tid)}")
		#cur.execute("{call PROC_Detail(?)}",(1))
		#temp = 'call PROC_Detail('+tid+')'
		cur.execute('''Select * from prices''')
        # execute the stored procedure passing in
        # search_string as a parameter

        # grab the results
		# context['my_data'] = get_my_data()
        #tables = cur.fetchall()
		tables=cur.fetchall()
        #cur.close()
		cur.close()
        # wrap the results up into Document domain objects
		return tables
        #return tables


    @staticmethod
    def search():
        # create a cursor
        cur = connection.cursor()
        # execute the stored procedure passing in
        # search_string as a parameter
        cur.execute('SELECT * FROM prices')
        #cur.callproc('PROC_Search')
        # grab the results
		# context['my_data'] = get_my_data()
        tables = cur.fetchall()
        cur.close()
        # wrap the results up into Document domain objects
        return tables





