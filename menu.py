from launcher import launcher
from func import minus as FMINUS
import sys
class Menu:
    def __init__(self,buttons=None,background=None,checkboxes=None,clock=None,screen=None,terminal1=None,terminal2=None,particle_list=None,text_boxes=None):
        self.particle_list=particle_list
        self.buttons_displayed=[]
        self.check_boxs_displayed=[]
        self.background = background
        self.terminal1=terminal1;
        self.terminal2=terminal2;
        self.cb_a=checkboxes
        self.b_a=buttons    
        self.screen=screen
        self.menu_state="start"
        self.clock=clock;
        self.text_boxs_displayed=[]
        self.tb_a=[]
    def update(self, state,events):
        self._update_menu(state,events);

        # python has no switch - but would this be a good use for match? (I hear it's faster)
        if   self.menu_state=="start"               :self.start_menu(              state,events)
        elif self.menu_state=="settings"            :self.settings_menu(           state,events)
        elif self.menu_state=="mp_start"            :self.multiplayer_start_menu(  state,events)
        elif self.menu_state=="upnp_menu"           :self.upnp_menu(               state,events)
        elif self.menu_state=="single_player_lobby" :self.single_player_lobby_menu(state,events)
        elif self.menu_state=="lobby"               :self.lobby_menu(              state,events)
        elif self.meue_state=="mp_menu"             :self.mp_menu(                 state,events)
    def _update_basic_state(self,state,events):
        ##
        ##here goes the basic menu state updates regardless of screen
        ##
        ##check for exit
        for e in events:
            if state["exit"]==True or state["_app_ref"].QUIT==e.type:
                sys.exit()
        for x in self.particle_list:
            x.tick(self.screen,[0,0])

        #make mouse_pos current mouse pos    
        state["mouse_pos"]=state["get_mouse_pos"]()

    def start_menu(self,state):
        self.screen.blit(state["info"], [20,150])
        button_sp_menu = self.b_a[0]
        button_mp_menu = self.b_a[1]
        button_settings = self.b_a[2]
        button_quit_game = self.b_a[10]
        mouse_pos = state["mouse_pos"]
        s1 = button_sp_menu.tick(self.screen, mouse_pos, state["mouse_single_tick"], state["glitch"])
        s2= button_mp_menu.tick(self.screen, mouse_pos, state["mouse_single_tick"], state["glitch"])
        s3 = button_settings.tick(self.screen, mouse_pos, state["mouse_single_tick"], state["glitch"])
        button_quit_game.tick(self.screen, mouse_pos, state["mouse_single_tick"], state["glitch"])
        if s1 != None:
            self.menu_status = s1
            state["mouse_single_tick"] = False
        if s2 != None:
            self.menu_status  = s2
            state["mouse_single_tick"] = False
        if s3 != None:
            self.menu_status  = s3
            state["mouse_single_tick"] = False
    def settings_menu(self,state,events):
        button_client_quit = self.b_a[10]
        self.check_boxs_displayed=[
            self.cb_a[0],
            self.cb_a[1],
            self.cb_a[4],
            self.cb_a[3],
            self.cb_a[5]
            ]
        self.text_boxs_displayed=[self.tb_a[0]]
        mouse_pos = state["mouse_pos"]
        s8_2 = button_client_quit.tick(self.screen, mouse_pos, state["mouse_single_tick"], self["glitch"])

        text = self.terminal1.render("Name:", False, [255,255,255])
        self.screen.blit(text, [20,207])

        for tb in self.text_boxs_displayed:
            tb.tick(self.screen, state["mouse_single_tick"], mouse_pos, events)
        for cb in self.check_boxs_displayed:
            cb.render_checkbox()
        if s8_2 != None:
            self.menu_status  = s8_2
            state["mouse_single_tick"] = False
        for event in events:
            for cb in self.check_boxs_displayed:
                cb.update_checkbox(event,mouse_pos);

    def multiplayer_start_menu(self,state):
        button_host_game=self.b_a[3]
        button_join_game=self.b_a[4]
        button_back=self.b_a[13]
        buttonUpnp=self.b_a[6]
        mouse_pos = state["mouse_pos"]
        s4, net1, host = button_host_game.tick(self.screen, mouse_pos, state["mouse_single_tick"], self.glitch)
        list  = button_join_game.tick(self.screen, mouse_pos, state["mouse_single_tick"], self.glitch, arg = state["appIP"])
        if list != None:
            s5, net2, a1 = list
        else:
            s5 = None
            net2 = None
            a1 = None

        s6 = button_back.tick(self.screen, mouse_pos, state["mouse_single_tick"], self.glitch)
        if state["_app_ref"].dev:
            sButtonUpnp = buttonUpnp.tick(self.screen, mouse_pos, state["mouse_single_tick"], self.glitch)
            print(f"sButtonUpnp:{sButtonUpnp}")
        else:
            sButtonUpnp = None

        if state["net"] == None and net1 != None:
            state["net"] = net1
            print("NETWORK SAVED")
        if state["net"] == None and net2 != None:
            state["net"] = net2
            print("NETWORK SAVED")
        if s4 != None:
            self.menu_status  = s4
            print("Game hosted")
            state["mouse_single_tick"] = False
        if s5 != None:
            button_join_game.__dict__["args"] = state["appIP"]
            self.menu_status  = s5
            state["mouse_single_tick"] = False
        if s6 != None:
            self.menu_status  = s6
            state["mouse_single_tick"] = False
        if sButtonUpnp != None:
            self.menu_status  = sButtonUpnp
            print(f'--------------menu status:{self.menu_status}')
            state["mouse_single_tick"] = False

    def upnp_menu(self,state):
        print('tst2')
        buttonUpnpTest=self.b_a[11]
        buttonUpnpBack=self.b_a[12]
        text = self.terminal1.render("This is a STUB menu - more to come.", False, [255,255,255])
        self.screen.blit(text, [430- text.get_rect().size[0]/2,20])
        text = self.terminal1.render("{button to enter here only visible with dev tools enabled}", False, [255,255,255])
        self.screen.blit(text, [430- text.get_rect().size[0]/2,80])
        mouse_pos = state["mouse_pos"]
        sButtonUpnpTest = buttonUpnpTest.tick(self.screen, mouse_pos, mouse_single_tick, self.glitch)
        if sButtonUpnpTest != None:
            print('stub ... exiting game here by design...')
            state["exit"]=True;
        sButtonUpnpBack = buttonUpnpBack.tick(self.screen, mouse_pos, mouse_single_tick, self.glitch)
        if sButtonUpnpBack != None:
            menu_status  = sButtonUpnpBack
            mouse_single_tick = False
    def single_player_lobby_menu(self,state):pass
    def multiplayer_menu(self,state):pass 
    def lobby_menu(self,state):

        button_host_quit=self.b_a[9]
        button_start_sp=self.b_a[7]
        text = self.terminal1.render("MAP", False, [255,255,255])
        self.screen.blit(text, [430- text.get_rect().size[0]/2,20])

        rect_map = state["maps_dict"][selected_map]["image"].get_rect()


        if state["host"]:
            text = self.terminal1.render("LOBBY (HOSTING)", False, [255,255,255])
            self.screen.blit(text, [30,20])
            text = self.terminal1.render("HOSTED AT:" + state["ip"], False, [255,255,255])
            self.screen.blit(text, [500,420])

            if rect_map.collidepoint(FMINUS(state["mouse_pos"],[330,80],"-")):

                if state["mouse_single_tick"]:
                    selected_map += 1

                    state["click_sound"].play()

                    if selected_map == len(state["maps_dict"]):
                        selected_map = 0

                rect_map = state["maps_dict"][selected_map]["image"].get_rect()

                rect_map.inflate_ip(4,4)

                state["draw"].rect(self.screen, [255,255,255], rect_map.move([330,80]))
        else:
            text = self.terminal1.render("LOBBY", False, [255,255,255])
            self.screen.blit(text, [30,20])
            text = self.terminal1.render("HOSTED AT:" + state["appIP"], False, [255,255,255])
            self.screen.blit(text, [500,420])
        #screen.blit(text, [400,20])

        self.screen.blit(state["maps_dict"][selected_map]["image"], [330,80])


        text = self.terminal1.render(state["maps_dict"][selected_map]["map"].__dict__["name"], False, [255,255,255])
        self.screen.blit(text, [430- text.get_rect().size[0]/2,50])

        rect_map2 = state["maps_dict"][selected_map]["image"].get_rect()

        text = self.terminal1.render(state["maps_dict"][selected_map]["map"].__dict__["name"], False, [255,255,255])
        self.screen.blit(text, [430- text.get_rect().size[0]/2,50])

        state["draw"].line(self.screen, [255,255,255], [550, 80], [550, 80 + rect_map2.h])
        state["draw"].line(self.screen, [255,255,255], [550, 80], [545, 80])
        state["draw"].line(self.screen, [255,255,255], [550, 80 + rect_map2.h], [545, 80 + rect_map2.h])

        text = self.terminal.render(str(round(state["maps_dict"][selected_map]["map"].__dict__["size"][1]/100)) + "m", False, [255,255,255])
        self.screen.blit(text, [552,80 + rect_map2.h/2 - text.get_rect().size[1]/2])

        state["draw"].line(self.screen, [255,255,255], [330, 100 + rect_map2.h], [530, 100 + rect_map2.h])
        state["draw"].line(self.screen, [255,255,255], [330, 100 + rect_map2.h], [330, 95 + rect_map2.h])
        state["draw"].line(self.screen, [255,255,255], [530, 100 + rect_map2.h], [530, 95 + rect_map2.h])

        text = self.terminal1.render(str(round(state["maps_dict"][selected_map]["map"].__dict__["size"][0]/100)) + "m", False, [255,255,255])
        self.screen.blit(text, [430- text.get_rect().size[0]/2,105 + rect_map2.h])

        text = self.terminal1.render("Players:", False, [255,255,255])

        self.screen.blit(text, [20,200])

        if state["host"]:
            reply = state["net"].send("index:" + str(selected_map))
        else:
            reply = state["net"].send("un")


        if reply == "KILL":
            self.menu_status = "start"

        if reply == "start_game/":
            print("STARTING GAME")
            launcher.start_multiplayer_client()

        else:
            try:
                reply2 = reply.split("#END")[0]
                data = reply2.split("\n")
                for line in data:
                    type, info1 = line.split(":")
                    if type == "players":
                        players = info1.split("/")
                    elif type == "index" and not state["host"]:
                        selected_map = int(info1)

            except Exception as e:
                pass

        i = 210
        for y in players:
            if y == "" or y == "clients":
                continue
            i += 20
            text = self.terminal1.render(y, False, [255,255,255])
            self.screen.blit(text, [30,i])
        if state["host"]:
            button_start_sp.tick(self.screen, state["mouse_pos"], state["mouse_single_tick"], self.glitch cbx=True)
        s8 = button_host_quit.tick(self.screen, state["mouse_pos"], state["mouse_single_tick"], self.glitch)
        if s8 != None:
            self.menu_status  = s8
    def get_state(self,state):
        return self.menu_state