.. :changelog:

History
-------

Unreleased (2026-03-01)
+++++++++++

Modernise the project for later versions of python, Django and Wagtail.
The aim is to support modern versions of Django and Wagtail and continue to use the existing tests to ensure compatibility.

* Django 4.2 | 5.1 | 5.2 | 6.0
* Wagtail 7.x
* Python >= 3.9, <= 3.14
* fixes the api url to be at the root of the domain
* remove dependency on model-admin, use Snippets and Wagtail's admin interface instead. Recreate the order management interface using wagtails ListView and a custom detail page.
* rename project apps and recreate migrations for database tables to use the \"longclaw\_\" prefix to avoid confusion with other apps.
* added more granular permissions for actions on orders (cancel, refund, fulfill).


TODO: These are parts of the project that need further work.

* currently it may not be possible to use the longclaw.contrib apps??
* update project template
* update tests
* update documentation

1.0.0
+++++++++++

  * Switched to supporting Python 3 only
  * Updated to support Wagtail & Django > 2 only
  * Reworked the products app to make customisation easier (#76 and #47)
  * Documentation moved to Gitbook
  * Bug fixes: #130, #154, #165

0.2.0 (2017-07)
++++++++++++++++++++++

* Added a template tag for easy 'Add To Basket' buttons
* Added a template tag for shipping rates
* Created a client side Javascript library for the REST API
* We built basic views for Checkout and Basket
* Added template tags to help simplify integration with payment backends
* Basic checkout template in the project_template
* Bug fixes around payment gateway integrations
* Created a standard address form
* Pushed test coverage past 80%

0.1.1 (2017-04-14)
+++++++++++++++++++

* 'rest-framework' corrected to 'rest_framework' (#57)
* Limit Django requirements to 1.8-1.10 (#58)

0.1 (2017-04-14)
+++++++++++++++++++

* Initial release.
