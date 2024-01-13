from django.urls import path
from samsung import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.home),
    path("register",views.register),
    path("login",views.user_login),
    path("logout",views.user_logout),
    path("catfilter/<cv>",views.catfilter),
    path("range",views.range),
    path("detail/<pid>",views.product_detail),
    path("addtocart/<pid>",views.addtocart),
    path("cart",views.cart),
    path("remove/<cid>",views.removecart),
    path("updateqty/<qv><cid>",views.updateqty),
    path("about",views.aboutus),
    path("contact",views.contact),
    path('sort/<str:order>/', views.sort),
    path("placeorder",views.placeorder),
    path("makepayment",views.makepayment)
    
]





if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)