#############################################
# Select the OS
FROM python:3.9.7-slim-buster

#############################################
# Setup default flywheel/v0 directory
ENV FLYWHEEL=/flywheel/v0
RUN mkdir -p ${FLYWHEEL}
WORKDIR ${FLYWHEEL}
COPY requirements.txt run DR_estimation.py manifest.json README.md $FLYWHEEL/

#############################################
# install required dependencies
RUN pip install -r requirements.txt

#############################################
# Configure entrypoint
RUN chmod a+x /flywheel/v0/run
ENTRYPOINT ["/flywheel/v0/run"]
