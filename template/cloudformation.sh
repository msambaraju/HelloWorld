#!/usr/bin/env sh
aws cloudformation deploy --stack-name $1 --template-file ./docker_server.template --parameter-overrides KeyName=MallikEC2Key

