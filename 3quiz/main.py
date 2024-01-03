from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

Window.fullscreen = False

# Colors and contrasts checked and set according to WCAG 2.1 regulations (partly) / NL

# Questings and answers page
class EventScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.tbutton = None
        self.questions = []
        self.right_answer = None        
        self.numbers = 0
        self.score = 0


    # check which toggle button has pressed 
    def check_button(self, tb): 
        # check togglebutton
        if tb == 1:
            self.tbutton = self.tbutton1
            self.tbutton.background_color = 255/255, 193/255, 193/255, .5
            self.tbutton.disabled_color = 112/255, 70/255, 53/255, 1   
        elif tb == 2:
            self.tbutton = self.tbutton2
            self.tbutton.background_color = 255/255, 193/255, 193/255, .5
            self.tbutton.disabled_color = 112/255, 70/255, 53/255, 1  
        elif tb == 3:
            self.tbutton = self.tbutton3
            self.tbutton.background_color = 255/255, 193/255, 193/255, .5
            self.tbutton.disabled_color = 112/255, 70/255, 53/255, 1  
        else:
            self.tbutton = self.tbutton4
            self.tbutton.background_color = 255/255, 193/255, 193/255, .5
            self.tbutton.disabled_color = 112/255, 70/255, 53/255, 1  
   
        # the next button is able again to press                   
        self.nextbutton.disabled = False 
        
        # First time go to check question category after next has pressed.
        # Round 2-4 go to check if answer is right          
        if self.numbers > 0 and self.numbers < 4:
            self.check_right()

    
    # search question category from data.csv        
    def search_questions(self):

        # set questions to questions list
        with open('data.csv', 'r') as tiedosto:
            for rivi in tiedosto:
                rivi = rivi.replace("\n", "")
                osat = rivi.split(';')
                if self.tbutton == self.tbutton1:
                    if osat[0] == "Food":
                        self.questions.append(osat)
                elif self.tbutton == self.tbutton2:                            
                    if osat[0] == "General":
                        self.questions.append(osat)
                elif osat[0] == "Nature":
                    if self.tbutton == self.tbutton3:
                        self.questions.append(osat)   
                elif osat[0] == "Health":
                    if self.tbutton == self.tbutton4:
                        self.questions.append(osat)          

        # the next button is able again to press            
        self.nextbutton.disabled = False           
           
    # check if answer is right or wrong and change color of button 
    def check_right(self):
        self.tbutton1.disabled = True
        self.tbutton2.disabled = True
        self.tbutton3.disabled = True
        self.tbutton4.disabled = True
        
        # if answer is rigth change color to green and add 1 to right answers 
        if self.tbutton.text == self.right_answer:
            self.score += 1
            self.tbutton.background_color = 127/255, 255/255,0/255,.6
            self.tbutton.color = 40/255, 40/255, 40/255,.8 #0,0,0,1  
            self.tbutton.state = "normal"          
        
        # if answer is wrong change color to red and show the right answer with green color                  
        else:
            self.tbutton.state = "normal"
            self.tbutton.background_color = 255/255,48/255,48/255,.6
            self.tbutton.color = 40/255, 40/255, 40/255,.8
            if self.right_answer == self.tbutton1.text:
                self.tbutton1.background_color = 127/255, 255/255,0/255,.6
                self.tbutton1.color = 40/255, 40/255, 40/255,.8	
            elif self.right_answer == self.tbutton2.text:
                self.tbutton2.background_color = 127/255, 255/255,0/255,.6	
                self.tbutton2.color = 40/255, 40/255, 40/255,.8	
            elif self.right_answer == self.tbutton3.text:
                self.tbutton3.background_color = 127/255, 255/255,0/255,.6	
                self.tbutton3.color = 40/255, 40/255, 40/255,.8	           
            elif self.right_answer == self.tbutton4.text:
                self.tbutton4.background_color = 127/255, 255/255,0/255,.6
                self.tbutton4.color = 40/255, 40/255, 40/255,.8	

        # the next button is able again to press
        self.nextbutton.disabled = False             
        
        # delete the shown (the last) question set from questions list
        if self.numbers < 3:
            self.questions.pop()
        
          
    # change text of togglebuttons when next button is pressed
    def values(self, *args):
        # add 1 every time when next button has clicked
        self.numbers += 1
        
        # first time check category and set question series       
        if self.numbers == 1:
            self.search_questions()
        
        # set basic settings to toggle buttons
        Button.basic_button(self)
                        
        # refresh question and answers 
        self.label1.text = self.questions[-1][1]           
        self.tbutton1.text = self.questions[-1][2] 
        self.tbutton2.text = self.questions[-1][3] 
        self.tbutton3.text = self.questions[-1][4] 
        self.tbutton4.text = self.questions[-1][5] 
        
        # set right answer
        self.right_answer = self.questions[-1][-1]
        
        # set next button disable before answer has pressed
        self.nextbutton.disabled = True                          
        
        # when clicked forth times show result, fifth times restart game 
        if self.numbers == 4:   
            self.show_result()
        elif self.numbers == 5:
            self.play_again()

    # show scores when next button is pressed 4 times
    # two Buttons set instead of four / NL
    def show_result(self):
        self.label1.text = "Your score:" 
        self.label1.font_size = 80
        self.tbutton1.size_hint_y = 0  
        self.tbutton2.size_hint_y = 0  
        self.tbutton3.size_hint_y = 0.30  
        self.tbutton4.size_hint_y = 0.30
        self.tbutton1.text = ""
        self.tbutton2.text = ""
        self.tbutton3.text = f'{str(self.score)}/3'
        self.tbutton4.text = format(int(self.score)/3, '.1%')
        self.tbutton3.disabled_color = 112/255, 70/255, 53/255, 1
        self.tbutton4.disabled_color = 112/255, 70/255, 53/255, 1
        self.tbutton1.background_color = 255/255, 193/255, 193/255, 1 
        self.tbutton2.background_color = 255/255, 193/255, 193/255, 1
        self.tbutton3.background_color = 255/255, 193/255, 193/255, 1  
        self.tbutton4.background_color = 255/255, 193/255, 193/255, 1           
        self.tbutton1.disabled = True  
        self.tbutton2.disabled = True 
        self.tbutton3.disabled = True 
        self.tbutton4.disabled = True

        # the next button is able again to press
        self.nextbutton.disabled = False 
        self.nextbutton.text = "PLAY AGAIN"
                
    # play again start a new round
    def play_again(self):       

        # start position for the new round
        self.tbutton = None
        self.questions = []
        self.right_answer = None        
        self.numbers = 0
        self.score = 0
        self.label1.text = "Please, choose the subject from below"      # no more GDPR / NL
        self.tbutton1.text = "Food" 
        self.tbutton2.text = "General" 
        self.tbutton3.text = "Nature"
        self.tbutton4.text = "Health"
        self.nextbutton.text = "NEXT" 
        self.tbutton1.font_size = 100
        self.tbutton2.font_size = 100
        Button.basic_button(self, restore_size_hint_y=True)

