# Business Card OCR

___

### Table of Contents

1. [Preface](#preface) 
2. [Quickstart](#quickstart)
3. [Engineering and Design](#design)

___
## Preface <a name="preface"></a>

This project was designed in [Python](https://www.python.org/), specifically version 3.6, and the application
can either be run standalone in a terminal or within a [Docker](https://www.docker.com/)  container. The reason
behind adding a container option is installing __Python 3.6__ could be presented as cumbersome to a tester and 
with the growth of _containerization_ it seemed like a pefectly viable avenue for the presentation and execution
of this project.

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

For ease of use and so that one does not have to directly modify their development environment to test/run this program,
a Dockerfile was built to containerize the application. Execute all commands in a Bash terminal while in the root
directory of the _AsymmetrikOCR_ project. Please reference the [Tool Stack](#tool-stack) in the [Preface](#preface) for
the required dev tools for this section.

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
[Asymmetrik Challenges site](https://www.asymmetrik.com/programming-challenges/); this string type is needed
so that the escaped characters can be parsed properly. 

- Executing a _docker run_ without specifiying the _--name_ flag will give the container an auto-generated name

- Using the _docker run_ commands with _-d_, prior to the image name, quiets the output which can be viewed
  later with _docker logs_

___

##Engineering and Design <a name="design"></a>

This section will go over some of the code design choices I made when working on this project, as well as some road bumps
I hit along the way and their mitigations.

#### Code Implementation
For the actual implementation of the OCR I felt that a single Python module , _ocr/parser.py_, was plenty and having 
both the _BusinessCardParser_ and _\_ContactInfo_ classes in one file leads to easier comprehension of the implementation. 
Compliance with [PEP8](https://www.python.org/dev/peps/pep-0008/) was something I strove to keep in line with. 

- Class: _BusinessCardParser_
    - Has a one "public" accessor method: _get_contact_info_
    - Returns a _\_ContactInfo_ object from the _get_contact_info_ method
    - The _\_filter_fields_ method uses the _\_ContactInfo_._\_\_slots__\_ attribute to build the corresponding dictionary
    - The _\_filter_fields_ method returns a dictionary purpose built to populate a _\_ContactInfo_ object
    - The fields _email_ and _phone_ are parsed independently, while the _name_ field requires a populated email field
    
- Class: _\_ContactInfo_
    - Has three "public" accessor methods: _get_name_, _get_phone_number_, and _get_email_address_ 
    - Uses the _\_\_slots___ attribute to minimize memory profile
    - _kwargs**_ is explicitly used to populate object on initialization
    - All variable attributes are name mangled so that cannot be accessed directly
    - Getters all call _str()_ on their respective attribute, this adds redundancy if attribute object changes from _str_ type
 
#### Parsing Algorithm

The initial checks were quick to implement for both email and phone, however the name parsing implementation was more
than I initially anticipated. This algorithm is implemented in the method _\_filter_fields_ under the class _BusinessCardParser_. 
Here is the breakdown of how I handled finding each type in the data set.

##### Initial Assumptions

The initial thoughts I had on the data sets being processed by this program were, if a set is going to be parsed 
there are likely to be minimal if any oddities (due to the professional nature of business cards); Along with this, the 
data sets to be processed will be well formed, thus parsing line by line would work well.

##### Email Address

With email parsing/regex I have been told before that if it has a "." and an "@" it is most likely valid. I thought that 
the simplicity of a check like that would be quick, but true validation was necessary. After digging into some 
email parsing research, I was led to [emailregex.com](http://emailregex.com/) which had the exact regex I should use 
in Python to get an exceptionally accurate match rate. Via the email regex site and other sources I was led to 
[RFC 5322](https://tools.ietf.org/html/rfc5322) which is the compliant RFC to handle email addressing. I ended up using
the regex string provided by emailregex.com as it covered exactly what I needed, however the line check is just as simple 
as having a "@" and "." in the same string! There was a discrepancy in the community over an small error in the regex presented
by emailregex.com noted [here](https://stackoverflow.com/questions/201323/using-a-regular-expression-to-validate-an-email-address)
, however it is outside of the scope of this project's use case.

##### Phone Number

This segment didn't seem to particularly difficult, what stood out from the examples provided was there could be more than
one number that would meet the qualifications for a telephone number, that being a fax number! I did some research on 
validating phone numbers and came up quite short. What I did find was [E.164](https://en.wikipedia.org/wiki/E.164), 
an internation telcom numbering plan, seems to regulate with a maximum length of 15 digits, but no minimum. After this, 
I divulged that as long as the digit count in a line is greater than 6, and "fax" is not in the string, it should be 
fairly compliant with most standards outside of minimal oddities. I chose 6 as my delimiter since most American numbers
,with an area code, are 10 digits long (7 without), and most address have a street number of 5 digits or less and 
zipcode of 5 digits or less on a seperate line. Having the zipcode and street number on a seperate line is key, and 
a typical address format, as if they were on the same line the processing would be invalid. One note about the phone
number parsing, if multiple phone numbers are provide, such as "office" and "cell", the latter will be taken as it was
parsed last. 

##### Name 

When I started to handle the name parsing, I isolated the name data from any of the other available data points in the set; 
I thought about it as if I was processing the data myself. When you look at the text "John Smith", that registers itself
as a person's name in your brain, but writing a program to recognize it as a name seemed like quite a challenge in of itself. 
It turned out to be one! I stumbled upon an [article](https://thetokenizer.com/2013/08/25/how-to-easily-recognize-peoples-names-in-a-text/)
which related to Name Entity Recognition or NER, a problem set under Natural Language Processing. This seemed to be my
solution! If a library can process a language naturally then NER was my solution to finding names in arbitrary strings.
After drudging through a plentiful amount of articles, I started to use the [nltk](http://www.nltk.org/) 
(Natural Language Toolkit) and [Stanford's CoreNLP](https://stanfordnlp.github.io/CoreNLP/) to start to work on processing
the strings. If I used a full input document then I was able to figure out what was a PERSON entity and what wasn't, 
isolating the names I needed! This worked up until the set with "Arthur Wilson" (third example input) which output his 
name strings as merely an OBJECT entity. I had my doubts about the problem being so complex, and sat back after implementing
the CoreNLP server with failed tests. Then I looked at my data set as a whole and realized that the email field in the 
set contained exactly what I was looking for. If string match against an extracted email, then a simple solution to 
finding the line with a name was to be had. Now, making sure that an email field is parsed, the algorithm checks
that a line's string token exists before the "@" in an email, if it does then that is the line with the valid name. 
To view the code prior to the current implemtation using the CoreNLP server and entity tagging go to 
[commit c37bf28](https://github.com/TheShankapotomus/AsymmetrikOCR/commit/c37bf28bffbe6cb8b2eebbf3033a3740b991e12f)!

#### Open Source Tools

The only open source library used in the Python code is [PyYAML](https://pypi.python.org/pypi/PyYAML); this is done 
solely for parsing the YAML files in _/tests/samples/_ . As explained above the regex provided by [emailregex.com](http://emailregex.com/)
is used to validate the email's that are parsed out of the data set. For the Dockerfile, a library called 
[dumb-init](https://github.com/Yelp/dumb-init) is used to formalize the container a tad, it allows for cleaner
closing of processes and signal handling within the container if it ever has to be expanded on. Outside of that, the 
container uses [CentOS 7](https://hub.docker.com/_/centos/) and standard yum repositories for building Python 3.6 
and downloading the dumb-init binary.

#### Test Cases

The test cases implemented are built for ease of use for the tester. Two files are provided, _asymmetrik.yaml_ which contains
the three examples provided at the [Asymmetrik Challenges site](https://www.asymmetrik.com/programming-challenges/), and 
_custom.yaml_ with three examples containing obfuscated data and moderately unique formats modeled off of real business cards.
The _test_parser_ in _/tests_ loads these files in their respective methods (_test_asymmetrik_, _test_custom_) thenn uses 
_BusinessCardParser_ class to process the example's documents and compare them to the expected example output. The format
for the YAML file is straightforward with examples being on the top level, containing only their _document_ and _output_ 
attributes, both types being multi-line strings. 