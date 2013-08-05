from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    (r'^version/$', 'WorldTripLoggerRest.api.views.version'),
    (r'^start/$', 'WorldTripLoggerRest.api.views.start'), 
    (r'^stop/$', 'WorldTripLoggerRest.api.views.stop'),
    (r'^status/$', 'WorldTripLoggerRest.api.views.status'),
    #(r'^config/photo/set/$', 'WorldTripLoggerRest.api.views.config_photo_set'),
    #(r'^config/video/set/$', 'WorldTripLoggerRest.api.views.config_video_set'),

)

