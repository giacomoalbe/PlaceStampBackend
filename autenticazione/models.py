from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class PSUserManager(BaseUserManager):

	def create(self, **kwargs):

		# Wrapper della funzione create_user, per compatibilita
		# con rest_framework che chiama questa per creare utente
		return self.create_user(**kwargs)

	def create_user(self, **kwargs):

		# Controllo che i parametri abbiano valori corretti
		email = kwargs.get('email')
		password = kwargs.get('password')
		nome = kwargs.get('nome')
		cognome = kwargs.get('cognome')
		account = self.model(email=email, nickname = kwargs.get('nickname'),
							 nome = nome, cognome = cognome)
		account.set_password(password)
		account.save()

		return account

	def create_superuser(self, email, password, **kwargs):

		account = self.create_user(email, password, **kwargs)
		account.is_admin = True
		account.save()

		return account

	def delete_user(self, id):

		if self.get(pk=id) is not None:
			self.get(pk=id).delete()
		else:
			raise ValueError("Utente non presente!")	

class PSUser(AbstractBaseUser):

	email = models.EmailField(unique=True)
	nickname = models.CharField(max_length=40, unique=True)

	nome = models.CharField(max_length=255, blank=True)	
	cognome = models.CharField(max_length=255, blank=True)

	# QUesto e il manager degli utenti
	objects = PSUserManager()

	# Modificato al momento della creazione dell'account
	created_at = models.DateTimeField(auto_now_add=True)
	# Modificato ogni volta che questo record viene salvato
	updated_at = models.DateTimeField(auto_now=True)

	is_admin = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['nickname']

class PostManager(models.Manager):

	def get_from_user(self, id):
		
		try:
			user = PSUser.objects.get(pk=id)
			return super(PostManager, self).get_queryset().filter(owner=user)
		except:	
			return None

	def create(self, owner, title, content):

		newPost = super(PostManager, self).create(owner=owner, title=title, content=content)
		return newPost

	def get_queryset(self):
		return super(PostManager, self).get_queryset()


class Post(models.Model):

	owner = models.ForeignKey('PSUser', related_name = 'post')
	content = models.CharField(max_length=400)
	title = models.CharField(max_length=40)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	#objects = PostManager()



# About Serializer Class

class Owner(models.Model):

	name = models.CharField(max_length=40)
	surname = models.CharField(max_length=40)

	def __str__(self):

		return self.name + " " + self.surname

class Car(models.Model):

	owner = models.ForeignKey(Owner)

	name = models.CharField(max_length=40)
	marchio = models.CharField(max_length=40)

class Foto(models.Model):

	image = models.URLField(blank=True, max_length=254)
	compass = models.IntegerField(blank=True)
	latitude = models.FloatField(blank=True)
	longitude = models.FloatField(blank=True)
	color = models.CharField(blank=True, default="256,256,256", max_length = 11)
	created_at = models.DateTimeField(auto_now_add=True)
