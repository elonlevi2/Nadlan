from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from ..models import Property, Photo, Contact, Tip
from .serializers import PropertySerializers, PhotoSerializers, ContactSerializers, TipSerializers, UserSerializers
import boto3
import os

# from django.conf import settings

access_key = os.environ.get('S3_ACCESS_KEY')
secret_key = os.environ.get('S3_SECRET_KEY')

s3_client = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)


@api_view(['POST'])
def signup(req):
    """
    Sign up a new user.

    Parameters:
    - req: The HTTP request object containing user data.

    Returns:
    - Response: The HTTP response object containing a success or error message.
    """
    # Function code
    try:
        username = req.data.get("username")
        password = req.data.get("password")
        email = req.data.get("email")
        firstname = req.data.get("firstname")
        lastname = req.data.get("lastname")

        user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname,
                                        last_name=lastname)
        token = Token.objects.create(user=user)
        return Response({"msg": f"hey you have {token}",
                         "status": "success",
                         "token": str(token)})
    except Exception as e:
        return Response(f"{e}")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def private(req):
    """
    Get user information for authenticated users.

    Parameters:
    - req: The HTTP request object.

    Returns:
    - Response: The HTTP response object containing the user information.
    """
    # Function code
    return Response({'msg': f"ok. user is: {req.user.username}", 'user': {req.user.username}, 'id': {req.user.id},
                     "superuser": req.user.is_superuser})


# @method_decorator(cache_page(60), name="dispatch")
class PropertyApi(APIView):
    """
    API view for managing properties.

    Methods:
    - get: Retrieve properties or a specific property.
    - post: Create a new property.
    - put: Update an existing property.
    - delete: Delete a property.

    Parameters:
    - req: The HTTP request object.
    - action: The action to perform (e.g., "get", "add", "edit", "delete").

    Returns:
    - Response: The HTTP response object.
    """

    # Class code
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    @classmethod
    def get(cls, req, action=None):
        if action == 'get':
            try:
                if "id" in req.query_params:
                    id = req.query_params.get("id")
                    property = Property.objects.get(id=id)
                    ps = PropertySerializers(property)
                    return Response(ps.data)
                else:
                    all_properties = Property.objects.all()
                    ps = PropertySerializers(all_properties, many=True)
                    return Response(ps.data)
            except Exception as e:
                return Response(f"{e}")
        elif action == 'home':
            try:
                property = Property.objects.order_by('-id')[:3]
                ps = PropertySerializers(property, many=True).data
                return Response(ps)

            except Exception as e:
                return Response(f"{e}")

        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /get ")

    @classmethod
    def post(cls, req, action=None):
        # if not req.user.is_authenticated:
        #     return Response("No permissions for this api")
        if action == "add":
            try:
                ps = PropertySerializers(data=req.data)
                if ps.is_valid():
                    ps.save()
                    cache.delete('properties')
                    return Response({"msg": "objects Created", "id": ps.data['id']})
                else:
                    return Response(f"{ps.errors}")
            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /add ")

    @classmethod
    def put(cls, req, action=None):
        if action == "edit":
            try:
                id = req.query_params.get("id")
                property_instance = Property.objects.get(id=id)
                ps = PropertySerializers(data=req.data, instance=property_instance)
                if ps.is_valid():
                    ps.save()
                    cache.delete('properties')
                    return Response({"msg": "objects updated", "id": ps.data['id']})
                else:
                    return Response(f"{ps.errors}")
            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /edit ")

    @classmethod
    def delete(cls, req, action=None):
        if action == "delete":
            try:
                id = req.query_params.get("id")
                property_instance = Property.objects.get(id=id)
                property_instance.delete()
                cache.delete('properties')
                return Response("objects deleted")

            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /delete ")


# @method_decorator(cache_page(60), name="dispatch")
class ContactApi(APIView):
    """
    API view for managing contacts.

    Methods:
    - get: Retrieve contacts or a specific contact.
    - post: Create a new contact.
    - put: Update an existing contact.
    - delete: Delete a contact.

    Parameters:
    - req: The HTTP request object.
    - action: The action to perform (e.g., "get", "add", "edit", "delete").

    Returns:
    - Response: The HTTP response object.
    """

    # Class code
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    @classmethod
    def get(cls, req, action=None):
        if action == 'get':
            try:
                if "id" in req.query_params:
                    id = req.query_params.get("id")
                    contact = Contact.objects.get(id=id)
                    cs = ContactSerializers(contact)
                    return Response(cs.data)
                else:
                    all_contacts = Contact.objects.all()
                    cs = ContactSerializers(all_contacts, many=True)
                    return Response(cs.data)
            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /get ")

    @classmethod
    def post(cls, req, action=None):
        # if not req.user.is_authenticated:
        #     return Response("No permissions for this api")
        if action == "add":
            try:
                cs = ContactSerializers(data=req.data)
                if cs.is_valid():
                    cs.save()
                    return Response("objects Created")
                else:
                    return Response(f"{cs.errors}")
            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /add ")

    @classmethod
    def put(cls, req, action=None):
        if action == "edit":
            try:
                id = req.query_params.get("id")
                contact_instance = Contact.objects.get(id=id)
                cs = ContactSerializers(data=req.data, instance=contact_instance)
                if cs.is_valid():
                    cs.save()
                    return Response("objects updated")
                else:
                    return Response(f"{cs.errors}")
            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /edit ")

    @classmethod
    def delete(cls, req, action=None):
        if action == "delete":
            try:
                id = req.query_params.get("id")
                contact_instance = Contact.objects.get(id=id)
                contact_instance.delete()
                return Response("objects deleted")

            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /delete ")


