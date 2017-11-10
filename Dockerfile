FROM centos:centos7

ADD http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip /tmp/

ENV VERSION 3.6.3
ENV PYTHON3 https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tgz
ENV DUMB_INIT https://github.com/Yelp/dumb-init/releases/download/v1.0.2/dumb-init_1.0.2_amd64

#Install system packages
RUN yum update -y \
 && yum groupinstall -y "Development tools" \
 && yum install -y wget java-1.8.0-openjdk-devel

#Install Python 3.6.3
RUN wget -qO /tmp/Python-$VERSION.tgz $PYTHON3 \
 && tar zxf /tmp/Python-$VERSION.tgz -C /tmp/ \
 && (cd /tmp/Python-$VERSION && ./configure --quiet) \
 && sudo make -C /tmp/Python-$VERSION -s -j 4 > /dev/null 2>&1 \
 && sudo make -C /tmp/Python-$VERSION -s -j 4 install > /dev/null 2>&1 \

#Install dumb-init
RUN wget -qO /usr/bin/dumb-init $DUMB_INIT \
 && chmod +x /usr/bin/dumb-init \
 && dumb-init --version \

#Unpack nlp packages and load jars into CLASSPATH
RUN unzip -d /opt/ /tmp/stanford*.zip \
 && for f in $(ls stanford*/*.jar); do \
        export CLASSPATH="${CLASSPATH}:$(pwd)/${f}"; \
    done
