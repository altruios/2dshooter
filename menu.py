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
        self._update_menu(state);

        # python has no switch - but would this be a good use for match? (I hear it's faster)
        if   self.menu_state=="start"               :self.start_menu(              state,events)
        elif self.menu_state=="settings"            :self.settings_menu(           state,events)
        elif self.menu_state=="mp_start"            :self.multiplayer_start_menu(  state,events)
        elif self.menu_state=="upnp_menu"           :self.upnp_menu(               state,events)
        elif self.menu_state=="single_player_lobby" :self.single_player_lobby_menu(state,events)
        elif self.menu_state=="lobby"               :self.lobby_menu(              state,events)
        elif self.meue_state=="mp_menu"             :self.mp_menu(                 state,events)
    def _update_basic_state(self,state):
        ##
        ##here goes the basic menu state updates regardless of screen
        ##
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
        mouse_pos = state["get_mouse_pos"]()
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
        mouse_pos = state["get_mouse_pos"]()
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
        pass
    def upnp_menu(self,state):pass
    def single_player_lobby_menu(self,state):pass
    def lobby_menu(self,state):pass
    def multiplayer_menu(self,state):pass
    def get_state(self,state):
        return self.menu_state