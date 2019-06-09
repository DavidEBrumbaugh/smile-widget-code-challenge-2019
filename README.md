# Challenge Completed

## Updates to models
* New model: ProductPrice has been added
* code is now unique for Product and GiftCard to assure that get_object_or_404 functions properly
* Help messages are updated to reflect new models

## General Updates
* Added DRF (Django Rest Framework) to the Dockerfile
* Added migrations for the model updates
* Added Models to admin
* Added ProductPrice records via admin
* Exported fixtures and replaced fixture file

## Functional Additions
* Added PriceView to handle logic:
  * **productCode
    * productCode is required: 404 on failure
    * productCode must match existing product: 404 on failure
    * if productCode is valid, product retrieved, **price is set
  * **date
    * date is requied: 404 on failure
    * date must be formatted 'YYYY-MM-DD': 406 on failure
    * if ProductPrice ojbects exist that match the product code, 
      and date is between start and end date (or after start date if no end date):
      override **price (if multiple prices exist, select lowest **price)
  * **giftCardCode
    * GiftCard retrieved for giftCardCode and date: Ignore failures
    * If GiftCard exists: 
          If amount is less than *price subtract **amount from **price 
          Else price is zero
  * Return Response with formatted price as dictionary
  
* Added api/get-price and associated view to urls.py

## Unit Testing
### Added API unit testing
1. Required parameters
2. Date Formatting
3. Normal 2018 prices
4. Normal 2019 prices
5. Black Friday prices
6. GiftCard prices
7. GiftCards on Black Friday

### To Test on Docker

From project directory
* `>>> sudo docker-compose up --build` (Starts and initiizes container)
* `>>> sudo docker ps` (Gets the container id)
* `>>> sudo docker exec -it <container id> /bin/bash`
* `$ cd smilewidgets/`
* `$ python manage.py test products`

### Tests Passed
All 7 tests passed when this branch was installed, and the above process was followed.




See the original requirements below.
---
# smile-widget-code-challenge

The Smile Widget Company currently sells two types of smile widgets: a Big Widget and a Small Widget.  We'd like to add more flexibility to our product pricing.

## Setup with Docker
1. Install Docker (https://docs.docker.com/install/)
2. Fork this repository.
3. `>>> docker-compose up --build`

## Setup without Docker
1. Install Python (>3.4)
2. Install postgres.  By default the Django app will connect to the database named 'postgres'.  See `settings.DATABASES`.
3. Fork this repository, then clone your repository locally.
4. Install requirements.
  * `>>> pip install -r requirements.txt`
5. Run migrations.
  * `>>> python manage.py migrate`
6. Load data from fixtures:
  * `>>> python manage.py loaddata 0001_fixtures.json`

### Technical Requirements
* We currently have two products with the following prices:
    * Big Widget - $1000
    * Small Widget - $99
* These products, along with existing gift cards are already setup in the database.  Study the existing models and initial data.
* Create a new ProductPrice model and setup the following price schedule:    
  * Black Friday Prices (November 23, 24, & 25)
    * Big Widget - $800
    * Small Widget - FREE!
  * 2019 Prices (starting January 1, 2019)
    * Big Widget - $1200
    * Small Widget - $125
* Build a JSON API endpoint that accepts a product code, date, and (optional) gift card and returns product price.
  * The endpoint should live at `api/get-price` and accept the following parameters:
    * `"productCode"`
    * `"date"`
    * `"giftCardCode"`
* Make all of your changes in a new feature branch and submit a pull request to _your own forked repo_.

### Additional Information
* Please use Django Rest Framework or a Python HTTP framework of your choice to create the endpoint.
* Just as a general guideline, we've designed this exercise to take less than 4 hours.
