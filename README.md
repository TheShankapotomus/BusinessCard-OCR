# Business Card OCR

___

### Table of Contents

1. [Preface](#preface) 
2. [Quickstart](#quickstart)
3. [Engineering and Design](#design)

___
## Preface <a name="preface"></a>

This project was designed in [Python](https://www.python.org/), version 3.6, and the application
can either be run standalone in a terminal or within a [Docker](https://www.docker.com/)  container. The reason
behind adding a container option is installing _Python 3.6_ could be cumbersome to a tester and with the growth 
of _containerization_ it is a viable avenue for the presentation and execution of this project.

#### Tool Stack <a name="tool-stack"></a>

The project uses:

- [Python 3.6](https://www.python.org/downloads/release/python-363/) - Python Interpreter
    - [PyYAML](https://pypi.python.org/pypi/PyYAML) - a Python YAML parser (used solely for testing) 

- [Docker](https://www.docker.com/) - Container Utility
    - [CentOS 7](https://hub.docker.com/_/centos/) - Base Container Image
    - [dumb-init](https://github.com/Yelp/dumb-init) - Container initialization system
    - Python 3.6 and dependencies (above)

#### Platform Compliance
The project has been tested on:

- Mac OS X
- CentOS 7 (containerized)

#### Application Help

```bash
usage: __main__.py [-h] [-d DOCUMENT] [--test]

Simple Business Card OCR

optional arguments:
  -h, --help            show this help message and exit
  -d DOCUMENT, --document DOCUMENT
                        pass the document string to be parsed
  --test                run test cases
```

___

## Quickstart <a name="quickstart"></a>

For ease of use and so that one does not have to directly modify their development environment to test/run this
application, a Dockerfile was implemented. All commands should be executed in a Bash terminal while in the root
directory of the _BusinessCard-OCR_ project. The required dev tools can be located in the [Tool Stack](#tool-stack) 
(under [Preface](#preface)).

#### Docker Usage

_Requires:_ Docker

```bash
# Build docker image
docker build -t ocr .

# Run test suite
docker run ocr

# Run sample document string
docker run ocr --document $'ASYMMETRIK LTD\nMike Smith\nSenior Software Engineer\n(410)555-1234\nmsmith@asymmetrik.com'

# Access help menu
docker run ocr -h
```

#### Terminal Usage

_Requires:_ Python 3.6, pip3.6 (default with Python)

```bash
# Install PyPI dependencies
pip3.6 install -r requirements.txt

# Run test suite
python3.6 -m ocr --test

# Run sample document string
python3.6 -m ocr --document $'ASYMMETRIK LTD\nMike Smith\nSenior Software Engineer\n(410)555-1234\nmsmith@asymmetrik.com'

# Access help menu
python3.6 -m ocr -h
```

#### Notes:

- The above _--document_ flag examples use an ANSI-C quoted string with the first example input provided at the 
[challenges site](https://www.asymmetrik.com/programming-challenges/); this string type is needed
so that the escaped characters can be parsed properly. 

- Executing a _docker run_ without specifiying the _--name_ flag will give the container an auto-generated name

- Using the _docker run_ commands with _-d_, prior to the image name, quiets the output which can be viewed
  later with _docker logs_

___

## Engineering and Design <a name="design"></a>

This section will review the design choices made, road blocks hit, and solutions developed when working on this project.

#### Code Implementation

For the actual implementation of the OCR, a single Python module (_ocr/parser.py_) worked well; having 
both the _BusinessCardParser_ and _\_ContactInfo_ classes in one file lead to easier comprehension of the implementation. 
Compliance with [PEP8](https://www.python.org/dev/peps/pep-0008/) was key throughout the project. 

- Class: _BusinessCardParser_
    - Has a one "public" accessor method: _get_contact_info_()
    - Returns a _\_ContactInfo_ object from the _get_contact_info_() method
    - _\_filter_fields_() method uses the _\_ContactInfo_._\_\_slots__\_ attributes as a search reference
    - _\_filter_fields_() method returns a dictionary purpose built to populate a _\_ContactInfo_ object
    - The fields _email_ and _phone_ are parsed independently, while the _name_ field requires a populated email field
    
- Class: _\_ContactInfo_
    - Has three "public" accessor methods: _get_name_(), _get_phone_number_(), and _get_email_address_() 
    - Uses the _\_\_slots___ attribute to minimize memory profile
    - _kwargs**_ is explicitly used to populate object on initialization
    - All variable attributes are name mangled so that cannot be accessed directly
    - Getters all call _str()_ on their respective attributes, adding redundancy if their attribute object 
    ever changes from _str_ type
 
#### Parsing Algorithm

The initial checks were quick to implement for both email and phone, however the name parsing was more of a challenge.
The implementions discussed below can be found in the method _\_filter_fields_() under the class 
_BusinessCardParser_.

##### Initial Assumptions

Based on the example data sets, it was determined that there are likely to be minimal, if any, oddities in the data sets
due to the professional nature of the medium (business cards); the data sets are also assumed to be well formed. 

##### Email Address

Simple research into email parsing led to the site [emailregex.com](http://emailregex.com/) which had the exact regex 
string to be used in Python to get an exceptionally accurate match rate. A starting line check for an "@" symbol in the 
current line followed by a assessment that a "." is in the same token, leads into a regex validation of the string.

##### Phone Number

What stood out from the example data sets provided was there could be more than one number that would meet the 
qualifications for a telephone number (ex: a fax number). After some research, [E.164](https://en.wikipedia.org/wiki/E.164) 
, an international telecom numbering standard, revealed phone number regulations with a maximum digit length of 15, 
but no minimum. Based off the American standard, if a digit count in a line is greater than 6, and "fax" is not found 
in the same line, then it is valid. If multiple phone numbers are provided, such as "cell" and "office", 
only the last one processed will be stored. 

##### Name 

Attempting to extract the name field independent of the data points proved to be difficult. Research led to an 
[article](https://thetokenizer.com/2013/08/25/how-to-easily-recognize-peoples-names-in-a-text/) on Name Entity 
Recognition or NER, a problem set under Natural Language Processing; this continued on into 
implementations of Python's [nltk](http://www.nltk.org/) (Natural Language Toolkit) and 
[Stanford's CoreNLP](https://stanfordnlp.github.io/CoreNLP/) server. Passing full documents into the CoreNLP server returned
proper entity sets up until the "Arthur Wilson" (third example input) set. Reassessing the data set 
as a whole led to the realization that the email field's username segment could be used to validate the name. 
To view the code prior to the current implemtation using the CoreNLP server and entity tagging go to 
[commit c37bf28](https://github.com/TheShankapotomus/BusinessCard-OCR/commit/c37bf28bffbe6cb8b2eebbf3033a3740b991e12f)!

#### Open Source Tools

The only open source library used in the Python code is [PyYAML](https://pypi.python.org/pypi/PyYAML); this is done 
solely for parsing the YAML files in __/tests/samples/__ . The regex string provided by [emailregex.com](http://emailregex.com/) 
is used to validate extracted emails in the _BusinessCardParser_ class. The Dockerfile is built off of 
[CentOS 7](https://hub.docker.com/_/centos/) with a library called [dumb-init](https://github.com/Yelp/dumb-init) to
allow for cleaner processes and signal handling. 

#### Test Cases

Two sample files are provided, __asymmetrik.yaml__ which contains the three examples provided at the 
[challenges site](https://www.asymmetrik.com/programming-challenges/), and __custom.yaml__ with three examples containing 
obfuscated data and formats modeled off of real business cards. The format for each YAML file is multiple top level 
examples containing their _document_ and _output_ attributes, both types being multi-line strings. The _test_parser_ 
module in __/tests__ loads these files in their respective methods ( _test_asymmetrik_(), _test_custom_() ) then uses a 
_BusinessCardParser_ object to process the example's documents and compare the output to the expected example output. 