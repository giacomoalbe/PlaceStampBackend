from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from django.db import *

from rest_framework import status, generics, permissions, views
from rest_framework.response import Response

from autenticazione.models import PSUser as user
from autenticazione.models import Post, Owner, Car 

from autenticazione.serializers import PSUserSerializer as userSerializer
from autenticazione.serializers import PostSerializer, OwnerSerializer, CarSerializer

from autenticazione.permissions import IsOwnerOrReadOnly

from django.contrib.auth import authenticate, login, logout

import sys

"""
# Response che ritorna contenuto JSON

class JSONResponse(HttpResponse):

	def __init__(self, data, **kwargs):

		# Formattiamo il contenuto in JSON
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'

		# Dopo aver aggiunto quello che volevamo,
		# chiamiamo il costruttore superiore
		super(JSONResponse, self).__init__(content, **kwargs)

"""

# View per la lista di utenti
"""
@api_view(['GET', 'POST'])
def user_list(request, format = None):

	if request.method == 'GET':

		utenti = user.objects.all()
		utentiSerialized = userSerializer(utenti, many=True)

		# Usiamo la response appena creata per mandare il contenuto in JSON
		return Response(utentiSerialized.data)

	elif request.method == 'POST':

		# Creiamo un nuovo utente
		nuovoUserSerialized = userSerializer(data=data)

		# Verifichiamo che quello che abbiamo in JSON sia un nuovo 
		# utente valido!

		if nuovoUserSerialized.is_valid():

			# Creiamo una nuova istanza del model
			nuovoUserSerialized.save()
			return Response(nuovoUserSerialized.data, status=status.HTTP_201_CREATED)

		return Response(nuovoUserSerialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def utente_detail(request, id, format=None):

	try:
		utente = user.objects.get(pk=id)
	except:
		return HttpResponse(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':

		# Diamo i dettagli del nuovo utente
		userSerialized = userSerializer(utente)
		return Response(userSerialized.data)

	elif request.method == 'PUT':

		# Modifichiamo alcuni campi dell'utente corrente
		userSerialized = userSerializer(utente, data=data)

		if userSerialized.is_valid():
			userSerialized.save()
			return Response(userSerialized.data)

		return Response(userSerialized.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':

		# Cancelliamo l'utente corrente
		utente.delete()
		return Response(status=status.HTTP_204_BAD_REQUEST)
"""

""" 
	Views per Login & logout
"""
class LoginView(views.APIView):

	def post(self, request, format=None):

		email = request.data.get('username', None)
		password = request.data.get('password', None)
		
		print(email)
		print(password)

		#email = 'culo@culo.com'
		#password = 'culo'
		account = authenticate(email=email, password=password)

		print(account)

		if account is not None:
			if account.is_active:

				login(request, account)

				accountSerial = userSerializer(account)

				return Response(accountSerial.data, 
								status=status.HTTP_200_OK)
			else:
				return Response({
					'status': 'Non autorizzato!',
					'message' : 'Account disabilitato'
 					}, status=status.HTTP_401_UNAUTHORIZED)
		else:

			return Response({
					'status': 'Non autorizzato',
					'message': 'Coppia user/pass non valida'
				},status=status.HTTP_401_UNAUTHORIZED)

	def get(self, request, format=None):

		# Only for debug

		for elem in request.data.keys():
			print(elem)
		email = request.data.get('userame', None)
		password = request.data.get('password', None)

		responseObj = {
			'status': 'ok',
			'email': email,
			'password': password,
			'data': request.data
		}
		
		return Response(responseObj)

class LogoutView(views.APIView):

	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, format=None):
		logout(request)
		return Response({}, status=status.HTTP_204_NO_CONTENT)
	def post(self, request, format=None):

		logout(request)
		return Response({}, status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListCreateAPIView):

	# Lista tutti gli utenti usando una classe predefinita
	queryset = user.objects.all()
	serializer_class = userSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):

	# Ottiene, modifica o cancella un'utente 
	queryset = user.objects.all()
	serializer_class = userSerializer

