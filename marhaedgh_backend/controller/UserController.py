from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/v1/user",
)

@router.post("/sign-in")
async def loginUser():

    #apple 인증서버에 요청 보내기
    apple_user_identifier = " "

    user_service = UserService()
    response = user_service.loginToAppleService(apple_user_identifier)

    return response

@router.patch("")
async def modifyUserInfo():
    # dto 객체 만들기
    # dto 객체 = 서비스함수();
    # 서비스함수 = 레포지토리 함수 ()
    # 레포지토리함수 = DB에 사용자 정보 가져오기
    #
    tmp = 0
    return 0


@router.delete("")
async def deleteUserInfo():
    # dto 객체 만들기
    # dto 객체 = 서비스함수();
    # 서비스함수 = 레포지토리 함수 ()
    # 레포지토리함수 = DB에 사용자 정보 가져오기
    #
    tmp = 0
    return 0