from core.authentication import PrivateAPI
from rest_framework.response import Response
from rest_framework import status
from user_registration.models import UserWorkSpaceRelationTable
from .models import UserQuestions

# Create your views here.
from rest_framework.response import Response
from core.authentication import PublicAPI, PrivateAPI
from rest_framework import status
from user_registration.models import UserModel
from .models import Questions, QuestionsOptions, UserQuestions, QuizAnswer

class GetAllUsersWithQuiz(PrivateAPI):
    
    def get(self, request):      

        try:
            UserWorkSpaceRelationTable.objects.get(
                workspace__id = request.GET.get('workspace_id'), 
                user = request.user
            )
        except UserWorkSpaceRelationTable.DoesNotExist:
            return Response({
                "status": False,
                "message": "Invalid workspace"
            }, status=status.HTTP_400_BAD_REQUEST)

        workspace_users = [obj.user for obj in UserWorkSpaceRelationTable.objects.filter(
            workspace__id = request.GET.get('workspace_id')
        )]

        return Response([{
            'user_id': usr.user.id,
            'name':usr.user.name,
            'image_url':usr.user.image_url,
            'email': usr.user.email
        } for usr in UserQuestions.objects.filter(user__in=workspace_users)], status=status.HTTP_200_OK)

class QuestionView(PrivateAPI):

    def get(self, request):
        
        All_Question = Questions.objects.all()
        array_object = []
        
        for question in All_Question:
            data_object = {
                "question_id" : question.id,
                "question" : question.question
            }
            options_object = []
            for option in question.options.all():
                obj = {
                    "option_id" : option.id,
                    "option_text" : option.option_text
                }
                options_object.append(obj)
            
            data_object.update({"options":options_object})
            array_object.append(data_object)
        
        return Response({
            'status': True, 
            'email': request.user.username , 
            'questionare': array_object
        }, status=status.HTTP_200_OK)


    def post(self,request):

        data = request.data

        try:
            Question = Questions.objects.get(id=data.get('question_id'))
        except :
            return Response({
                "status": False,
                "message": "Question Not Found!",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            Option = QuestionsOptions.objects.get(id= data.get('option_id'),question=Question)
        except :
            return Response({
                "status": False,
                "message": "Option Not Found For The Provided Question!",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            created = UserQuestions.objects.create(question=Question,correct_answer=Option,user=request.user)
            if created:
                return Response({
                    "status": True,
                    "message": "Question Answered Successfully",
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "status": True,
                "message": e.__str__()
            }, status=status.HTTP_400_BAD_REQUEST)


class QuizAnswerAPIView(PrivateAPI):

    def get(self, request):
        All_Question = UserQuestions.objects.filter(user__email=request.GET.get('email'))
        array_object = []
        
        for question in All_Question:
            
            data_object = {
                "question_id": question.question.id, 
                "question": question.question.question, 
                "correct_answer_id": question.correct_answer.id,
                "already_answered": True if question.question.answers.filter(played_by=request.user) else False,
            }
            
            options_object = []
            for option in question.question.options.all():
                obj = {
                    "option_id": option.id,
                    "option_text": option.option_text
                }
                options_object.append(obj)
            
            data_object.update({
                "options":options_object
            })
            array_object.append(data_object)
        
        return Response({
            'status': True, 
            'questionare': array_object
        }, status=status.HTTP_200_OK)

    def post(self,request):

        data = request.data
        correct_answer = False
        try:
            Question = Questions.objects.get(id=data.get('question_id'))
        except :
            return Response({
                "status": False,
                "message": "Question Not Found!",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            Option = QuestionsOptions.objects.get(id= data.get('option_id'),question=Question)
        except :
            return Response({
                "status": False,
                "message": "Option Not Found For The Provided Question!",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_questions = UserQuestions.objects.get(question=Question,user=request.user)
            if user_questions:
                if user_questions.correct_answer == Option:
                    correct_answer = True
        except Exception as e:
            return Response({
                "status": True,
                "message": e.__str__()
            }, status=status.HTTP_400_BAD_REQUEST)


        try:
            user = UserModel.objects.get(email=data.get('answered_for'))
        except Exception as e:
            return Response({
                "status": True,
                "message": e.__str__()
            }, status=status.HTTP_400_BAD_REQUEST)

        answer_created = QuizAnswer.objects.create(
            answered_for = user,
            played_by = request.user,
            question = Question,
            option = Option,
            correct_answer = correct_answer
        )
        
        if answer_created:
            return Response({
                "status": True,
                "message": "Quiz Answered Successfully",
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "message": "Quiz Not Answered Successfully!",
        }, status=status.HTTP_400_BAD_REQUEST)

class LeaderBoard(PrivateAPI):

    def get(self,request):

        quiz_answers_object = QuizAnswer.objects.filter(answered_for=request.user)
        leader_board_array = []
        leader_board_object = {}
        for quiz_answer_object in quiz_answers_object:
            if quiz_answer_object.played_by.email not in leader_board_object.keys():
                leader_board_object[quiz_answer_object.played_by.email] = {"question_attempted_count": 1,
                                                                           "question_attempted_correct_count": 1 if quiz_answer_object.correct_answer else 0,
                                                                           "name":quiz_answer_object.answered_for.name,
                                                                           "image_url":quiz_answer_object.answered_for.image_url,
                                                                             }
            else:
                leader_board_object[quiz_answer_object.played_by.email]["question_attempted_count"] += 1
                leader_board_object[quiz_answer_object.played_by.email]["question_attempted_correct_count"] += 1 if quiz_answer_object.correct_answer else 0

            leader_board_array.append(leader_board_object)
        for leader_board_data in leader_board_array:
            leader_board_value = list(leader_board_data.values())[0]
            leader_board_value['success_percentage'] = leader_board_value['question_attempted_correct_count']/leader_board_value['question_attempted_count'] * 100

        if len(leader_board_array) > 0:
            return Response({
                "status": True,
                "message": leader_board_array,
            }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "message": "No Answers Found!",
        }, status=status.HTTP_400_BAD_REQUEST)