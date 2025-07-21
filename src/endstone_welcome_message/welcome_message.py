from endstone.plugin import Plugin
from endstone.event import event_handler, PlayerJoinEvent
from endstone.form import ModalForm, Label
import time

class WelcomeMessage(Plugin):
    api_version = "0.6"

    def on_enable(self) -> None:
        self.save_default_config()
        self.register_events(self)
        self.welcome_message_type = max(0, min(int(self.config["welcome_message"]["type"]), 6))

        if self.welcome_message_type > 0:
            self.welcome_message_header = str(self.config["welcome_message"]["header"])
            self.welcome_message_body = str(self.config["welcome_message"]["body"])
            self.welcome_message_form_button_text = str(self.config["welcome_message"]["form_button_text"])
            self.welcome_message_wait_before = max(0, min(int(self.config["welcome_message"]["wait_before"]), 5))
        else:
            self.logger.info("Welcome Message is disabled in the config file!")

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        if self.welcome_message_type > 0:
            self.replace_placeholders(event.player)
            if self.welcome_message_wait_before > 0:
                time.sleep(self.welcome_message_wait_before)
            match self.welcome_message_type:
                case 1:
                    event.player.send_message(self.welcome_message_body)
                case 2:
                    event.player.send_tip(self.welcome_message_body)
                case 3:
                    event.player.send_popup(self.welcome_message_body)
                case 4:
                    event.player.send_toast(self.welcome_message_header, self.welcome_message_body)
                case 5:
                    event.player.send_title(self.welcome_message_header, self.welcome_message_body)
                case 6:
                    welcome_form = ModalForm(
                        title = self.welcome_message_header,
                        controls = [Label(text=self.welcome_message_body + '\n\n')],
                        submit_button = self.welcome_message_form_button_text
                    )
                    event.player.send_form(welcome_form)

    def replace_placeholders(self, player) -> None:
        placeholder = {
            'player_name': player.name,
            'player_locale': player.locale,
            'player_device_os': player.device_os,
            'player_device_id': player.device_id,
            'player_hostname': player.address.hostname,
            'player_port': player.address.port,
            'player_game_mode': player.game_mode.name,
            'player_game_version': player.game_version,
            'player_exp_level': player.exp_level,
            'player_total_exp': player.total_exp,
            'player_exp_progress': player.exp_progress,
            'player_ping': player.ping,
            'server_level_name': self.server.level.name,
            'server_max_players': self.server.max_players,
            'server_online_players': len(self.server.online_players),
            'server_start_time': self.server.start_time,
            'server_locale': self.server.language.locale,
            'server_endstone_version': self.server.version,
            'server_minecraft_version': self.server.minecraft_version,
            'server_port': self.server.port,
            'server_port_v6': self.server.port_v6
            # requires 'latest' api
            #'server_protocol_version': self.server.protocol_version
        }
        self.welcome_message_header = self.welcome_message_header.format(**placeholder)
        self.welcome_message_body = self.welcome_message_body.format(**placeholder)
