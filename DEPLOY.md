# Instructions for finishing setup and deployment

To finish setting up the application:

1. Edit `.envrc` with your own STACK_NAME, HOST_NAME, and SITE_URL
2. `source ~/.bashrc` to activate direnv, `direnv allow` to load the environment.
3. Initialize the docker stack with `docker swarm init --advertise-addr [ipaddress]`

Now you can deploy the application:

`./deploy.sh`

Repeat this command when you have committed changes to the deployment branch (default
`main`) that you are ready to deploy. Setting up CI/CD is left as an exercise for the
reader. Enjoy!
