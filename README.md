# iikoDinnerTime
[![CircleCI](https://circleci.com/gh/zakhar-petukhov/iikoDinnerTime.svg?style=svg)](https://circleci.com/gh/zakhar-petukhov/iikoDinnerTime)
[![codecov](https://codecov.io/gh/zakhar-petukhov/iikoDinnerTime/branch/master/graph/badge.svg)](https://codecov.io/gh/zakhar-petukhov/iikoDinnerTime)

iikoDinnerTime is an extension [application](https://github.com/zakhar-petukhov/DinnerTime), but only with full integration of iiko.

The entire dinner application has been redesigned to work with iiko.

Changes:
1) composite dinners were removed from the database, additional dishes took their place (iiko contains all the dishes)
2) redesigned the concept of updating of dishes, categories of dishes
3) added logging with sentry
4) the tests were updated
5) company address fields have been added, now filled in from the beginning of the city to the apartment number
6) fixed in backup