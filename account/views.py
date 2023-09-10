import random

from django.contrib.auth import logout
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from beeline import settings
from course.models import Course
from .models import User, MotivationLetter, UserCourse, TestResult, UserProgress, VideoLessonProgress
from .serializers import UserSerializer, MotivationLetterSerializer, TestResultSerializer, UserCourseSerializer, \
    UserProgressSerializer, VideoLessonProgressSerializer


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            user = serializer.instance

            verification_code = generate_verification_code()
            user.is_verified = False
            user.verification_code = verification_code
            user.save()

            UserProgress.objects.create(user_id=user.id)

            courses = Course.objects.all()[:4]
            for i in range(1, 5):
                UserCourse.objects.create(user=user, course=courses[i])

            send_mail(
                'Email Verification',
                f'Your verification code: {verification_code}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )

            response_data = {
                'user': serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerificationView(APIView):
    def post(self, request):
        verification_code = request.data.get('verification_code', None)

        if not verification_code:
            return Response({'error': 'Verification code is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(verification_code=verification_code)
        except User.DoesNotExist:
            return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.verification_code = None
        user.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response_data = {
            'message': 'Verification successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email', None)

        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        verification_code = generate_verification_code()
        user.verification_code = verification_code
        user.save()

        send_mail(
            'Email Verification',
            f'Your verification code: {verification_code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        return Response({'message': 'Verification code sent to your email'}, status=status.HTTP_200_OK)


def generate_verification_code():
    return str(random.randint(100000, 999999))


class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserProgressView(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]


class UserCourseView(viewsets.ModelViewSet):
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserCourse.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = UserCourse.objects.filter(user_id=user_id)
        return queryset


class VideoLessonProgressView(viewsets.ModelViewSet):
    serializer_class = VideoLessonProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = VideoLessonProgress.objects.all()
        user_course_id = self.request.query_params.get('user_course_id')
        if user_course_id:
            queryset = VideoLessonProgress.objects.filter(user_course=user_course_id)
        return queryset


class TestResultView(viewsets.ModelViewSet):
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TestResult.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = TestResult.objects.filter(user_id=user_id)
        return queryset


class MotivationLetterView(viewsets.ModelViewSet):
    serializer_class = MotivationLetterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = MotivationLetter.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = MotivationLetter.objects.filter(user_id=user_id)
        return queryset
