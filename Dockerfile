FROM centos:centos7


RUN yum update -y && yum groupinstall -y "Development tools"

#TODO install dumb init, set params, add CMD