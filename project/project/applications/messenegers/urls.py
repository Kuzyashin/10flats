from django.conf.urls import url

from messenegers.views import TelegramBotView, FacebookBotView, LineBotView

urlpatterns = [
    url(r'^telegram/(?P<bot_token>.+)/$', TelegramBotView.as_view()),
    url(r'^facebook/(?P<bot_token>.+)/$', FacebookBotView.as_view()),
    url(r'^line/(?P<bot_token>.+)/$', LineBotView.as_view()),
]