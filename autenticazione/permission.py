from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):

		print(permissions.SAFE_METHODS)
		# I metodi sicuri sono accessibili a tutti
		if request.method in permissions.SAFE_METHODS:
			return True

		# Se l'utente che accede e il proprietario della risorsa
		# allora la puo modificare
		return obj.owner == request.user