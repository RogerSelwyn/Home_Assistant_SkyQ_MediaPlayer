ROOT = "/home/homeassistant/.homeassistant/"

class SwitchMaker:

    def __init__(self, name, room, conf_folder):
        self._name = name
        self._room = room
        ROOT = conf_folder
        self._f= open(ROOT + "skyq" + self._room.replace(" ","") + ".yaml","w+")
        self._f.write("    skyq_pause" + self._room.replace(" ","").lower() + ":\n" + 
                "      value_template: '{{\"off\"}}'\n" + 
                "      friendly_name: 'pause in the " + self._room + "'\n" + 
                "      turn_on:\n" + 
                "        service: media_player.media_pause\n" + 
                "        data:\n" + 
                "          entity_id: media_player." + self._name.replace(" ","_").lower() + "\n" +
                "      turn_off:\n" + 
                "        service: script.placeholder\n")
        self._f.write("    skyq_play" + self._room.replace(" ","").lower() + ":\n" + 
                "      value_template: '{{\"off\"}}'\n" + 
                "      friendly_name: 'play in the " + self._room + "'\n" + 
                "      turn_on:\n" + 
                "        service: media_player.media_play\n" + 
                "        data:\n" + 
                "          entity_id: media_player." + self._name.replace(" ","_").lower() + "\n" +
                "      turn_off:\n" + 
                "        service: script.placeholder\n")
        self._f.write("    skyq_ff" + self._room.replace(" ","").lower() + ":\n" + 
                "      value_template: '{{\"off\"}}'\n" + 
                "      friendly_name: 'fastforward in the " + self._room + "'\n" + 
                "      turn_on:\n" + 
                "        service: media_player.media_next_track\n" + 
                "        data:\n" + 
                "          entity_id: media_player." + self._name.replace(" ","_").lower() + "\n" +
                "      turn_off:\n" + 
                "        service: script.placeholder\n")
        self._f.write("    skyq_rw" + self._room.replace(" ","").lower() + ":\n" + 
                "      value_template: '{{\"off\"}}'\n" + 
                "      friendly_name: 'rewind in the " + self._room + "'\n" + 
                "      turn_on:\n" + 
                "        service: media_player.media_previous_track\n" + 
                "        data:\n" + 
                "          entity_id: media_player." + self._name.replace(" ","_").lower() + "\n" +
                "      turn_off:\n" + 
                "        service: script.placeholder\n")
        
    def addChannel(self, channel):
        self._f.write("    skyq_" + channel.replace(" ","").lower() + self._room.replace(" ","").lower() + ":\n" + 
                "      value_template: '{{\"off\"}}'\n" + 
                "      friendly_name: '"+ channel + " in the " + self._room + "'\n" + 
                "      turn_on:\n" + 
                "        service: media_player.select_source\n" + 
                "        data:\n" + 
                "          entity_id: media_player." + self._name.replace(" ","_").lower() + "\n" +
                "          source: '" + channel + "'\n" +  
                "      turn_off:\n" + 
                "        service: script.placeholder\n")
    def closeFile(self):
        self._f.close()
           