# @method_decorator(cache_page(60), name="dispatch")
class TipApi(APIView):
    """
    API view for managing tips.

    Methods:
    - get: Retrieve tips or a specific tip.
    - post: Create a new tip.
    - put: Update an existing tip.
    - delete: Delete a tip.

    Parameters:
    - req: The HTTP request object.
    - action: The action to perform (e.g., "get", "add", "edit", "delete").

    Returns:
    - Response: The HTTP response object.
    """

    # Class code
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    @classmethod
    def get(cls, req, action=None):
        if action == 'get':
            try:
                if "id" in req.query_params:
                    id = req.query_params.get("id")
                    tip = Tip.objects.get(id=id)
                    ts = TipSerializers(tip)
                    return Response(ts.data)
                else:
                    all_tips = Tip.objects.all()
                    ts = TipSerializers(all_tips, many=True)
                    return Response(ts.data)
            except Exception as e:
                return Response(f"{e}")
        elif action == 'pagination':
            page_size = int(req.GET.get("page_size", 10))
            page_num = int(req.GET.get("page_num", 0))

            start = page_num * page_size
            end = start + page_size

            tips = Tip.objects.filter()[start:end]

            ts = TipSerializers(tips, many=True).data

            res = {
                'data': ts,
                "next_page": 'n',
                "has_more": end <= Tip.objects.count()
            }
            return Response(res)
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /get ")

    @classmethod
    def post(cls, req, action=None):
        # if not req.user.is_authenticated:
        #     return Response("No permissions for this api")
        if action == "add":
            try:
                print(req.data)
                ts = TipSerializers(data=req.data)
                if ts.is_valid():
                    ts.save()
                    return Response({'msg': "objects Created", 'status': 'success'})
                else:
                    return Response(f"{ts.errors}")
            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /add ")

    @classmethod
    def put(cls, req, action=None):
        if action == "edit":
            try:
                id = req.query_params.get("id")
                tip_instance = Tip.objects.get(id=id)
                ts = TipSerializers(data=req.data, instance=tip_instance)
                if ts.is_valid():
                    ts.save()
                    return Response("objects updated")
                else:
                    return Response(f"{ts.errors}")
            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /edit ")

    @classmethod
    def delete(cls, req, action=None):
        if action == "delete":
            try:
                id = req.query_params.get("id")
                tip_instance = Tip.objects.get(id=id)
                tip_instance.delete()
                return Response("objects deleted")

            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /delete ")


# @method_decorator(cache_page(60), name="dispatch")
class PhotoApi(APIView):
    """
    API view for managing photos.

    Methods:
    - get: Retrieve photos for a specific property.
    - post: Upload a new photo for a property.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Response: The HTTP response object.
    """

    # Class code
    @classmethod
    def get(cls, request):
        id = int(request.GET.get("id"))
        images = Photo.objects.filter(property=id)
        ps = PhotoSerializers(images, many=True).data

        res = {
            'data': ps,
        }
        return Response(res)

    @classmethod
    def post(cls, request):
        id = int(request.GET.get("id"))
        for i in request.FILES:
            s3_client.upload_fileobj(request.FILES[i].file, Bucket="nadlans3", Key=f"properties/{i}")
            p = Property.objects.filter(id=id)
            Photo.objects.create(image=f'{i}', property=p[0])

        return Response("Photo uploaded!")


# @method_decorator(cache_page(60), name="dispatch")
class PropertyApiPagination(APIView):
    """
    API view for pagination and filtering properties.
    """

    @classmethod
    def post(cls, request, action):
        print("server")

        page_size = int(request.GET.get("page_size", 10))
        page_num = int(request.GET.get("page_num", 0))

        start = page_num * page_size
        end = start + page_size

        data = request.data["filter"]

        properties_list = Property.objects.filter(type=action)

        if data['rooms'] is not None:
            properties_list = properties_list.filter(rooms=data['rooms'])
        if data['city'] is not None:
            properties_list = properties_list.filter(location=data['city'])
        if data['balcony'] is not None:
            properties_list = properties_list.filter(balcony=data['balcony'])
        if data['price'] is not None:
            properties_list = properties_list.filter(price__lte=data['price'])

        properties_list_s = PropertySerializers(properties_list[start:end], many=True).data

        cache.set('properties', properties_list_s)

        res = {
            'data': properties_list_s,
            "has_more": end <= Property.objects.count()
        }

        return Response(res)


