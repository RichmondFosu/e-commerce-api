# TODO List for Landing Page Creation

- [x] Add landing_view function in demo/views.py to render 'demo/landing.html'
- [x] Add path('', landing_view, name='landing') to demo/urls.py urlpatterns
- [x] Change path('demo/', include('demo.urls')) to path('', include('demo.urls')) in products_api/urls.py
- [x] Create demo/templates/demo/landing.html template extending base.html with landing page content
- [x] Update TODO.md to mark the landing page task as complete
- [x] Run Django server and test the landing page at /
