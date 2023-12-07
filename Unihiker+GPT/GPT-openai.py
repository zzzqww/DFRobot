from unihiker import Audio
from unihiker import GUI
import openai
import time

openai.api_key = "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" #填入OpenAI的api key

# openai语音转文本
def asr():
    audio_file= open("input.mp3", "rb")

    transcript = openai.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="text"
    )

    return transcript


# openai文本转语音
def tts(text):
    response = openai.audio.speech.create(
        model="tts-1",
        # Experiment with different voices (alloy, echo, fable, onyx, nova, and shimmer) 
        voice="alloy",
        input=text,
    )

    response.stream_to_file("output.mp3")


# openai对话
def askOpenAI(question):
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = question
    )
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content


# 文字显示
def text_update():
    global y1
    time.sleep(16)
    while True:
        y1 -= 2
        time.sleep(0.15)
        trans.config(y = y1)

# 回答打断返回功能
def play_audio():
    global flag
    u_audio.play('output.mp3')
    u_gui.stop_thread(thread1)
    flag = 0


def monitor_silence():
    global is_recording, monitor_thread
    silence_time = 0

    while is_recording:
        sound_level = u_audio.sound_level()
        if sound_level < THRESHOLD:
            silence_time += 0.1
        else:
            silence_time = 0

        if silence_time >= SILENCE_DURATION:
            # print("检测到2秒静音，停止录音。")
            u_audio.stop_record()
            is_recording = 0
            u_gui.stop_thread(monitor_thread)
            
        time.sleep(0.1)  # 每0.1秒检测一次

def start_recording_with_silence_detection(filename):
    global is_recording, monitor_thread
    is_recording = 1
    u_audio.start_record(filename)  # 开始录音
    monitor_thread = u_gui.start_thread(monitor_silence)


# 事件回调函数
def button_click1():
    global flag
    flag = 1
    

def button_click2():
    global flag
    flag = 3

def button_click3():
    global flag,thread1,thread2
    flag = 0
    u_gui.stop_thread(thread1)
    u_gui.stop_thread(thread2)





u_gui=GUI()
u_audio = Audio()


# GUI初始化
img1=u_gui.draw_image(image="background.jpg",x=0,y=0,w=240)
button=u_gui.draw_image(image="mic.jpg",x=13,y=240,h=60,onclick=button_click1)
refresh=u_gui.draw_image(image="refresh.jpg",x=157,y=240,h=60,onclick=button_click2)
init=u_gui.draw_text(text="Tap to speak",x=27,y=50,font_size=15, color="#00CCCC")
trans=u_gui.draw_text(text="",x=5,y=0, color="#000000", w=230)
back=u_gui.draw_image(image="backk.jpg",x=0,y=268,onclick=button_click3)
DigitalTime=u_gui.draw_digit(text=time.strftime("%Y/%m/%d       %H:%M"),x=9,y=5,font_size=12, color="black")


result = ""
flag = 0
text_display = ""
y1 = 0

message = [{"role": "system", "content": "You are a helpful assistant."}]
user = {"role": "user", "content": ""}
assistant = {"role": "assistant", "content": ""}

# 阈值设定，具体值需要根据实际情况调整
THRESHOLD = 20  # 假设这是检测到的静音阈值
SILENCE_DURATION = 2  # 2秒静音时间

# 录音控制变量
is_recording = 0


while True:
    if (flag == 0):
        button.config(image="mic.jpg",state="normal")
        refresh.config(image="refresh.jpg",state="normal")
        back.config(image="",state="disable")
        DigitalTime.config(text=time.strftime("%Y/%m/%d       %H:%M"))
        

    if (flag == 3):
        message.clear()
        message = [{"role": "system", "content": "You are a helpful assistant."}]

    if (flag == 2):
        DigitalTime.config(text=time.strftime(""))
        azure_synthesis_result = askOpenAI(message)
        assistant["content"] = azure_synthesis_result
        message.append(assistant.copy())
        tts(azure_synthesis_result)
        trans.config(text=azure_synthesis_result)
        back.config(image="backk.jpg",state="normal")

        thread1=u_gui.start_thread(text_update)
        thread2=u_gui.start_thread(play_audio)


        while not (flag == 0):
            pass

        y1 = 0
        trans.config(text="      ", y = y1)
        button.config(image="",state="normal")
        refresh.config(image="",state="normal")
        init.config(x=15)
    
    if (flag == 1):
        DigitalTime.config(text=time.strftime(""))
        is_recording = 1
        init.config(x=600)
        trans .config(text="Listening。。。")
        start_recording_with_silence_detection('input.mp3')
        button.config(image="",state="disable")
        refresh.config(image="",state="disable")
        back.config(image="",state="disable")

        while not ((is_recording == 0)):
            pass

        back.config(image="",state="disable")
        result = asr()
        user["content"] = result
        message.append(user.copy())
        trans .config(text=result)
        time.sleep(2)
        trans .config(text="Thinking。。。")
        flag = 2