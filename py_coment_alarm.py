import pygame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pyttsx3
import os


current_dir = os.path.dirname(os.path.abspath(__file__))



url = "https://omlet.gg/streamchat/username" # set the URL of the page to be parsed and the sound file to play
sound_file = os.path.join(current_dir, "sounds", "alert.mp3")

pygame.init()  # initialize Pygame
pygame.mixer.init()

sound = pygame.mixer.Sound(sound_file)  # get sound object

driver = webdriver.Chrome()  # initialize the web driver

engine = pyttsx3.init()

driver.get(url)


time.sleep(5)

new_content = current_content = driver.page_source
comments = []
while True:

    try:    # waiting for comments
        comments = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[class='msg-container__message__2_Y4y animated msg-container-tall msg-container-styled']")))
    except TimeoutException:
        print("Комментарии не найдены")

    num_comments = len(comments)  # get the current number of comments

    try:    # waiting for new comments
        comments = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@class='msg-container__message__2_Y4y animated msg-container-tall msg-container-styled']")))
    except TimeoutException:
        print("Новые комментарии не найдены")

    new_num_comments = len(comments)    # get the new number of comments

    if new_num_comments > num_comments:  # check if there are new comments
        sound.play()    # play sound
        for i in range(num_comments, new_num_comments):  # read new commentsv
            print(comments[i].text)
            time.sleep(2)
            engine.say(comments[i].text)
            engine.runAndWait()
