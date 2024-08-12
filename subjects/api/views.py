from rest_framework.viewsets import ModelViewSet
from ..models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from history.models import History
from .serializers import *
# from .gpts import *
from .permissions import *
from rest_framework.permissions import IsAuthenticated

class SubjectsModelViewSet(ModelViewSet):
    serializer_class = SubjectSerializer
    queryset = Subjects.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSuperAdmin]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsSuperAdmin | IsTeacher | IsStudentForFiles]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    def get_queryset(self):
        semester = self.request.query_params.get('semester')
        if semester:
            return Subjects.objects.filter(semester__id=semester)
        return

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Subject Added In Course Successfully"}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        self.permission_denied(request)

    def destroy(self, request, *args, **kwargs):
        self.permission_denied(request)


class SubjectFilesModelViewSet(ModelViewSet):
    serializer_class = PDFSerializers
    permission_classes = [IsTeacherforFile | IsStudentForFiles]
    queryset = PDFFiles.objects.filter(is_active=True)

    def log_history(self, request, action, instance, changes=None):
        History.objects.create(
            user = request.user,
            action = action,
            model_name = instance.__class__.__name__,
            instance_id = instance.id,
            changes = changes,
        )

    def get_queryset(self):
        subject = self.request.query_params.get('subject')
        return PDFFiles.objects.filter(subject__id=subject, is_active=True)

    def create(self, request, *args , **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response, instance = serializer.save()
        self.log_history(request, 'CREATE', instance, f"File(s) added suucessfully")
        return Response({"message":"File(s) Added Successfully"}, status=status.HTTP_201_CREATED)


    def put(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return self.update(request, *args , **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs['partial']
        serializer = self.get_serializer(instance , data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        self.log_history(request, 'UPDATE', instance , f"File {instance.name} updated")
        return Response({"message":"File Updated Successfully"}, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        instance.is_active = False
        instance.save()
        self.log_history(request, 'DELETE', instance)
        return Response({"Deleted":f"This File {instance_id} has been deleted successfully"}, status=status.HTTP_200_OK)


'''
# Summary Keypoints and Quizes Sections is going from below
'''
class CreateSummaryApiView(APIView):
    def post(self, request):
        user = request.user

        gerenal_prompt =  f"You are the content creator , Provide me the descriptive, related and concise and everytime unique summary for:"

        if user.role == 'Teacher':
            document = request.data.get('file')
            user_prompt = request.data.get('prompt')

            if not document:
                return Response({"Error":"File id is must field"}, status=status.HTTP_400_BAD_REQUEST)


            summary_count = DocumentSummary.objects.filter(document__id=document).count()
            if summary_count >= 3:
                return Response({"Limit Exceeded":"Your Limits of Summary Generation for this Document has Exceeded"}, status=status.HTTP_510_NOT_EXTENDED)

            try:
                file = PDFFiles.objects.get(id=document)
            except:
                return Response({"Not Found":"No Associated File Found"}, status=status.HTTP_404_NOT_FOUND)

            content = read_file_content(file.file)

            if content is None:
                return Response({"error": "Unable to decode file content"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not content.strip():
                return Response({"error": "Decoded content is empty"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if user_prompt == "":
                prompt = gerenal_prompt
            else:
                prompt = user_prompt
            try:
                summary, _ = generate_summary_from_gpt(content, prompt)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            created_summary = DocumentSummary.objects.create(
                    summary=summary,
                    document=file,
                    prompt=_,
                    added_by=self.request.user
            )

            return Response({"id": created_summary.id, "summary": f"{created_summary.summary}",
                                 "prompt": f"{created_summary.prompt}"}, status=status.HTTP_200_OK)
        return Response({"Access Denied": "You Are not Allowed to create summary"},
                            status=status.HTTP_401_UNAUTHORIZED)


# kEYPOINTS APIVIEW
class CreateKeypointApiView(APIView):
    def post(self, request):
        user = request.user

        gerenal_prompt = f"You are the key-points generator , Provide me the keypoints in bollet-points without extra useless text, related to the and everytime provide me unique keypoints :"

        if user.role == 'Teacher':
            document = request.data.get('file')
            user_prompt = request.data.get('prompt')

            if not document:
                return Response({"Error":"File id is must field"}, status=status.HTTP_400_BAD_REQUEST)


            keypoint_count = DocumentKeypoint.objects.filter(document__id=document).count()
            if keypoint_count >= 3:
                return Response({"Limit Exceeded":"Your Limits of Keypoints Generation for this Document has Exceeded"}, status=status.HTTP_510_NOT_EXTENDED)

            try:
                file = PDFFiles.objects.get(id=document)
            except:
                return Response({"Not Found":"No Associated File Found"}, status=status.HTTP_404_NOT_FOUND)

            content = read_file_content(file.file)

            if content is None:
                return Response({"error": "Unable to decode file content"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not content.strip():
                return Response({"error": "Decoded content is empty"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if user_prompt == "":
                prompt = gerenal_prompt
            else:
                prompt = user_prompt
            try:
                keypoint, _ = generate_keypoints_from_gpt(content, prompt)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            created_keypoint = DocumentKeypoint.objects.create(
                    keypoint=keypoint,
                    document=file,
                    prompt=_,
                    added_by=self.request.user
            )

            return Response({"id": created_keypoint.id, "summary": f"{created_keypoint.keypoint}",
                                 "prompt": f"{created_keypoint.prompt}"}, status=status.HTTP_200_OK)
        return Response({"Access Denied": "You Are not Allowed to create summary"},
                            status=status.HTTP_401_UNAUTHORIZED)
<<<<<<< HEAD

'''
=======
'''
>>>>>>> abc853ee88a2d9bb94413ca15a90807c0f6bbf88
