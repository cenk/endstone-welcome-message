from endstone.plugin import Plugin
from endstone.event import event_handler, PlayerJoinEvent
from endstone.form import ModalForm, Label
from enum import IntEnum


class MessageType(IntEnum):
    DISABLED = 0
    CHAT = 1
    TIP = 2
    POPUP = 3
    TOAST = 4
    TITLE = 5
    FORM = 6


class WelcomeMessage(Plugin):
    api_version = "0.6"

    def on_enable(self) -> None:
        self.save_default_config()
        self.register_events(self)

        config = self.config["welcome_message"]
        self.welcome_message_type = MessageType(
            max(0, min(int(config["type"]), 6))
        )

        if self.welcome_message_type != MessageType.DISABLED:
            self.welcome_message_header = str(config["header"])
            self.welcome_message_body = str(config["body"])
            self.welcome_message_form_button_text = str(config["form_button_text"])
            self.welcome_message_wait_before = max(0, min(int(config["wait_before"]), 5))
        else:
            self.logger.info("Welcome Message is disabled in the config file.")

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        if self.welcome_message_type == MessageType.DISABLED:
            return

        if self.welcome_message_wait_before > 0:
            wait_ticks = self.welcome_message_wait_before * 20
            task = self.make_delayed_task(event.player)
            self.server.scheduler.run_task(self, task, delay=wait_ticks)
        else:
            self.show_message(event.player)

    def make_delayed_task(self, player):
        def task():
            self.show_message(player)
        return task

    def show_message(self, player):
        header, body = self.replace_placeholders(player)

        match self.welcome_message_type:
            case MessageType.CHAT:
                player.send_message(body)
            case MessageType.TIP:
                player.send_tip(body)
            case MessageType.POPUP:
                player.send_popup(body)
            case MessageType.TOAST:
                player.send_toast(header, body)
            case MessageType.TITLE:
                player.send_title(header, body)
            case MessageType.FORM:
                form = ModalForm(
                    title=header,
                    controls=[Label(text=body + "\n\n")],
                    submit_button=self.welcome_message_form_button_text
                )
                player.send_form(form)

    def replace_placeholders(self, player):
        placeholder = {
            'player_name': player.name,
            'player_locale': player.locale,
            'player_device_os': player.device_os,
            'player_device_id': player.device_id,
            'player_hostname': player.address.hostname,
            'player_port': player.address.port,
            'player_game_mode': player.game_mode.name.capitalize(),
            'player_game_version': player.game_version,
            'player_exp_level': player.exp_level,
            'player_total_exp': player.total_exp,
            'player_exp_progress': f"{player.exp_progress:.2f}",
            'player_ping': player.ping,
            'player_dimension_name': player.location.dimension.type.name.replace("_", " ").title(),
            'player_dimension_id': player.location.dimension.type.value,
            'player_coordinate_x': int(player.location.x),
            'player_coordinate_y': int(player.location.y),
            'player_coordinate_z': int(player.location.z),
            'player_xuid': player.xuid,
            'player_uuid': player.unique_id,
            'player_health': player.health,
            'player_max_health': player.max_health,
            'server_level_name': self.server.level.name.replace("_", " ").title(),
            'server_max_players': self.server.max_players,
            'server_online_players': len(self.server.online_players),
            'server_start_time': self.server.start_time.strftime('%d %b %Y %H:%M:%S'),
            'server_locale': self.server.language.locale,
            'server_endstone_version': self.server.version,
            'server_minecraft_version': self.server.minecraft_version,
            'server_port': self.server.port,
            'server_port_v6': self.server.port_v6
        }

        replaced_header = self.welcome_message_header.format(**placeholder)
        replaced_body = self.welcome_message_body.format(**placeholder)

        return replaced_header, replaced_body
