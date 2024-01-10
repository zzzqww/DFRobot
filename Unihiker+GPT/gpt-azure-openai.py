from unihiker import Audio
from unihiker import GUI
import openai
import time
import os 
from azure.cognitiveservices.speech import SpeechConfig 


speech_key = "xxxxx" # Fill key 
service_region = "xxxxx" # Enter Location/Region 

openai.api_key = "xxxxxx" #Fill key 

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:

    
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)


# Set up the subscription info for the Speech Service:
# Replace with your own subscription key and service region (e.g., "japaneast").



def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    speech_recognition_result = speech_recognizer.recognize_once_async().get()


    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        # print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


def atts(text):
    speech_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceResponse_RequestSentenceBoundary, value='true')
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesizer.synthesis_word_boundary.connect(speech_synthesizer_word_boundary_cb)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()


# text display
def speech_synthesizer_word_boundary_cb(evt: speechsdk.SessionEventArgs):
    global text_display

    if not (evt.boundary_type == speechsdk.SpeechSynthesisBoundaryType.Sentence):
        text_result = evt.text
        text_display = text_display + "   " + text_result
        trans.config(text = text_display)
    
    if evt.text == ".":
        text_display = ""



def asr():
    audio_file= open("input.mp3", "rb")

    transcript = openai.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="text"
    )

    return transcript


def tts(text):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    response.stream_to_file("output.mp3")



def askOpenAI(question):
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = question
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content




def button_click1():
    global flag
    flag = 1


def button_click2():
    global flag
    flag = 3


u_gui=GUI()
u_audio = Audio()



speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_language = 'en-US'
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"


img1=u_gui.draw_image(image="background.jpg",x=0,y=0,w=240)
button=u_gui.draw_image(image="mic.jpg",x=13,y=240,h=60,onclick=button_click1)
refresh=u_gui.draw_image(image="refresh.jpg",x=157,y=240,h=60,onclick=button_click2)
init=u_gui.draw_text(text="Tap to speak",x=27,y=50,font_size=15, color="#00CCCC")
trans=u_gui.draw_text(text="",x=2,y=0,font_size=12, color="#000000")
trans.config(w=230)
result = ""
flag = 0
text_display = ""

message = [{"role": "system", "content": "You are a helpful assistant."}]
user = {"role": "user", "content": ""}
assistant = {"role": "assistant", "content": ""}




while True:
    if (flag == 0):
        button.config(image="mic.jpg",state="normal")
        refresh.config(image="refresh.jpg",state="normal")
        

    if (flag == 3):
        message.clear()
        message = [{"role": "system", "content": "You are a helpful assistant."}]

    if (flag == 2):
        azure_synthesis_result = askOpenAI(message)
        assistant["content"] = azure_synthesis_result
        message.append(assistant.copy())
        trans.config(text=azure_synthesis_result)
        tts(azure_synthesis_result)
        time.sleep(1)
        u_audio.play('output.mp3')
        time.sleep(1)
        

        flag = 0
        trans.config(text="      ")
        button.config(image="",state="normal")
        refresh.config(image="",state="normal")
        init.config(x=15)
    
    if (flag == 1):
        init.config(x=600)
        trans .config(text="Listening。。。")
        button.config(image="",state="disable")
        refresh.config(image="",state="disable")

        u_audio.record('input.mp3', 5)

        result = asr()
        user["content"] = result
        message.append(user.copy())
        trans .config(text=result)
        time.sleep(2)
        trans .config(text="Thinking。。。")
        flag = 2
