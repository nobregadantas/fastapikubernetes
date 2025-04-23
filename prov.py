from fastapi import FastAPI
from kubernetes import client, config

app = FastAPI()

# Carregar configuração do cluster
config.load_kube_config()

@app.post("/create_deployment/")
def create_deployment(name: str, image: str, replicas: int = 1):
    api_instance = client.AppsV1Api()
    
    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector={"matchLabels": {"app": name}},
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": name}),
                spec=client.V1PodSpec(
                    containers=[client.V1Container(name=name, image=image)]
                )
            )
        )
    )
    
    api_instance.create_namespaced_deployment(namespace="default", body=deployment)
    return {"message": f"Deployment {name} criado com sucesso!"}