class Button():
       
    # set basic settings to toggle buttons
    def basic_button(self, restore_size_hint_y=False): 
        
        # return right settings after score-settings
        if restore_size_hint_y:         # return to four buttons / NL
            self.label1.font_size = self.width/25
            self.tbutton1.size_hint_y = 0.15
            self.tbutton2.size_hint_y = 0.15
            self.tbutton3.size_hint_y = 0.15
            self.tbutton4.size_hint_y = 0.15     
            self.tbutton1.font_size= self.width/15
            self.tbutton2.font_size= self.width/15  
            self.tbutton3.disabled_color =.5, .5, .5, .5  
            self.tbutton4.disabled_color =.5, .5, .5, .5  
            
        # other basic settings  
        self.tbutton1.background_color = (255/255, 193/255, 193/255, .75)
        self.tbutton2.background_color = (255/255, 193/255, 193/255, .75)
        self.tbutton3.background_color = (255/255, 193/255, 193/255, .75)
        self.tbutton4.background_color = (255/255, 193/255, 193/255, .75)
        self.tbutton1.color = 205/255,55/255,0/255,.75 
        self.tbutton2.color = 138/255,43/255,226/255,1    
        self.tbutton3.color = 255/255,128/255,0/255,1  
        self.tbutton4.color = 84/255,139/255,84/255,1 
        self.tbutton1.state = "normal" 
        self.tbutton2.state = "normal" 
        self.tbutton3.state = "normal" 
        self.tbutton4.state = "normal"      
        self.tbutton1.disabled = False
        self.tbutton2.disabled = False
        self.tbutton3.disabled = False
        self.tbutton4.disabled = False

# Final page thanks
class FinalScreen(Screen):
    pass

# App
class QuizApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()    
        
        self.event_page = EventScreen()
        screen = Screen(name="Events")   
        screen.add_widget(self.event_page)
        self.screen_manager.add_widget(screen)
        
        self.final_page = FinalScreen()
        screen = Screen(name="Final")
        screen.add_widget(self.final_page)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager 

if __name__ == "__main__":
    app = QuizApp().run()
