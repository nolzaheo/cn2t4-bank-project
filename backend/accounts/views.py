from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from users.models import User
from .models import Account

class CreateAccountView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        nickname = request.data.get("nickname", "")
        balance = request.data.get("balance", 0)

        # 유저 확인 (user_id 기반 조회)
        user = get_object_or_404(User, user_id=user_id)

        # 새로운 계좌 생성
        account = Account.objects.create(
            user=user,
            nickname=nickname,
            balance=balance,
            status="OPEN"
        )

        return Response({
            "account_id": str(account.account_id),
            "account_number": account.account_number,
            "user_id": str(user.user_id),  # id → user_id
            "nickname": account.nickname,
            "balance": account.balance,
            "status": account.status
        }, status=status.HTTP_201_CREATED)

class UserAccountsView(APIView):
    def get(self, request, userId):
        user = get_object_or_404(User, user_id=userId)
        accounts = Account.objects.filter(user=user)  # user_id 대신 user 사용

        account_data = [
            {
                "account_id": str(account.account_id),
                "nickname": account.nickname,
                "balance": account.balance
            }
            for account in accounts
        ]

        return Response(account_data, status=status.HTTP_200_OK)



class AccountDetailView(APIView):
    def get(self, request, account_id):
        account = get_object_or_404(Account, account_id=account_id)
        return Response({
            "account_id": str(account.account_id),
            "account_number": account.account_number,
            "user_id": str(account.user.user_id),
            "nickname": account.nickname,
            "balance": account.balance,
            "status": account.status,
            "created_at": account.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }, status=status.HTTP_200_OK)


class AccountUpdateView(APIView):
    def put(self, request, account_id):
        account = get_object_or_404(Account, account_id=account_id)

        account.nickname = request.data.get("nickname", account.nickname)
        account.balance = request.data.get("balance", account.balance)
        account.status = request.data.get("status", account.status)

        account.save()
        return Response({"message": "Account updated successfully"}, status=status.HTTP_200_OK)


class AccountDeleteView(APIView):
    def delete(self, request, account_id):
        account = get_object_or_404(Account, account_id=account_id)

        if account.status == "CLOSED":
            return Response({"error": "Account already closed"}, status=status.HTTP_400_BAD_REQUEST)

        account.status = "CLOSED"
        account.save()
        return Response({"message": "Account closed successfully"}, status=status.HTTP_200_OK)