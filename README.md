
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

<img src="https://github.com/sakilanasrinsetu/coffee_shop/blob/main/erd.png " width =100% > 



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
