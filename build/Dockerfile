FROM python:3.13.0rc2-alpine

# Set the work directory to the app folder.
WORKDIR /hai-on-hackerone

# Install Python dependencies.
COPY requirements.txt /hai-on-hackerone
RUN  pip3 install --no-cache-dir --disable-pip-version-check -r requirements.txt

# Copy only the relevant Python files into the container.
COPY requirements.txt /hai-on-hackerone
COPY webserver /hai-on-hackerone/webserver
COPY watcher /hai-on-hackerone/watcher
COPY cli /hai-on-hackerone/cli

# Expose the port that the app runs on.
EXPOSE 5000

# Set the environment variable for the Flask app.
ENV FLASK_APP=webserver/app.py

# Run the Bash script and the Flask app using a process manager
CMD ["sh", "-c", "python ./watcher/watch_reports.py & flask run --host 0.0.0.0"]