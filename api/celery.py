import os
from celery import Celery
from celery.schedules import crontab

# 이 부분은 'celery' program 구동을 위한 Default Django settings module을 setting합니다.
# 이 줄은 필요하지 않지만 항상 설정 모듈을 셀러리 프로그램으로 전달하는 것을 방지합니다. 앱 인스턴스를 생성하기 전에 다음 작업을 수행해야 합니다.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "core.settings",
)

app = Celery("api")

# 여기서 문자열을 사용하면 작업자가 구성 개체를 하위 프로세스에 직렬화할 필요가 없습니다.
# 네임스페이스='CELERY'는 모든 셀러리 관련 구성 키에 'CELERY_' 접두사가 있어야 함을 의미합니다.
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)
app.conf.beat_schedule = {
    "get-resource-metrics-every-1-second": {
        "task": "api.tasks.get_resource_metrics",  # tasks.py 파일 경로에 맞게 수정
        "schedule": 1.0,  # 1초마다 실행
    },
}
# 등록된 django apps 내부의 모든 task 모듈을 찾습니다.

app.autodiscover_tasks()
