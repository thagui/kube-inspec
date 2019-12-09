FROM chef/inspec:latest

RUN apk add python3 py3-requests
RUN inspec --chef-license=accept

COPY inspec_audit.py /share

CMD python3 /share/inspec_audit.py