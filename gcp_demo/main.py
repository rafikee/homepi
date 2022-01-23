# gcloud functions deploy hello_world --runtime python39 --trigger-http --allow-unauthenticated


def hello_world(request):
    return "Hello, World!\n"
