from django.http import JsonResponse
import subprocess
import json

def ollama_chat(request):
    if request.method == "POST":
        # Parse the input message from the request
        try:
            data = json.loads(request.body)  # Parse JSON body
            user_message = data.get("message", "")

            if user_message:
                # Run the ollama command with the user's message
                try:
                    result = subprocess.run(
                        ["ollama", "run", "deepseek-r1:1.5b"],
                        input=user_message,
                        text=True,
                        capture_output=True,
                        check=True
                    )
                    ai_response = result.stdout.strip()  # Get the output from the command
                except subprocess.CalledProcessError as e:
                    ai_response = f"Error running ollama: {e.stderr.strip()}"
            else:
                ai_response = "Please provide a valid message."

            return JsonResponse({"response": ai_response})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)

from django.shortcuts import render

def learn_with_ai(request):
    return render(request, 'learn_with_ai/learn_with_ai.html')  # Updated path

