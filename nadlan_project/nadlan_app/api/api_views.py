from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from ..models import Property, Photo, Contact, Tip
from .serializers import PropertySerializers, PhotoSerializers, ContactSerializers, TipSerializers, UserSerializers
from django.conf import settings

STATIC_PATH = str(settings.BASE_DIR) + r"//nadlan_app//static//"


@api_view(['POST'])
def signup(req):
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
    return Response({'msg': f"ok. user is: {req.user.username}", 'user': {req.user.username}, 'id': {req.user.id}})


class PropertyApi(APIView):
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
                    all_propertys = Property.objects.all()
                    ps = PropertySerializers(all_propertys, many=True)
                    return Response(ps.data)
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
                    return Response("objects updated")
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
                return Response("objects deleted")

            except Exception as e:
                return Response(f"{e}")
        else:
            return Response(f"cannot use '{action}' action with the current method. try to use with /delete ")

    # def dispatch(self, request, *args, **kwargs):
    #     pass


class ContactApi(APIView):
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

    # def dispatch(self, request, *args, **kwargs):
    #     pass


class TipApi(APIView):
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

    # def dispatch(self, request, *args, **kwargs):
    #     pass


class PhotoApi(APIView):
    @classmethod
    def get(cls, request):
        id = int(request.GET.get("id"))

        # start = page * page_size
        # end = page * page_size + 10

        # properties = Property.objects.filter(type='sale')[start:end]
        images = Photo.objects.filter(property=id)
        # properties = ()
        #
        # for i in range(len(images)):
        #     print(Property.objects.filter(id=images[i].property.id)[0])
        #     properties.append(Property.objects.filter(id=images[i].property.id)[0])
        # print(properties)

        ps = PhotoSerializers(images, many=True).data

        res = {
            'data': ps,
        }
        return Response(res)

    @classmethod
    def post(cls, request):
        id = int(request.GET.get("id"))

        for f in request.FILES.items():
            p = Property.objects.filter(id=id)
            Photo.objects.create(image=f[1], property=p[0])

        # with open(STATIC_PATH + new_photo_name, 'wb+') as f:
        #     for chunk in request.data.get("photo").chunks():
        #         f.write(chunk)

        return Response("Photo uploaded!")


class PropertyApiPagination(APIView):
    @classmethod
    def get(cls, request, action=None):
        if action == 'sale':
            page_size = int(request.GET.get("page_size", 10))
            page_num = int(request.GET.get("page_num", 0))

            start = page_num * page_size
            end = start + page_size

            properties = Property.objects.filter(type='sale')[start:end]

            ps = PropertySerializers(properties, many=True).data

            res = {
                'data': ps,
                "next_page": 'n',
                "has_more": end <= Property.objects.count()
            }
            return Response(res)

        elif action == 'filters':
            rooms = request.GET.get("rooms")
            city = request.GET.get("city")

            print(rooms, city)
            page_size = int(request.GET.get("page_size", 10))
            page_num = int(request.GET.get("page_num", 0))

            start = page_num * page_size
            end = start + page_size

            if city != "" and rooms != "":
                properties = Property.objects.filter(type='sale', rooms=rooms, location=city)[start:end]
            else:
                properties = Property.objects.filter(type='sale')[start:end]

            ps = PropertySerializers(properties, many=True).data
            res = {
                'data': ps,
                "next_page": 'n',
                "has_more": end <= Property.objects.count()
            }
            return Response(res)

        elif action == 'rent':
            page_size = int(request.GET.get("page_size", 1))
            page_num = int(request.GET.get("page_num", 0))

            start = page_num * page_size
            end = start + page_size

            properties = Property.objects.filter(type='rent')[start:end]

            ps = PropertySerializers(properties, many=True).data

            res = {
                'data': ps,
                "next_page": 'n',
                "has_more": end <= Property.objects.count()
            }
            return Response(res)


class PropertyOfUserApiPagination(APIView):
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


class TipsOfUser(APIView):
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


class UserApi(APIView):
    @classmethod
    def get(cls, request, action):
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

    @classmethod
    def put(cls, request, action):
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
