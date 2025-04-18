FROM registry.community.greenbone.net/community/vulnerability-tests AS nasl
# use latest version
RUN mv `ls -d /var/lib/openvas/* | sort -r | head -n 1`/vt-data/nasl /nasl

FROM golang AS binaries
COPY --chmod=7777 smoketest /usr/local/src
WORKDIR /usr/local/src
RUN make build-cmds

FROM registry.community.greenbone.net/community/openvas-scanner:edge

RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
    mosquitto \
    redis \
    gcc \
    python3-dev \
    python3 \
    python3-pip \
    openssh-server &&\
	apt-get remove --purge --auto-remove -y &&\
	rm -rf /var/lib/apt/lists/*
COPY --chmod=7777 . /usr/local/src/ospd-openvas
COPY smoketest/redis.conf /etc/redis/redis.conf
RUN rm -rf /var/lib/openvas/plugins/*
RUN cp -r /usr/local/src/ospd-openvas/smoketest/data/notus /var/lib/notus

RUN useradd -rm -s /bin/bash -g redis -u 1000 gvm
RUN mkdir /run/redis
RUN chown gvm:redis /run/redis
RUN mkdir -p /var/run/ospd/
RUN chown gvm:redis /var/run/ospd
RUN touch /etc/openvas/openvas_log.conf
RUN chown gvm:redis /etc/openvas/openvas_log.conf
WORKDIR /usr/local/src/ospd-openvas
RUN python3 -m pip install --break-system-packages .
RUN chown gvm:redis /var/log/gvm
RUN mkdir /run/mosquitto
RUN echo "allow_anonymous true" >> /etc/mosquitto.conf
RUN echo "pid_file /tmp/mosquitto.pid" >> /etc/mosquitto.conf
RUN echo "log_dest file /tmp/mosquitto.log" >> /etc/mosquitto.conf
RUN echo "persistence_location = /tmp/" >> /etc/mosquitto.conf
RUN echo "persistence true" >> /etc/mosquitto.conf
RUN echo "mqtt_server_uri = localhost:1883" >> /etc/openvas/openvas.conf
RUN chown mosquitto:mosquitto /run/mosquitto
RUN mkdir -p /var/log/mosquitto/
RUN chown mosquitto:mosquitto /var/log/mosquitto
RUN chmod 774 /var/log/mosquitto

COPY --from=binaries /usr/local/src/bin/* /usr/local/bin/
RUN mv /usr/local/src/ospd-openvas/smoketest/run-tests.sh /usr/local/bin/run
COPY --from=nasl --chmod=7777 /nasl /var/lib/openvas/plugins

RUN mkdir -p /usr/local/src/policies 
COPY smoketest/gatherpackagelist-c18bb781-3740-44c2-aa01-1b73a00066e8.xml /usr/local/src/policies
RUN ospd-policy-feed -p /usr/local/src/policies -t /usr/local/src/plugins
RUN rm -rf /var/lib/openvas/plugins
RUN mv /usr/local/src/plugins /var/lib/openvas/plugins
RUN cp -r /usr/local/src/ospd-openvas/smoketest/data/plugins/* /var/lib/openvas/plugins

RUN rm -rf /usr/local/src/ospd-openvas
RUN apt-get remove --purge --auto-remove -y python3-pip
RUN chown -R gvm:redis /var/lib/openvas/plugins/
RUN mkdir /run/sshd
# make gvm capable of running sshd
RUN chown -R gvm:redis /etc/ssh
RUN echo 'gvm:test' | chpasswd
RUN sed -i 's/#PidFile/Pidfile/' /etc/ssh/sshd_config
USER gvm
WORKDIR /home/gvm
CMD /usr/local/bin/run
