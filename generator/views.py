from django.http import JsonResponse
from .tasks import generate_image

def generate_images(request):
    prompts = ["A red flying dog", "A piano ninja", "A footballer kid"]
    task_ids = []

    for prompt in prompts:
        task = generate_image.delay(prompt)  # Use .delay() to run the task asynchronously
        task_ids.append(task.id)  # Collect the task IDs to track the tasks

    return JsonResponse({"status": "tasks started", "task_ids": task_ids})
