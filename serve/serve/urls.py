from django.urls import path
from . import interface
from . import check
from . import test
 
urlpatterns = [
    path('api/test', interface.test),
    path('api/getMovieList', interface.get_movie_list),
    path('api/getMovieData', interface.get_movie_data),
    path('api/getAnalysisData', interface.get_analysis_data),

    path('api/checkEnvironment', check.check_environment),
    path('api/checkDataSet', check.check_dataset),
    path('api/checkModel', check.check_model),

    path('api/getVideoCut', test.get_video_cut),
    path('api/getVideoShowData', test.get_video_showData),
    path('api/getTextShowData', test.get_text_showData)
]