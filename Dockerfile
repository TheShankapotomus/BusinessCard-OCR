FROM centos:centos7

ADD http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip /opt/

ENV VERSION 3.6.3
ENV PYTHON3 https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
ENV DUMB_INIT https://github.com/Yelp/dumb-init/releases/download/v1.0.2/dumb-init_1.0.2_amd64

#Install system packages
RUN yum update -y && yum groupinstall -y "Development tools"
RUN yum install -y wget

#Install Python 3.6.3 and dumb-init
RUN wget -qO /tmp/Python-$VERSION.tgz $PYTHON3 \
 && tar zxf /tmp/Python-$VERSION.tgz -C /tmp/ \
 && (cd /tmp/Python-$VERSION && ./configure --quiet) \
 && sudo make -C /tmp/Python-$VERSION -s -j 4 > /dev/null 2>&1 \
 && sudo make -C /tmp/Python-$VERSION -s -j 4 install > /dev/null 2>&1 \

 && wget -qO /usr/bin/dumb-init $DUMB_INIT \
 && chmod +x /usr/bin/dumb-init \
 && dumb-init --version \

#Unpack nlp packages and load jars into ClassPATH
#Install java8 here too
RUN unzip /opt/stanford*.zip \
 && for f in $(ls stanford*/*.jar); do \
        export CLASSPATH="${CLASSPATH}:$(pwd)/${f}"; \
    done

