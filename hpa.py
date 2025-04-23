@app.post("/create_hpa/")
def create_hpa(deployment_name: str, cpu_threshold: int = 50):
    api_instance = client.AutoscalingV1Api()
    
    hpa = client.V1HorizontalPodAutoscaler(
        metadata=client.V1ObjectMeta(name=f"{deployment_name}-hpa"),
        spec=client.V1HorizontalPodAutoscalerSpec(
            scale_target_ref=client.V1CrossVersionObjectReference(
                api_version="apps/v1", kind="Deployment", name=deployment_name
            ),
            min_replicas=1,
            max_replicas=10,
            target_cpu_utilization_percentage=cpu_threshold
        )
    )
    
    api_instance.create_namespaced_horizontal_pod_autoscaler(namespace="default", body=hpa)
    return {"message": f"HPA criado para {deployment_name} com threshold de {cpu_threshold}% CPU"}
