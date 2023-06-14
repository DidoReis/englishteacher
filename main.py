# flake8: noqa
import speech_recognition as sr
import pyttsx3
import openai
import random

openai.api_key = 'Your API Key'


def recognize_speech():
    r = sr.Recognizer()
    
    initial_question = random.choice([
        "What is your favorite hobby?",
        "Tell me about your favorite movie.",
        "What do you enjoy doing in your free time?"
    ])

    with sr.Microphone() as source:
        print(initial_question)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="pt-BR")
        print("You answered:", text)

        prompt = create_prompt(initial_question, text)

        response = generate_response(prompt)
        answer = get_model_answer(response)

        print("Model's response:", answer)

        speak_response(answer)

    except sr.UnknownValueError:
        print("Unable to recognize audio.")


def create_prompt(question, answer):
    prompt = (
        "Act as a teacher and language improver for spoken English. "
        "I will speak to you in Portuguese, and you will respond in English "
        "to practice my spoken English. Translate your responses into Portuguese "
        "only if I ask.\n\n"
        "I want you to:\n"
        "- Keep your response organized, limiting it to 100 words.\n"
        "- Point out and correct any conjugation, spelling, grammar, and other "
        "errors I make; this is most important.\n"
        "- Ask me a question in your response.\n\n"
        "Your questions should always be in English, and you should use Portuguese "
        "only to explain my errors.\n\n"
        "Now let's start practicing. Answer the following question in English:\n\n"
        f"{question}\n\nYour response: {answer}"
    )
    return prompt


def generate_response(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100
    )
    return response


def get_model_answer(response):
    answer = response.choices[0].text.strip()
    return answer


def speak_response(answer):
    engine = pyttsx3.init()
    engine.say(answer)
    engine.runAndWait()


recognize_speech()






