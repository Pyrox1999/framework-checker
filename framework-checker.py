import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
import random
import pgzrun
import pygame
import requests

pygame.mixer.music.load("song.ogg") #glitchart
pygame.mixer.music.play(-1)

level = -2
message=""
target=""
made=False

def detect_frameworks(url):
    frameworks = {
        "jQuery": ["jquery"],
        "React": ["react", "data-reactroot"],
        "Vue.js": ["vue", "v-cloak", "v-bind", "v-model"],
        "Angular": ["angular", "ng-app", "ng-model", "ng-controller"],
        "Svelte": ["svelte"],
        "Ember.js": ["ember"],
        "Backbone.js": ["backbone"],
        "Alpine.js": ["alpine", "x-data", "x-bind", "x-show"],
        "Next.js": ["next"],
        "Nuxt.js": ["nuxt"],
        "Meteor": ["meteor"],
        "Polymer": ["polymer"],
        "Vanilla JS": []  
    }
    
    try:
        response = requests.get(url, timeout=10)
        html = response.text.lower()
    except Exception as e:
        return {"error": str(e)}
    
    results = {}
    for name, indicators in frameworks.items():
        if name == "Vanilla JS":
            results[name] = all(not any(ind in html for ind in ind_list) 
                                for fw, ind_list in frameworks.items() if fw != "Vanilla JS")
        else:
            results[name] = any(indicator in html for indicator in indicators)
    
    return results


def draw():
    global level, target, message
    screen.clear()
    if level==-2:
        screen.blit("disclaimer",(0,0))
    if level == -1:
        screen.blit("title", (0, 0))
    elif level == 0:
        screen.blit("intro", (0, 0))
    elif level == 1:
        screen.blit("back", (0, 0))
        screen.draw.text("Website to identify framework:", center=(400, 130), fontsize=24, color=(25, 200, 255))
        screen.draw.text(target, center=(400, 180), fontsize=24, color=(255, 255, 0))
    elif level == 2:
        screen.draw.text(message, center=(400, 180), fontsize=24, color=(255, 255, 0))

def on_key_down(key, unicode=None):
    global level, target
    if key==keys.ESCAPE:
        pygame.quit()
    if key == keys.BACKSPACE:
        target = ""
    elif key == keys.RETURN and level == 1:
        if not target.strip():
            target = "127.0.0.1"
        level = 2
    elif unicode and key != keys.RETURN and level==1:
        target += unicode

def update():
    global level,target,message,made
    if (level == 0 or level==-2) and keyboard.RETURN:
        level +=1
    elif (level ==-1 or level==2) and keyboard.space:
        level = 0
    if level==2 and not made:
        detected = detect_frameworks(target)
        made=True
        for fw, present in detected.items():
            message+=f"{fw}: {'Found' if present else 'Not found'}\n"

pgzrun.go()
