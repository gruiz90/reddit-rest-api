from django.shortcuts import render
from rest_framework import viewsets
from .models import Subreddit
from .serializers import SubredditSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.exceptions import NotFound
import json

# Create your views here.2


class SubredditViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows subreddits to be viewed or edited.
    """
    queryset = Subreddit.objects.all().order_by('created_utc')
    serializer_class = SubredditSerializer

    def create(self):
        # subredditNameToGet = self.request.query_params.get('name')
        # if subredditNameToGet is not None:
        # 	subreddit = Subreddit.get
        # 	subreddit = Subreddit.get_or_create_by_name(subredditNameToGet)
        # 	if subreddit is None:
        # 		raise NotFound(detail="Error 404, subreddit not found", code=404)
        # 	return Response(201, SubredditSerializer(subreddit).data)
        # else:
        # 	pass
        pass


# class SubredditAPIView(APIView):
# 	"""
# 	View to list all users in the system.

# 	* Requires token authentication.
# 	* Only admin users are able to access this view.
# 	"""
# 	# authentication_classes = [authentication.TokenAuthentication]
# 	# permission_classes = [permissions.IsAdminUser]

# 	def get(self):
# 		"""
# 		Return a list of all users.
# 		"""
# 		subredditNameToGet = self.request.query_params.get('name')
# 		subreddit = Subreddit.get_by_name(subredditNameToGet)
# 		if subreddit is None:
# 			raise NotFound(detail="Error 404, subreddit not found", code=404)
# 		return Response(json.dumps(subreddit))
