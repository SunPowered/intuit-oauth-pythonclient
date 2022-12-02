# Intuit OAuth Python Client

A Python package to manage OAuth2 authentication with Intuits API.

## Rationale

This package is a fork from the official Intuit OAuth [repository](https://github.com/intuit/oauth-pythonclient).

It was forked after 2 years of inactivity and lack of maintenance on the original project.  
I wanted to use it and was frustrated with how it was designed; it made it particularly costly on unit tests.  
PRs that would have fixed this were closed with no action or response by the maintainers.  

The lack of engagement from Intuit is telling and it's better to have an engaged community-driven fork, than a 
poorly maintained official project.

## Installation

`pip install intuit-oauth-client`

## Usage

See original [repository](https://github.com/intuit/oauth-pythonclient)

## Changes

Notable changes from the official repository are:

1.  Remove HTTP requests on AuthClient __init__ constructor
2.  Lazy load the discovery doc dictionary and all corresponding attributes that were being set on __init__
3.  Remove subclass on  `requests.Session`.  A separate session can be passed on __init__ or one is created
4.  Update project to `poetry` with a pyproject.toml file
5.  Improve unit tests fixtures.  Tests run much faster now issuing far fewer actual HTTP requests
6.  Responsive unpaid maintainer

## Contributions

Feel free to submit an issue or pull request, I promise to respond

## License

This library is provided under Apache 2.0 which is found [here](https://github.com/SunPowered/intuit-oauth-pythonclient/blob/master/LICENSE)


