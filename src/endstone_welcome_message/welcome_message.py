from endstone.plugin import Plugin
from endstone.event import event_handler, PlayerJoinEvent
from endstone.form import ModalForm, Label
from enum import IntEnum
import string


class SafeFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        return kwargs.get(key, f"<unknown:{key}>")


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

        cfg = self.config["welcome_message"]
        self.msg_type = MessageType(max(0, min(int(cfg["type"]), 6)))

        if self.msg_type != MessageType.DISABLED:
            self.msg_header = str(cfg["header"])
            self.msg_body = str(cfg["body"])
            self.btn_text = str(cfg["form_button_text"])
            self.wait_secs = max(0, min(int(cfg["wait_before"]), 5))
        else:
            self.logger.info("Welcome Message is disabled in the config file.")

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        if self.msg_type == MessageType.DISABLED:
            return

        if self.wait_secs > 0:
            wait_ticks = self.wait_secs * 20
            task = self._task(event.player)
            self.server.scheduler.run_task(self, task, delay=wait_ticks)
        else:
            self._show_msg(event.player)

    def _task(self, p):
        def run():
            self._show_msg(p)
        return run

    def _show_msg(self, p):
        header, body = self._fill_placeholders(p)

        match self.msg_type:
            case MessageType.CHAT:
                p.send_message(body)
            case MessageType.TIP:
                p.send_tip(body)
            case MessageType.POPUP:
                p.send_popup(body)
            case MessageType.TOAST:
                p.send_toast(header, body)
            case MessageType.TITLE:
                p.send_title(header, body)
            case MessageType.FORM:
                form = ModalForm(
                    title=header,
                    controls=[Label(text=body + "\n\n")],
                    submit_button=self.btn_text
                )
                p.send_form(form)

    def _fill_placeholders(self, p):
        s = self.server

        values = {
            'player_name': p.name,
            'player_locale': p.locale,
            'player_device_os': p.device_os,
            'player_device_id': p.device_id,
            'player_hostname': p.address.hostname,
            'player_port': p.address.port,
            'player_game_mode': p.game_mode.name.capitalize(),
            'player_game_version': p.game_version,
            'player_exp_level': p.exp_level,
            'player_total_exp': p.total_exp,
            'player_exp_progress': f"{p.exp_progress:.2f}",
            'player_ping': p.ping,
            'player_dimension_name': p.location.dimension.type.name.replace("_", " ").title(),
            'player_dimension_id': p.location.dimension.type.value,
            'player_coordinate_x': int(p.location.x),
            'player_coordinate_y': int(p.location.y),
            'player_coordinate_z': int(p.location.z),
            'player_xuid': p.xuid,
            'player_uuid': p.unique_id,
            'player_health': p.health,
            'player_max_health': p.max_health,
            'server_level_name': s.level.name.replace("_", " ").title(),
            'server_max_players': s.max_players,
            'server_online_players': len(s.online_players),
            'server_start_time': s.start_time.strftime('%d %b %Y %H:%M:%S'),
            'server_locale': s.language.locale,
            'server_endstone_version': s.version,
            'server_minecraft_version': s.minecraft_version,
            'server_port': s.port,
            'server_port_v6': s.port_v6
        }

        formatter = SafeFormatter()
        return formatter.format(self.msg_header, **values), formatter.format(self.msg_body, **values)
