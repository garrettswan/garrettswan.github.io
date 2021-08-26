import actr
import pandas as pd

# load model
actr.load_act_r_model("ACT-R:tutorial;unit2;demo2-model_schedule.lisp")

# setting some default lists
response = False
responses = []
times = []
event_times = []
event_type = []

# loading in the event list
df = pd.read_csv('event_list0.csv',names=["time","event"])

# function for recording mouse movement
def respond_to_key_press (model,key):
    global response, light1Color, light2Color, window, text1,text2,light1_obj, \
        light2_obj,gauge1_obj,gauge2_obj,temp1_y, responses,times

    response = key

    # specific responses for different key presses
    if (key=="a") and (light1Color=="black"):
        light1_on(window,text1,"exp")
        responses.append("a")
        times.append(actr.get_time()/1000)

    if (key=="b") and (light2Color=="red"):
        light2_on(window,text2,"exp")
        responses.append("b")
        times.append(actr.get_time()/1000)

    # eventually, these keys should modify the position of the gauges
    if (key=="c"):
        #temp1_y = 200
        #actr.remove_items_from_exp_window(window,gauge1_obj)
        #gauge1_obj = actr.add_text_to_exp_window(window, "C", x=60, y=200,color="black")
        responses.append("c")
        times.append(actr.get_time()/1000)

    if (key=="d"):
        #temp2_y = 200
        #actr.remove_items_from_exp_window(window,gauge2_obj)
        #gauge2_obj = actr.add_text_to_exp_window(window, "D", x=110, y=200,color="black")
        responses.append("d")
        times.append(actr.get_time()/1000)

# setting up the initial screen
def intialize_screen(window,text1,text2,text3,text4,gauge1_startx,gauge1_starty,
    gauge2_startx,gauge2_starty):

    global light1_obj,light2_obj,gauge1_obj,gauge2_obj

    light1_on(window,text1,"intial")
    light2_on(window,text2,"intial")

    gauge1_obj = actr.add_text_to_exp_window(window, text3, x=gauge1_startx, y=gauge1_starty, color="black")
    actr.add_line_to_exp_window(window,[gauge1_startx+10,150], [gauge1_startx+20,150], color = False)
    actr.add_line_to_exp_window(window,[gauge1_startx+10,250], [gauge1_startx+20,250], color = False)

    gauge2_obj = actr.add_text_to_exp_window(window, text4, x=gauge2_startx, y=gauge2_starty, color="black")
    actr.add_line_to_exp_window(window,[gauge2_startx+10,150], [gauge2_startx+20,150], color = False)
    actr.add_line_to_exp_window(window,[gauge2_startx+10,250], [gauge2_startx+20,250], color = False)

