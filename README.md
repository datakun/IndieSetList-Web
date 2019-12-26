# IndieSetList-Web
1. manager
- 공연 영상, 공연 정보, 음악가, 공연장을 쉽게 추가하기 위한 관리용 웹 페이지
- Python, Flask, Firebase(Cloud Firestore, Authentication), Bootstrap 이용
2. user
- [indieSetList App](https://play.google.com/store/apps/details?id=com.kimjunu.indiesetlist) 의 기능을 하는 웹 페이지
- [프로토 타입](http://kimjunu.com/first_version_complted) 은 MongoDB로 개발했으나, Firestore를 이용할 수 있도록 마이그레이션 필요
- 프로토 타입에 나온 공연 정보, 공연 영상 자동 수집 기능은 API 사용 횟수 제한되는 문제 때문에 수동으로 추가하기로 함(manager 웹페이지가 필요한 이유)
