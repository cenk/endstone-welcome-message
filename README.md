# endstone-welcome-message

A simple plugin for **Endstone** that sends a welcome message to players when they join. The message can be shown in **chat**, **tip**, **popup**, **toast**, **title**, or **form** format.

## Message types
### 1 - Chat message:
<img width="570" height="152" alt="chat" src="https://github.com/user-attachments/assets/06e80480-0e4a-4cba-90f7-bab561ecf356" />

### 2 - Tip message:
<img width="754" height="84" alt="tip" src="https://github.com/user-attachments/assets/7b8c4a09-625a-4cba-9fe7-7cc39e92cc70" />

### 3 - Popup message:
<img width="382" height="131" alt="popup" src="https://github.com/user-attachments/assets/fb04c737-584a-4d4b-8c24-ee1da29edda9" />

### 4 - Toast message:
<img width="841" height="123" alt="toast" src="https://github.com/user-attachments/assets/c6074f6f-6559-4e3f-adbf-ae52be206d10" />

### 5 - Title message:
<img width="1595" height="550" alt="title" src="https://github.com/user-attachments/assets/ea257934-d1a7-4e3f-ad9c-38effb958700" />

### 6 - Form message:
<img width="455" height="407" alt="form" src="https://github.com/user-attachments/assets/6198471b-82b1-4888-8bda-13af17a5d458" />

---

## Available Commands

All configuration is done via in-game commands:

### `/wmset <key> <value>`
Used to update specific configuration options for the welcome message.

- `/wmset type <value>`
  Sets the message type. Valid values: `chat`, `tip`, `popup`, `toast`, `title`, `form`
- `/wmset header <value>`
  Sets the message header. Supports placeholders and Minecraft color codes. Only used for `toast`, `title`, and `form` types.
- `/wmset body <value>`
  Sets the message body. Supports placeholders and Minecraft color codes. Use `\n` for new lines.
- `/wmset button <value>`
  Sets the button text. Only used for form type.
- `/wmset wait <0-5>`
  Delays message for 0–5 seconds after player joins.

### `/wmopts`
Displays the current configuration for the welcome message.

- `/wmopts`

### `/wmtest [value]`
Used to manually preview the welcome message for testing before enabling it server-wide.

- `/wmtest`
  Sends a test message using the currently active type.
- `/wmtest [value]`
  Sends a test message using the specified type. (`chat`, `tip`, `popup`, `toast`, `title`, `form`)

### `/wmenable`
Enables the welcome message system with the current configuration options.

### `/wmdisable`
Disables the welcome message system.

---

### Placeholders
You can use the following placeholders in your welcome message. 
| Placeholder | Description |
| --- | --- |
| {player_name} | Player's name |
| {player_locale} | Player's current locale |
| {player_device_os} | Player's operation system |
| {player_device_id} | Player's current device id |
| {player_hostname} | Player's hostname |
| {player_port} | Player's port number |
| {player_game_mode} | Player's current game mode |
| {player_game_version} | Player's current game version |
| {player_exp_level} | Player's current experience level |
| {player_total_exp} | Player's total experience points |
| {player_exp_progress} | Player's current experience progress towards the next level |
| {player_ping} | Player's average ping |
| {player_dimension_name} | Player's current dimension name |
| {player_dimension_id} | Player's current dimension id |
| {player_coordinate_x} | Player's current x coordinate |
| {player_coordinate_y} | Player's current y coordinate |
| {player_coordinate_z} | Player's current z coordinate |
| {player_health} | Player's health |
| {player_max_health} | Player's max health |
| {player_xuid} | Player's XUID |
| {player_uuid} | Player's UUID |
| {server_level_name} | Server's level name |
| {server_max_players} | The maximum amount of player's which can login to this server |
| {server_online_players} | Current online players count |
| {server_start_time} | Start time of the server |
| {server_locale} | Server's current locale |
| {server_endstone_version} | Server's Endstone version |
| {server_minecraft_version} | Server's Minecraft version |
| {server_port} | Server's IPv4 port |
| {server_port_v6} | Server's IPv6 port |

---

## Installation
1. Download the latest `.whl` file from [GitHub Releases](https://github.com/cenk/endstone-welcome-message/releases) and place it into your `plugins/` folder.
2. Restart or reload the server.
