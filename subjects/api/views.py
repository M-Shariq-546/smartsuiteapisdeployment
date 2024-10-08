from rest_framework.viewsets import ModelViewSet
from ..models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework import status
from history.models import History
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from .serializers import *
from .gpts import *
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
        return Subjects.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# This is Subject Detail Api view
class SubjectDetailAPIView(RetrieveAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [ViewRightsPermission]
    queryset = Subjects.objects.all()
    lookup_field = 'id'

# This is Subject Delete Api view
class SubjectDeleteAPIView(DestroyAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsSuperAdmin]
    queryset = Subjects.objects.all()
    lookup_field = 'id'


class SubjectsOfTeacher(APIView):
    serializer_class = SubjectsOfTeacherSerializer
    permission_classes = [IsAuthenticated]
    queryset = Subjects.objects.all()


    def get(self, request,  *args, **kwargs):
        teacher = self.request.query_params.get('teacher')
        serializer = self.serializer_class(Subjects.objects.filter(teacher=teacher), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# This Api view works as assigning teacher to subjects and subjects update api view
class AssignTeacherToSubject(APIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsSuperAdmin]

    def patch(self, request, id,*args,**kwargs):
        instance = get_object_or_404(Subjects, pk=id)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Subject Updated Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return Response(response, status=status.HTTP_201_CREATED)


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
        return Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        instance.is_active = False
        instance.save()
        self.log_history(request, 'DELETE', instance)
        return Response({"Deleted":f"This File {instance_id} has been deleted successfully"}, status=status.HTTP_200_OK)


# Summary Keypoints and Quizes Sections is going from below

class CreateSummaryApiView(APIView):
    permission_classes = []

    def log_history(self, request, action, instance, changes=None):
        History.objects.create(
            user = request.user,
            action = action,
            model_name = instance.__class__.__name__,
            instance_id = instance.id,
            changes = changes,
        )

    def get(self , request, *args , **kwargs):
        file = self.request.query_params.get('file')

        if file is None:
            return Response({"File id is required"}, status=status.HTTP_400_BAD_REQUEST)

        summary = DocumentSummary.objects.filter(document__id=file).first()
        if summary is None:
            return Response({"error": "No summary found for this file"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role in ['Super Admin' , 'Student']:
            return Response({"summary_id":summary.id, "summary":summary.summary}, status=status.HTTP_200_OK)
        return Response({"summary_id":summary.id, "summary":summary.summary, "prompt":summary.prompt}, status=status.HTTP_200_OK)




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
                file = PDFFiles.objects.get(id=document, is_active=True)
            except:
                return Response({"Not Found":"No Associated File Found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                content = read_file_content(file.file)
            except:
                content = read_file_content(file.file.url)
            else:
                content = read_file_content(file.file.path)


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
            self.log_history(request, "CREATE", created_summary, f"Summary Created")
            return Response({"id": created_summary.id, "summary": f"{created_summary.summary}",
                                 "prompt": f"{created_summary.prompt}"}, status=status.HTTP_200_OK)
        return Response({"Access Denied": "You Are not Allowed to create summary"},
                            status=status.HTTP_401_UNAUTHORIZED)

class FileUpdteApiView(APIView):
    serializer_class = PDFSerializers
    permission_classes = [IsTeacherforFile]

    def get(self,request, id , *args , **kwargs):
        instance = get_object_or_404(PDFFiles, id=id)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, id, *args, **kwargs):
        instance = get_object_or_404(PDFFiles, id=id)
        data = request.data.copy()
        data.update(request.FILES)

        serializer = self.serializer_class(instance, data=data, partial=True)  # Use partial=True for patch
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # Save the instance
            return Response({"message": "File updated Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request, id , *args , **kwargs):
        instance = get_object_or_404(PDFFiles, id=id)
        instance.is_active=False
        instance.save()
        return Response({"message":"File Deleted Successfully"}, status=status.HTTP_200_OK)



# kEYPOINTS APIVIEW
class CreateKeypointApiView(APIView):
    permission_classes = []

    def log_history(self, request, action, instance, changes=None):
        History.objects.create(
            user = request.user,
            action = action,
            model_name = instance.__class__.__name__,
            instance_id = instance.id,
            changes = changes,
        )


    def get(self , request, *args , **kwargs):
        file = self.request.query_params.get('file')

        if file is None:
            return Response({"File id is required"}, status=status.HTTP_400_BAD_REQUEST)

        summary = DocumentKeypoint.objects.filter(document__id=file).first()
        if summary is None:
            return Response({"error": "No Keypoints found for this file"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role in ['Super Admin' , 'Student']:
            return Response({"keypoints_id":summary.id, "keypoints":summary.keypoint}, status=status.HTTP_200_OK)
        return Response({"keypoints_id":summary.id, "keypoints":summary.keypoint, "prompt":summary.prompt}, status=status.HTTP_200_OK)


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

            print(document)

            try:
                file = PDFFiles.objects.get(id=document, is_active=True)
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
            self.log_history(request, "CREATE", created_keypoint, f"Keypoints Created")
            return Response({"id": created_keypoint.id, "summary": f"{created_keypoint.keypoint}",
                                 "prompt": f"{created_keypoint.prompt}"}, status=status.HTTP_200_OK)
        return Response({"Access Denied": "You Are not Allowed to create summary"},
                            status=status.HTTP_401_UNAUTHORIZED)


class CreateQuizessApiView(APIView):
    serializer_class = CreateQuizesSerializer
    authentication_classes = [JWTAuthentication]
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

    def get(self, request):
        document_id = request.query_params.get('file')
        if not document_id:
            return Response({"error": "document_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            document = PDFFiles.objects.get(id=document_id, is_active=True)
        except PDFFiles.DoesNotExist:
            return Response({"error": "No Document Found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user.role == "Super Admin":
            quizzes = DocumentQuiz.objects.filter(document__id=document.id)
        elif user.role == "Teacher":
            quizzes = DocumentQuiz.objects.filter(document__id=document.id)
        else:
            quizzes = DocumentQuiz.objects.filter(document__id=document.id, upload=True)

        if request.user.role == 'Student':
            response_data = []
            for quiz in quizzes:
                # Check if the user has already attempted the quiz
                try:
                    quiz_result = QuizResult.objects.get(user=request.user, quiz=quiz)
                    quiz_data = {
                        "id": quiz.id,
                        "name": quiz.name,
                        "upload_status": quiz.upload,
                        "attempt_status": "Attempted",
                        "percentage": f"{quiz_result.score}%",
                        "result_status": quiz_result.status,
                        "obtained_marks":quiz_result.obtained,
                        "total_marks":quiz_result.total
                    }
                except QuizResult.DoesNotExist:
                    quiz_data = {
                        "id": quiz.id,
                        "name": quiz.name,
                        "upload_status": quiz.upload,
                        "attempt_status": "Yet to attempt",
                    }
                response_data.append(quiz_data)

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = []
            for quiz in quizzes:
                # Check if the user has already attempted the quiz
                quiz_data = {
                    "id": quiz.id,
                    "name": quiz.name,
                    "upload_status": quiz.upload,
                }
                response_data.append(quiz_data)
            return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.role == "Teacher":
            document_id = request.data.get('file')
            if not document_id:
                return Response({"error": "file is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                document = PDFFiles.objects.get(id=document_id, is_active=True)
            except PDFFiles.DoesNotExist:
                return Response({"error": "No Document Found"}, status=status.HTTP_404_NOT_FOUND)

            user = request.user

            if user.role == "Student":
                return Response({"Error":" You are Not Allowed for this request"})
            elif user.role == 'Super Admin':
                return Response({"Error":" You are Not Allowed for this request"})
            else:
                pass

            if not document.file:
                return Response({"Not Found": "No File is associated"}, status=status.HTTP_400_BAD_REQUEST)

            quiz_count = DocumentQuiz.objects.filter(document=document, added_by=user).count()
            if quiz_count >= 5:
                return Response(
                    {"error": "Quiz creation limit reached. No more than 5 quizzes allowed for this document."},
                    status=status.HTTP_400_BAD_REQUEST)


            content = read_file_content(document.file)

            if content is None:
                return Response({"error": "Unable to decode file content"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not content.strip():
                logger.error("Decoded content is empty")
                return Response({"error": "Decoded content is empty"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info(f"Decoded content: {content[:100]}")  # Log the first 100 characters of the content

            try:
                quiz, _ = generate_quizes_from_gpt(content)
                quiz = quiz.replace('\x00', '')  # Remove null bytes
                if quiz is None:
                    return Response({"error": "Failed to generate quiz"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            created_quiz = DocumentQuiz.objects.create(
                name=f"Quiz # {quiz_count} of {document.name}",
                quiz=quiz,
                prompt=_,
                document=document,
                added_by=self.request.user
            )
            self.log_history(request, "CREATE", created_quiz, f"Quiz Created")
            possible_formats = ["Question:", "question:", "Question 1:", "q:"]
            questions_data = []
            temp_data = quiz
            for fmt in possible_formats:
                if fmt in temp_data:
                    parts = temp_data.split(fmt)
                    if len(parts) > 1:
                        questions_data.extend(parts[1:])
                        temp_data = parts[0]

            if len(questions_data) - 1 > 10:
                return Response({"error": "Each quiz can have a maximum of 10 questions."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Iterate through the questions and create QuizQuestions objects
            for question_data in questions_data[1:]:
                lines = question_data.strip().split("\n")

                # Extract question text
                question_text = lines[0].strip()

                # Extract options and correct answer
                options = {}
                correct_answer = None
                for line in lines[1:]:
                    parts = line.split(": ")
                    if len(parts) >= 2:  # Check if there are at least two elements
                        option = parts[0].strip()
                        text = parts[1].strip()
                        if parts[0].strip() == "Correct Answer":
                            correct_answer = parts[1].strip()
                            # print(correct_answer)
                        options[option] = text
                # Create QuizQuestions object
                quiz_question = QuizQuestions.objects.create(
                    question=question_text,
                    option_1=options.get("A"),
                    option_2=options.get("B"),
                    option_3=options.get("C"),
                    option_4=options.get("D"),
                    answer=correct_answer,
                    quiz=created_quiz,  # Assuming 'created_quiz' is the instance of DocumentQuiz created earlier
                    added_by=request.user
                    # Assuming 'request' is available in this context "prompt":f"{created_quiz.prompt}"
                )
            return Response({"id": created_quiz.id, "quiz": f"{created_quiz.quiz}"}, status=status.HTTP_200_OK)
        return Response({"Access Denied": "You Are not Allowed to create quiz"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, quiz_id):
        try:
            if request.user.role == 'Teacher':
                if not quiz_id:
                    return Response({"error": "quiz_id is required"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    quiz = DocumentQuiz.objects.get(id=quiz_id)
                except DocumentQuiz.DoesNotExist:
                    return Response({"error": "No Quiz Found"}, status=status.HTTP_404_NOT_FOUND)
                instance = quiz
                quiz.delete()
                logger.info(f"Quiz with id {instance.id} deleted successfully by {request.user.id}")
                self.log_history(request, "DELETE", instance)
                return Response({"message": "Quiz deleted successfully", "id": quiz_id},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"Access Denied": "You are not allowed to delete quizzes"},
                                status=status.HTTP_401_UNAUTHORIZED)
        except serializers.ValidationError as e:
            logger.error(f"Validation error: {e.detail}")
            return Response(e.detail, status=status.HTTP_403_FORBIDDEN)
        except PermissionDenied as e:
            logger.error(f"Permission denied: {str(e)}")
            return Response({"Access Denied": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}", exc_info=True)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UploadQuiz(APIView):
    serializer_class = CreateQuizesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTeacherforFile]
    queryset = DocumentQuiz.objects.all()

    def post(self, request):
        quiz_id = request.data.get('quiz_id')
        quiz = DocumentQuiz.objects.get(id=quiz_id)
        if quiz:
            quiz.upload = True
            quiz.save()
            return Response({"message": "Quiz is Successfully uploaded or updated", "id": quiz.id},
                            status=status.HTTP_202_ACCEPTED)
        return Response({"Not Found": "No quiz found"}, status=status.HTTP_404_NOT_FOUND)

class EditQuizes(APIView):
    serializer_class = QuizQuestionsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTeacherforFile]

    def put(self, request, question_id):
        return self.update_question(request, question_id, partial=False)

    def patch(self, request, question_id):
        return self.update_question(request, question_id, partial=True)

    def update_question(self, request, question_id, partial):
        question = get_object_or_404(QuizQuestions, id=question_id)
        user = request.user

        if user.role != "Teacher":
            return Response({"error": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)

        # Ensure that options is a list of dictionaries
        options = request.data.get('options')
        if options and isinstance(options, list) and len(options) == 1 and isinstance(options[0], dict):
            options_dict = options[0]
            question.option_1 = options_dict.get('A')
            question.option_2 = options_dict.get('B')
            question.option_3 = options_dict.get('C')
            question.option_4 = options_dict.get('D')
            del request.data['options']  # Remove options from request data to avoid conflict
        elif options:
            return Response({"error": "Invalid options format"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(question, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionsofQuiz(ListAPIView):
    serializer_class = QuizQuestionsListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def get_queryset(self):
        quiz_id = self.request.query_params.get('quiz_id')
        if not quiz_id:
            return QuizQuestions.objects.none()

        quiz = get_object_or_404(DocumentQuiz, id=quiz_id)
        questions = QuizQuestions.objects.filter(quiz=quiz)
        return questions

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmitQuizView(APIView):
    permission_classes = []

    def log_history(self, request, action, instance, changes=None):
        History.objects.create(
            user = request.user,
            action = action,
            model_name = instance.__class__.__name__,
            instance_id = instance.id,
            changes = changes,
        )

    def post(self, request):
        if request.user.role == "Teacher" or request.user.role == "Super Admin":
            return Response({"Access Denied": "You are not authorized for this request"},
                            status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role == "Student":
            quiz_id = request.data.get("quiz_id")
            document = DocumentQuiz.objects.filter(id=quiz_id).first()

            if not document:
                return Response({"Not Found": "Document Not Found"}, status=status.HTTP_404_NOT_FOUND)

            answers = request.data.get("answers", [])

            # Fetch the quiz questions for the provided quiz_id
            quiz_questions = QuizQuestions.objects.filter(quiz_id=quiz_id)

            if not quiz_questions.exists():
                return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

            # Validate the answers
            total_questions = len(quiz_questions)
            correct_answers = 0
            for answer_data in answers:
                question_id = answer_data.get("question_id")
                selected_option = answer_data.get("option")

                # Fetch the question from the database
                try:
                    question = quiz_questions.get(id=question_id)
                except QuizQuestions.DoesNotExist:
                    return Response({"error": f"Question with id {question_id} not found in the quiz"},
                                    status=status.HTTP_404_NOT_FOUND)

                # Check if the selected option is correct
                if question.answer == selected_option:
                    correct_answers += 1

            # Calculate the score
            score = (correct_answers / total_questions) * 100

            if score > 33:
                status_test = "Pass"
            else:
                status_test = "Fail"
            quiz_result, created = QuizResult.objects.update_or_create(
                user=request.user,
                quiz=document,
                defaults={'score': score, 'status': status_test, 'total':total_questions, 'obtained':correct_answers}
            )
            self.log_history(request, "UPDATE", quiz_result, f"Quiz Attempted")
            return Response({"message":"Successfully submitted","Score": score, "Status": status_test}, status=status.HTTP_200_OK)
        else:
            return Response({"Access Denied": "Unauthorized Access Requested"}, status=status.HTTP_401_UNAUTHORIZED)