class NewUser(views.APIView):

	def post(self, request):

		try: 

			print(request.data['user'])
			# Creiamo un nuovo utente
			newUser = dict(request.data['user'])

			password = newUser.get('password', None)
			confirm_password = newUser.get('confirm_password', None)
			nickname = newUser.get('nickname', None)
			nome = newUser.get('nome', None)
			cognome = newUser.get('cognome', None)
			username = newUser.get('email', None)

			print(nickname)

			if password and confirm_password and password == confirm_password:
				
			# Controllo se e gia presente l'utente
			
				newAccount = user.objects.create_user(email=username, 
													  nickname = nickname, 
													  nome = nome, 
													  cognome= cognome, 
													  password = password) 
				userSerial = userSerializer(newAccount)
				return Response({'user': userSerial.data}, status=status.HTTP_201_CREATED)
			else:
				return Response({'errore': 'Le password non coincidono!'}, status=status.HTTP_400_BAD_REQUEST)

		except IntegrityError, err:


			# Stiamo chercando di inserire un utente con lo stesso nome!
			return Response({'errore': "Utente gia presente nel db!", 'more': str(err)})
		except:

			exc_type, exc_value, exc_traceback = sys.exc_info()

			print(sys.exc_info()[0])

			print( "***********")
			print( exc_value)
			print( type(exc_value))
			print( "**************")

			errStatus = {
				'errore' : 'Ci sono errori!',
				'valore' : str(exc_value),
				'data': str(request.data)
			}
			return Response(errStatus)
		

class PostList(generics.ListCreateAPIView):

	queryset = Post.objects.all()
	serializer_class = PostSerializer

class PostUser(views.APIView):

	def get(self, request, id):

		# Get a list of post from a single user
		# get_object_or_404

		try:
			post = Post.objects.all().filter(owner=id)

			length = len(list(post))
			postSerialized = PostSerializer(post, many=True)

			return Response(postSerialized.data)

		except:

			return Response({}, status=status.HTTP_400_BAD_REQUEST)

	def post(self, request):

		# Creiamo un nuovo post se esiste un utente loggato
		#return Response({}, status=status.HTTP_200_OK)
		return Response({'user': request.user}, status=status.HTTP_200_OK)

class NewPost(views.APIView):

	def post(self, request):

		if request.user.is_authenticated():

			# L'utente e attivo, dunque posso creare il task

			title = request.data.get('title', None)
			content = request.data.get('content', None)

			print( title)
			print( content)

			if title and content:

				newPost = Post.objects.create(owner=request.user, title = title, content = content)
				newPostSerial = PostSerializer(newPost)
				return Response({'new_post': newPostSerial.data}, status=status.HTTP_201_CREATED)

			else:

				return Response({'status': 'Bad Request', 'message': 'Title or Content missing'}, status=status.HTTP_400_BAD_REQUEST)

		else:

			return Response({'status': "Non autorizzato", 'message' : 'Utente non registrato non puo inserire post!'}, status=status.HTTP_401_UNAUTHORIZED)

class OwnerList(views.APIView): 

	def get(self, request):

		ownerSerial = OwnerSerializer(Owner.objects.all(), many=True)

		return Response({'owners':ownerSerial.data}, status=status.HTTP_200_OK)

class CarsList(views.APIView):

	def get(self, request):

		carsSerial = CarSerializer(Car.objects.all(), many=True)

		return Response({'cars':carsSerial.data}, status=status.HTTP_200_OK)
class CarDetail(generics.RetrieveUpdateDestroyAPIView):

	queryset = Car.objects.all()
	serializer_class = CarSerializer


def upload(request):

	if request.method == 'POST':

		image = request.data.get('image', None)
		prova = request.data.get('prova', None)

		print(image)
		print(prova)

		return Response({'prova': prova, 'status': 'OK'}, status=status.HTTP_201_CREATED)



