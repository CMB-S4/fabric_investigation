
FROM ubuntu:latest

RUN set -ex \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq python3.9 \
    && apt-get install -yqq python3-pip \
    && apt-get install -yqq emacs

#expose ports to outside container for web app access
#EXPOSE 10500


LABEL maintainer="Don Petravick"
WORKDIR /app

#Get all the soruces. we need
ADD ./requirements.txt /app
ADD *.py ./

# Install the python that is our app.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



# Make a directory with the same path ..
# ... as the users' part the therir fabric files.
# ... so we can mount the files in the container
# ... and scripts, etc have a chance of working. 

ARG FABRIC_FILES
RUN mkdir -p  $FABRIC_FILES
RUN ln -s $FABRIC_FILES/setup.sh ./setup.sh

# CLEANUP
RUN apt-get autoremove -yqq --purge \
 && apt-get clean
 
#CMD [ "python", "/app/hello.py" ]
ENV SETUP=$FABRIC_FILES
#CMD ["/usr/bin/bash", "-c", "source $SETUP/setup.sh"]   
CMD ["/usr/bin/bash"]