# the experiment function
def experiment(human=False):

    # I guess setting response to false globally
    global response, light1Color, light2Color, window, text1,text2,text3,text4, \
        light1_obj,light2_obj,gauge1_obj,temp1_y,gauge1_startx,gauge1_starty, \
        gauge2_startx,gauge2_startx

    # some default parameters
    # for lights
    text1 = "A"
    text2 = "B"
    light1Color = "green"
    light2Color = "black"
    light1_obj = None
    light2_obj = None

    # for gauges
    text3 = "C"
    text4 = "D"
    gauge1_startx = 60
    gauge1_starty = 200
    gauge2_startx = 110
    gauge2_starty = 200
    gauge1_rate = 2
    gauge2_rate = 2
    fps = 5

    actr.reset()

    window = actr.open_exp_window("hello world",width=400,height=400,x=400,y=400)

    # adding commands
    actr.add_command("demo2-key-press",respond_to_key_press,
                     "Demo2 task output-key monitor")
    actr.add_command("gauge_1_move",gauge_1_move)
    actr.add_command("gauge_2_move",gauge_2_move)
    actr.add_command("light1_off",light1_off)
    actr.add_command("light2_off",light2_off)
    actr.add_command("delayed_print_visicon",delayed_print_visicon)
    actr.add_command("move_y",move_y)

    # monitoring for key board
    actr.monitor_command("output-key","demo2-key-press")

    # putting the initial screen onto the window
    intialize_screen(window,text1,text2,text3,text4,gauge1_startx,gauge1_starty,
        gauge2_startx,gauge2_starty)


    response = False

    # human = participant. Good for testing
    if human == True:
        if actr.visible_virtuals_available():

            # puts time.sleep(0)
            # I guess it lets the program run
            # maybe will need to change in the future

            while response == False:
                actr.process_events()

    else:

        actr.install_device(window)

        light1 = 1
        light2 = 1

        time1 = 0
        count = 0
        for event in range(0,df.shape[0]):

            time1 = df["time"][event]
            count += 1


            if df["event"][event] == (" 'Green (First) Light Script-triggered Fault'") and light1==1:

                #actr.schedule_event(time1-.1,"delayed_print_visicon",params=[],maintenance=True)

                actr.schedule_event(time1, "light1_off",params=[window,text1,"exp"],maintenance=True)
                event_times.append(time1)
                event_type.append("light1_off")

                #actr.schedule_event(time1+.1,"delayed_print_visicon",params=[],maintenance=True)

            elif df["event"][event] == (" 'Red (Second) Light Script-triggered Fault'") and light2==1:

                actr.schedule_event(time1, "light2_off",params=[window,text2,"exp"],maintenance=True)
                event_times.append(time1)
                event_type.append("light2_off")


        # parameters for gauges
        temp1_y = gauge1_starty
        temp2_y = gauge2_starty
        time1 = 0
        first_time_exceeded_gauge1 = 0
        first_time_exceeded_gauge2 = 0
        gauges_on = 1

        #
        if gauges_on == 1:
            for event in range(0,round(df["time"][len(df["time"])-1]*fps)):

                time1 = time1 + (1/fps)

                temp1_y = temp1_y + gauge1_rate
                temp2_y = temp2_y + (gauge2_rate*-1)

                if temp1_y < 150 or temp1_y > 250:
                    gauge1_color = "red"
                    if first_time_exceeded_gauge1==0:
                        first_time_exceeded_gauge1 += 1

                        actr.schedule_event(time1,"delayed_print_visicon",params=[],maintenance=True)
                        actr.schedule_event(time1+.1,"delayed_print_visicon",params=[],maintenance=True)
                else:
                    gauge1_color = "black"
                    first_time_exceeded_gauge1=0

                if temp2_y < 150 or temp2_y > 250:
                    gauge2_color = "red"
                    if first_time_exceeded_gauge2==0:
                        first_time_exceeded_gauge2 += 1
                else:
                    gauge2_color = "black"
                    first_time_exceeded_gauge2=0


                if temp1_y < 125 or temp1_y > 275:
                    gauge1_rate = gauge1_rate * -1
                    if first_time_exceeded_gauge1==1:
                        event_times.append(time1)
                        event_type.append("gauge1_off")

                if temp2_y < 125 or temp2_y > 275:
                    gauge2_rate = gauge2_rate * -1
                    if first_time_exceeded_gauge2==1:
                        event_times.append(time1)
                        event_type.append("gauge2_off")

                #actr.schedule_event(time1-.1,"delayed_print_visicon",params=[],maintenance=True)

                actr.schedule_event(time1, "gauge_1_move",params=[window,text3,gauge1_startx,temp1_y,gauge1_color],maintenance=True)
                actr.schedule_event(time1, "gauge_2_move",params=[window,text4,gauge2_startx,temp2_y,gauge2_color],maintenance=True)

                #actr.schedule_event(time1+.1,"delayed_print_visicon",params=[],maintenance=True)


    #actr.run(df["time"][len(df["time"])-1])
    actr.run(15,True)


    # pause actr



    # removing commands and things
    actr.remove_command_monitor("output-key","demo2-key-press")
    actr.remove_command("gauge_1_move")
    actr.remove_command("gauge_2_move")
    actr.remove_command("light1_off")
    actr.remove_command("light2_off")
    actr.remove_command("move_y")

    # printing some things
    print("respones",responses)
    print("response_times",times)
    print("event_times",event_times)
    print("event_type",event_type)


def delayed_print_visicon():
    actr.print_visicon()

def move_y(gauge1_obj,gauge1_starty):

    global text3,gauge1_startx

    if gauge1_starty < 150 or gauge1_starty > 250:
        gauge1_starty += -5
    else:
        gauge1_starty += 5

    actr.modify_text_for_exp_window(gauge1_obj,text3,x=gauge1_startx,y=gauge1_starty,color='black')
    actr.schedule_event_relative (.05, "move_y",params=[gauge1_obj,gauge1_starty],maintenance=True)


##############################
## functions for Gauges ##
##############################

def gauge_1_move(window, letter, newx, newy,gauge1_color):

    global gauge1_obj

    #actr.remove_items_from_exp_window(window,gauge1_obj)
    #gauge1_obj = actr.add_text_to_exp_window(window, letter, x=newx, y=newy,color = gauge1_color)

    actr.modify_text_for_exp_window(gauge1_obj,letter, x=newx, y=newy,color = gauge1_color)

def gauge_2_move(window, letter, newx, newy,gauge2_color):

    global gauge2_obj

    #actr.remove_items_from_exp_window(window,gauge2_obj)
    #gauge2_obj = actr.add_text_to_exp_window(window, letter, x=newx, y=newy,color = gauge2_color)

    actr.modify_text_for_exp_window(gauge2_obj,letter, x=newx, y=newy,color = gauge2_color)

##############################
## functions for light task ##
##############################

def light1_on(window,text1,mode):
    global light1Color, light1_obj

    light1Color = "green"
    if light1_obj != None:
        actr.remove_items_from_exp_window(window,light1_obj)
    light1_obj = actr.add_text_to_exp_window(window, text1, x=125, y=100,color=light1Color)


def light1_off(window,text1,mode):
    global light1Color, light1_obj

    light1Color = "black"
    if light1_obj != None:
        actr.remove_items_from_exp_window(window,light1_obj)
    light1_obj = actr.add_text_to_exp_window(window, text1, x=125, y=100,color=light1Color)


def light2_on(window,text2,mode):
    global light2Color, light2_obj

    light2Color = "black"
    if light2_obj != None:
        actr.remove_items_from_exp_window(window,light2_obj)
    light2_obj = actr.add_text_to_exp_window(window, text2, x=175, y=100,color=light2Color)


def light2_off(window,text2,mode):
    global light2Color, light2_obj

    light2Color = "red"
    if light2_obj != None:
        actr.remove_items_from_exp_window(window,light2_obj)
    light2_obj = actr.add_text_to_exp_window(window, text2, x=175, y=100,color=light2Color)
