#!/bin/bash
set -e

env=$1

if [[ "${env}" = "stage" ]]; then
    # Set the Kubernetes context for dev environment
    echo "Started deployment for ${env}"
    kubectl config use-context arn:aws:eks:ap-south-1:organization_account_alias:cluster/dev-cluster

elif [[ "${env}" = "prod" ]]; then
    # Set the Kubernetes context for prod environment
    kubectl config use-context arn:aws:eks:ap-south-1:organization_account_alias:cluster/prod-cluster
    # Prompt for confirmation
    read -r -p "Are you sure you want to deploy to prod environment? (y/n): " confirm
    if [[ "${confirm}" != "y" ]]; then
        echo "Deployment to prod environment canceled."
        exit 0
    fi
else
    echo "Invalid environment. Please provide 'stage' or 'prod' as the environment."
    exit 1
fi

echo "Started deployment for ${env}"

echo "Logging to Aws ECR"
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin organization_account_alias.dkr.ecr.ap-south-1.amazonaws.com

echo "Building The Docker Image with tag name as latest ..."

docker build --build-arg FLASK_MODE=production --no-cache -t ums-"${env}":latest -f Dockerfile .
docker tag ums-"${env}":latest organization_account_alias.dkr.ecr.ap-south-1.amazonaws.com/ums-"${env}":latest

echo "Docker Image Built"

echo "Pushing the Docker Image"

docker push organization_account_alias.dkr.ecr.ap-south-1.amazonaws.com/ums-"${env}":latest

echo "👉 Deleting Previous Running Pod"

if helm list -q | grep -q ums-"${env}"; then
    helm delete ums-"${env}"
fi

echo "Attaching to latest docker container"

helm install ums-"${env}" k8s -f k8s/values/"${env}".yaml
