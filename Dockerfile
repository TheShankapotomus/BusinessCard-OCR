FROM centos:centos7

COPY . /opt/asymmetrik

ENV VERSION 3.6.3
ENV PYTHON3 https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tgz
ENV DUMB_INIT https://github.com/Yelp/dumb-init/releases/download/v1.0.2/dumb-init_1.0.2_amd64

#Install system packages
RUN yum update -y \
 && yum groupinstall -y "Development tools" \
 && yum install -y wget

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

WORKDIR /opt/asymmetrik

ENTRYPOINT ["/usr/bin/dumb-init", "--", "python3.6", "-m", "ocr"]
CMD ["--tests"]