# @method_decorator(cache_page(60), name="dispatch")
class PropertyOfUserApiPagination(APIView):
    """
    API view for pagination and filtering properties of a specific user.

    Methods:
    - get: get method for filtering and paginating properties of a specific user.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - Response: The response containing the filtered and paginated properties.
    """

    # Class code

    @classmethod
    def get(cls, request):
        id = request.GET.get("id")
        page_size = int(request.GET.get("page_size", 10))
        page_num = int(request.GET.get("page_num", 0))

        start = page_num * page_size
        end = start + page_size

        properties = Property.objects.filter(type='sale', real_estate=id)[start:end]

        ps = PropertySerializers(properties, many=True).data
        res = {
            'data': ps,
            "next_page": 'n',
            "has_more": end <= Property.objects.count()
        }
        return Response(res)


# @method_decorator(cache_page(60), name="dispatch")
class TipsOfUser(APIView):
    """
    API view for pagination and filtering tips of a specific user.

    Methods:
    - get: get  method for filtering and paginating tips of a specific user.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - Response: The response containing the filtered and paginated tips.
    """

    # Class code

    @classmethod
    def get(cls, request):
        id = request.GET.get("id")
        page_size = int(request.GET.get("page_size", 10))
        page_num = int(request.GET.get("page_num", 0))

        start = page_num * page_size
        end = start + page_size

        tips = Tip.objects.filter(real_estate=id)[start:end]

        ts = TipSerializers(tips, many=True).data

        res = {
            'data': ts,
            "next_page": 'n',
            "has_more": end <= Tip.objects.count()
        }
        return Response(res)


# @method_decorator(cache_page(60), name="dispatch")
class UserApi(APIView):
    """
    API view for retrieving and updating user information.
    """

    @classmethod
    def get(cls, request, action):
        """
        Get method for retrieving user information.

        Parameters:
            request (HttpRequest): The HTTP request object.
            action (str): The action to perform.

        Returns:
            Response: The response containing the user information.
        """
        if action == 'user':
            id = request.GET.get("id")

            user = User.objects.filter(id=id)

            us = UserSerializers(user, many=True).data
            res = {
                'data': us,
            }
            return Response(res)

        elif action == "brokers":
            page_size = int(request.GET.get("page_size", 10))
            page_num = int(request.GET.get("page_num", 0))

            start = page_num * page_size
            end = start + page_size

            user = User.objects.filter()[start:end]

            us = UserSerializers(user, many=True).data
            res = {
                'data': us,
                "next_page": 'n',
                "has_more": end <= User.objects.count()
            }
            return Response(res)

        elif action == "all":
            user = User.objects.all()

            us = UserSerializers(user, many=True).data
            res = {
                'data': us,
                "next_page": 'n',
            }
            return Response(res)

    @classmethod
    def put(cls, request, action):
        """
        Put method for updating user information.

        Parameters:
            request (HttpRequest): The HTTP request object.
            action (str): The action to perform.

        Returns:
            Response: The response indicating the success of the update or an error message.
        """
        if action == "edit":
            try:
                id = request.query_params.get("id")
                user_instance = User.objects.get(id=id)
                us = UserSerializers(data=request.data, instance=user_instance)
                if us.is_valid():
                    us.save()
                    return Response("objects updated")
                else:
                    return Response(f"{us.errors}")
            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /edit ")

    @classmethod
    def delete(cls, request, action=None):
        """
        Delete method for deleting user information.

        Parameters:
            request (HttpRequest): The HTTP request object.
            action (str): The action to perform.

        Returns:
            Response: The response indicating the success of the delete or an error message.
        """
        if action == 'delete':
            try:
                id = request.query_params.get("id")
                user_instance = User.objects.get(id=id)
                user_instance.delete()
                return Response("objects deleted")

            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /delete ")


class DashboardApi(APIView):
    """
    This API provides the main dashboard page.
    """

    @classmethod
    def get(cls, request, action=None):
        """
        Handles GET requests.

        Parameters:
        - request: The request object.
        - action: The action to perform.

        Returns:
        - Response: The response containing the requested data or an error message.
        """

        if action == 'users':
            try:
                users = User.objects.count()
                return Response(int(users))
            except Exception as e:
                return Response(f"{e}")

        elif action == 'property_sale':
            try:
                property = Property.objects.filter(type='sale').count()
                return Response(property)
            except Exception as e:
                return Response(f"{e}")

        elif action == 'property_rent':
            try:
                property = Property.objects.filter(type='rent').count()
                return Response(property)
            except Exception as e:
                return Response(f"{e}")

        elif action == 'messages':
            try:
                contact = Contact.objects.count()
                return Response(contact)
            except Exception as e:
                return Response(f"{e}")
