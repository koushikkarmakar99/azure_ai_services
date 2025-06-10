FROM python:3.13-slim

# Create a non-root user
ARG USERNAME=devcontainer-user
ARG GROUPNAME=devcontainer-group
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create a group and user
RUN groupadd -g ${USER_GID} ${GROUPNAME} \
    && useradd -m -u ${USER_UID} -g ${GROUPNAME} ${USERNAME}
   
# Set working directory
WORKDIR /workspaces

# Install Git inside DevContainer
RUN apt-get update && apt-get install -y git

# Ensure the hostname is added to /etc/hosts
# RUN sudo echo "127.0.0.1 azureai.homelab.dev" >> /etc/hosts

# Copy all files from the current directory to the container
COPY . .

# Change ownership of the /workspaces directory to the non-root user
RUN chown -R ${USERNAME}:${GROUPNAME} /workspaces \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD: ALL" >> /dev/null
 
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

# Switch to the non-root user
USER $USERNAME

# Set the default command to run when the container starts
CMD [ "bash" ]
