from rest_framework import serializers 
from autenticazione.models import PSUser, Post, Car, Owner, Foto

from rest_framework.exceptions import ValidationError

import time, datetime

class PSUserSerializer(serializers.ModelSerializer):

	password = serializers.CharField(max_length=40, write_only=True, required=False)
	confirm_password = serializers.CharField(max_length=40, write_only=True, required=False)
	
	class Meta:
		# Questa classe prende un modello e serializza solo gli elementi 
		# che noi vogliamo serializzare

		model = PSUser
		fields = ('id', 'email', 'password','confirm_password', 'nickname', 'nome','cognome', 'created_at', 'updated_at')
		
		# Chiamata quando dobbiamo creare un nuovo oggetto
		def create(self, **validated_data):
		 	# Dal momento che abbiamo richiesto la confirm password, 
		 	# dobbiamo creare manualmente l'utente

		 	email = validated_data['email']
		 	nickname = validated_data['nickname']
		 	nome = validated_data['nome']
		 	cognome = validated_data['cognome']

		 	password = validated_data['password']
		 	confirm_password = validated_data['confirm_password']

		 	if password and confirm_password and password == confirm_password:
		 		new_account = PSUser.objects.create_user(email=email, nickname=nickname, nome=nome,cognome=cognome)
				new_account.set_password(password)
				new_account.save()
				return new_account
			
			return None

		# Chiamata su oggetti gia esistenti nel DB
		def update(self, instance, validated_data):

			instance.nickname = validated_data.get('nickname', instance.nickname)


			password = validated_data.get('password', None)
			confirm_password = validated_data.get('confirm_password', None)

			instance.save()

			if password and confirm_password and password == confirm_password:
				instance.set_password(password)

			# Update the session in order to auth the user with the new password
			update_session_auth_hash(self.context.get('request'), instance)

			return instance

		def save(self):

			# Override della funzione save 
			# chiamo correttamente il create
			print("Dentro save di serializer User")
			return self.create(**validated_data)


class PostSerializer(serializers.ModelSerializer):

	# source indica quale campo della chiave esterna e usato come campo nella serializzazione
	#owner = serializers.ReadOnlyField(source='owner')

	class Meta:

		model = Post
		fields = ('id', 'owner', 'content', 'title')

class CarSerializer(serializers.ModelSerializer):

	class Meta:

		model = Car
		fields = ('id', 'owner', 'name', 'marchio')

class OwnerSerializer(serializers.BaseSerializer):

		def to_representation(self, owner):

			# Owner rappresenta l'oggetto che stiamo andando 
			# a serializzare

			carsOwnedSerial = CarSerializer(Car.objects.all().filter(owner__id=owner.id), many=True)


			return {
				'name' : owner.name,
				'surname' : owner.surname,
				'cars': carsOwnedSerial.data
			}

		def to_internal_value(self, data):

			# Questa funzione viene chiamata quando cerchiamo di creare o aggiornare 
			# dei dati provenienti dall'API endpoint

			# Ritorna:

			# SUCCESS: il dict contenente i dati corretti
			# ERROR: un ValidationError contentente un dict con nome_field: errore_field

			name = data.get('name')
			surname = data.get('surname')

			if not name:
				raise ValidationError({
					'name' : 'Questo campo (name) non puo essere vuoto!'
					})
			if not surname: 
				raise ValidationError({
					'surname': 'Questo campo (surname) non puo essere vuoto'
					})

			return {
				'name' : name,
				'surname' : surname
			}

		def create(self, validated_data):

			# Qui validated_data viene da to_internal_data

			# La funzione create del manager di default richiede solamente
			# un argomento, che e un dict (**)

			return Owner.objects.create(**validated_data)

class FotoSerializer(serializers.BaseSerializer):

	def to_representation(self, obj):

		return dict(obj)


	def to_internal_value(self, data):

		image_path = data.image
		compass = data.compass
		latitude = data.latitude
		longitude = data.longitude
		foto_id = data.id
		created_at = int(time.mktime(data.created_at.timetuple())*1000)

		if not image_path:
			raise ValidationError({
					'image': 'Questo campo non puo essere vuoto'
				})
		if not compass:
			raise ValidationError({
					'compass': 'Questo campo non puo essere vuoto'
				})
		if not latitude:
			raise ValidationError({
					'latitude': 'Questo campo non puo essere vuoto'
				})
		if not longitude:
			raise ValidationError({
					'longitude': 'Questo campo non puo essere vuoto'
				})

		return {
			'image': image_path,
			'compass': compass,
			'latitude' : latitude,
			'longitude': longitude,
			'id': foto_id,
			'created_at': created_at
		}

	def create(self, validated_data):

		# Funzione chiamata quando viene creato un oggetto 
		# a partire dai dati ValidationError

		# Togliamo l'id o potrebbe dare errori!
		del validated_data['id']
		del validated_data['created_at']

		return Foto.objects.create(**validated_data)
