# RDS 연결 정보를 .env 파일에 업데이트하는 스크립트
# 사용법: .\scripts\update_rds_env.ps1

$envFile = ".env"

Write-Host "========================================="
Write-Host "RDS 연결 정보 업데이트"
Write-Host "========================================="
Write-Host ""

# RDS 정보 입력
$rdsEndpoint = Read-Host "RDS 엔드포인트를 입력하세요 (예: briefly-db.xxxxx.ap-northeast-2.rds.amazonaws.com)"
$rdsUsername = Read-Host "RDS 사용자명을 입력하세요 (예: admin)"
$rdsPassword = Read-Host "RDS 비밀번호를 입력하세요" -AsSecureString
$rdsPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($rdsPassword))
$rdsDatabase = Read-Host "데이터베이스명을 입력하세요 (예: briefly_db)"

# DATABASE_URL 생성
$databaseUrl = "mysql+pymysql://${rdsUsername}:${rdsPasswordPlain}@${rdsEndpoint}:3306/${rdsDatabase}"

Write-Host ""
Write-Host "생성된 DATABASE_URL:"
Write-Host "DATABASE_URL=$databaseUrl"
Write-Host ""

$confirm = Read-Host "위 정보가 맞나요? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "취소되었습니다."
    exit
}

# .env 파일 읽기
if (Test-Path $envFile) {
    $content = Get-Content $envFile
    
    # DATABASE_URL 라인 찾아서 교체
    $newContent = $content | ForEach-Object {
        if ($_ -match "^DATABASE_URL=") {
            "DATABASE_URL=$databaseUrl"
        } else {
            $_
        }
    }
    
    # 파일 쓰기
    $newContent | Set-Content $envFile -Encoding UTF8
    
    Write-Host ""
    Write-Host "✅ .env 파일이 업데이트되었습니다!"
    Write-Host ""
    Write-Host "다음 단계:"
    Write-Host "1. python scripts\migrate_db.py 실행하여 테이블 생성"
    Write-Host "2. uvicorn main:app --reload 실행하여 서버 시작"
    Write-Host "3. 회원가입/로그인 테스트"
} else {
    Write-Host "❌ .env 파일을 찾을 수 없습니다."
}

