import get_preferences
import sys
class Launcher:
    def __init__(self,state,game):
        self.state=state;
        self.game=game;

    def start_mp_game(self,arg):
        reply = self.state["net"].send("start_game")
        self.start_multiplayer_client()

    def host_game(self,arg) :
        print("HOSTING GAME")
        self.state["appIP"] = self.state["ip"] 
        try:
            self.start_new_thread(self.state["_app_ref"].lobby_host, ("1", self.state["appIP"]) )
            return self.join_game(self.state["appIP"], True)
        except:
            return "start", None, None

    def upnp_menu(self,arg):
        if self.state["_app_ref"].dev:
            print('test')
            return('upnp_menu')
    def upnp_test(self,arg):
        if self.state["_app_ref"].dev:
            print('upnp_test')
            return('upnp_test')

    def start_multiplayer_client(self):
        self.game.main(
        self.state["_app_ref"], 
        multiplayer = True, 
        net = self.state["net"], 
        players = self.state["players"], 
        self_name = self.state["_app_ref"].name, 
        map = self.state["maps_dict"][self.state["selected_map"]]["map"], 
        full_screen_mode = self.state["full_screen_mode"])


    def join_game(self,arg, host = False):

        print("JOINING TO:", arg)

        try:
            self.state["net"] = Network(arg)

            print("CLIENT: STARTING SEARCH")

            reply = self.state["net"].send(self.state["_app_ref"].name)
            if reply != [""]:

                print("CLIENT:", reply)
                print("CLIENT: CONNECTED")

                return "lobby", self.state["net"], host
            else:
                print("CLIENT: No connection found")
                return "start", None, None
        except Exception as e:
            print("CLIENT: Connection failed")
            print(e)
            return "start", None, None

    def main_menu(self,arg):
        app = self.state["_app_ref"]
        get_preferences.write_prefs(app.name, app.draw_los, app.dev, app.fs,
          app.ultraviolence, app.ip)
        return "start"


    def quit(self,args):
        app = self.state["_app_ref"]
        get_preferences.write_prefs(app.name, app.draw_los, app.dev, app.fs,
          app.ultraviolence, app.ip)

        sys.exit()

    def start_sp(self,arg cbx=False):
        print("SPa")
        app = self.state["_app_ref"]
        get_preferences.write_prefs(app.name, app.draw_los, app.dev, app.fs,
          app.ultraviolence, app.ip)
        args = (
            app,
            app.name,
            arg,
            app.draw_los,
            app.dev,
            cbx,
            self.state["maps_dict"][self.state["selected_map"]]["map"],
            self.state["full_screen_mode"])

        app.start_sp(args)

    def start_mp(arg):
        return "mp_start"

    def settings(arg):
        return "settings"

    def kill_server(arg):
        reply = net.send("kill")
        return "start"

    def sp_lob(arg):
        return "single_player_lobby"

