
# **`Coffee Shop**

## [Website]()

## [Swagger]()

## [Code Repo]()

## Backend Technologies

`Django:3.2.6` `django_rest_framework:3.13.1` `react-router-dom: 6.1.1` `drf-yasg2: 1.19.4` `drf-extra-fields: 3.2.1`
`Pillow:8.4.0` `python-decouple:3.5`



## Frontend Technologies
 `react: ^17.0.2` `react-bootstrap: ^2.0.3` `react-router-dom: 6.1.1` `react-icons: 4.3.1` `sass: 1.45.0`

```
# [ Coffee API][docs]

[![build-status-image]][build-status]
[![coverage-status-image]][codecov]
[![pypi-version]][pypi]

** Coffee APIs.**

Full documentation for the project is available at https://staging.Coffee.com/redoc/ 


---

---

# Backend API Overview

Backend Architecture: MVC (Model,View,Controller)

Some reasons you might want to use REST framework:


There is a live example API for testing purposes, [available here][sandbox].

**Below**: *Screenshot from the browsable API*

# ERD Diagram 

<img src="https://user-images.githubusercontent.com/72943748/193029465-52d50630-5485-4444-8e4f-119744156de9.png " width =100% > 


----

# Requirements

* asgiref 3.5.2
* certifi 2022.6.15
* cffi==1.15.1
* charset-normalizer==2.1.0
* coreapi==2.3.3
* coreschema==0.0.4
* cryptography==37.0.4
* defusedxml==0.7.1
* Django==3.2.6
* django-allauth==0.51.0
* django-cors-headers==3.13.0
* django-environ==0.9.0
* django-extensions==3.2.0
* django-widget-tweaks==1.4.12
* djangorestframework==3.13.1
* drf-yasg2==1.19.4
* idna==3.3
* inflection==0.5.1
* itypes==1.2.0
* Jinja2==3.1.2
* MarkupSafe==2.1.1
* oauthlib==3.2.0
* packaging==21.3
* psycopg2==2.9.3
* pycparser==2.21
* pygraphviz==1.10
* PyJWT==2.4.0
* pyparsing==3.0.9
* python-decouple==3.6
* python3-openid==3.2.0
* pytz==2022.1
* PyYAML==6.0
* requests==2.28.1
* requests-oauthlib==1.3.1
* ruamel.yaml==0.17.21
* ruamel.yaml.clib==0.2.6
* six==1.16.0
* sqlparse==0.4.2
* uritemplate==4.1.1
* urllib3==1.26.10

We **highly recommend** and only officially support the latest patch release of
each Python and Django series.



Add `'all third Patry APP and Packege '` to your `INSTALLED_APPS` setting.

```python

THIRD_PARTY_APPS=[
    
    
    'accounts',
    'coffee_shop',
    'dashboard',
    'cafe',
    'knox',
    'django_extensions',

    'django.contrib.sites',
    'django.contrib.postgres',
    # 'allauth',
    # 'allauth.account',

    'drf_yasg2',
    'rest_framework',

]

INSTALLED_APPS = [

] +THIRD_PARTY_APPS
```

# Example

Let's take a look at a quick example of using REST framework to build a simple model-backed API for accessing users and groups.

For Run the project requirment setup...
```python

   pip install -r requirements.txt
