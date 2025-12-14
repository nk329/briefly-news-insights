"""
RDS 연결 및 기본 기능 테스트 스크립트
"""
import sys
import os
import requests
import json

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

API_BASE_URL = "http://localhost:8000"

def test_signup():
    """회원가입 테스트"""
    print("\n[테스트 1] 회원가입")
    print("-" * 50)
    
    test_user = {
        "email": f"test_{os.urandom(4).hex()}@example.com",
        "username": f"testuser_{os.urandom(4).hex()}",
        "password": "test1234"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/auth/signup",
            json=test_user
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 회원가입 성공!")
            print(f"   사용자명: {data.get('user', {}).get('username')}")
            print(f"   이메일: {data.get('user', {}).get('email')}")
            return data.get('access_token'), test_user
        else:
            print(f"❌ 회원가입 실패: {response.status_code}")
            print(f"   응답: {response.text}")
            return None, None
    except Exception as e:
        print(f"❌ 오류: {e}")
        return None, None

def test_login(username, password):
    """로그인 테스트"""
    print("\n[테스트 2] 로그인")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/auth/login",
            data={
                "username": username,
                "password": password
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 로그인 성공!")
            print(f"   토큰: {data.get('access_token', '')[:50]}...")
            return data.get('access_token')
        else:
            print(f"❌ 로그인 실패: {response.status_code}")
            print(f"   응답: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 오류: {e}")
        return None

def test_get_current_user(token):
    """현재 사용자 정보 조회 테스트"""
    print("\n[테스트 3] 현재 사용자 정보 조회")
    print("-" * 50)
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 사용자 정보 조회 성공!")
            print(f"   ID: {data.get('id')}")
            print(f"   사용자명: {data.get('username')}")
            print(f"   이메일: {data.get('email')}")
            return True
        else:
            print(f"❌ 사용자 정보 조회 실패: {response.status_code}")
            print(f"   응답: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def test_search_history(token):
    """검색 히스토리 테스트"""
    print("\n[테스트 4] 검색 히스토리 조회")
    print("-" * 50)
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/history/",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 검색 히스토리 조회 성공!")
            print(f"   히스토리 개수: {len(data)}")
            return True
        else:
            print(f"❌ 검색 히스토리 조회 실패: {response.status_code}")
            print(f"   응답: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def main():
    """메인 함수"""
    print("=" * 50)
    print("RDS 연결 및 기능 테스트")
    print("=" * 50)
    print("\n⚠️  백엔드 서버가 실행 중이어야 합니다!")
    print("   (uvicorn main:app --reload --port 8000)")
    print("")
    
    input("엔터를 눌러 테스트를 시작하세요...")
    
    # 테스트 1: 회원가입
    token, user_data = test_signup()
    if not token:
        print("\n❌ 회원가입 실패로 인해 테스트를 중단합니다.")
        return
    
    # 테스트 2: 로그인
    login_token = test_login(user_data['username'], user_data['password'])
    if not login_token:
        print("\n❌ 로그인 실패로 인해 테스트를 중단합니다.")
        return
    
    # 테스트 3: 사용자 정보 조회
    if not test_get_current_user(login_token):
        print("\n⚠️  사용자 정보 조회 실패")
    
    # 테스트 4: 검색 히스토리 조회
    if not test_search_history(login_token):
        print("\n⚠️  검색 히스토리 조회 실패")
    
    print("\n" + "=" * 50)
    print("✅ 모든 테스트 완료!")
    print("=" * 50)

if __name__ == "__main__":
    main()

