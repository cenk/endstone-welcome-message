## endstone-welcome-message 

A simple Endstone plugin that allows you to send players a welcome message via chat, tip, toast, title, popup or form when they join the server.

### Message types
#### 1 - Chat message:
<img width="570" height="152" alt="chat" src="https://github.com/user-attachments/assets/06e80480-0e4a-4cba-90f7-bab561ecf356" />

#### 2 - Tip message:
<img width="754" height="84" alt="tip" src="https://github.com/user-attachments/assets/7b8c4a09-625a-4cba-9fe7-7cc39e92cc70" />

#### 3 - Popup message:
<img width="382" height="131" alt="popup" src="https://github.com/user-attachments/assets/fb04c737-584a-4d4b-8c24-ee1da29edda9" />

#### 4 - Toast message:
<img width="841" height="123" alt="toast" src="https://github.com/user-attachments/assets/c6074f6f-6559-4e3f-adbf-ae52be206d10" />

#### 5 - Title message:
<img width="1595" height="550" alt="title" src="https://github.com/user-attachments/assets/ea257934-d1a7-4e3f-ad9c-38effb958700" />

#### 6 - Form message:
<img width="455" height="407" alt="form" src="https://github.com/user-attachments/assets/6198471b-82b1-4888-8bda-13af17a5d458" />

### Config file options
#### ```type```
Welcome message type.

Valid values are between 0 and 6.
| Value | Description |
| --- | --- |
| 0 | Disables welcome message |
| 1 | Chat message |
| 2 | Tip message |
| 3 | Popup message |
| 4 | Toast message |
| 5 | Title message |
| 6 | Form message |

Example:
```toml
type = 1
```

#### ```header```
Toast, Title or Form message header

Effective only when type is 4 (Toast), 5 (Title) or 6 (Form).

You can use ```§``` style Minecraft color codes and ```{}``` style placeholders like: ```{player_name}```, ```{player_ping}```

Example:
```toml
header = "§u§lWelcome §s{player_name}"
```

#### ```body```
Welcome message body

You can use ```§``` style Minecraft color codes and ```{}``` style placeholders like: ```{player_name}```, ```{player_ping}```

You can use newlines within the welcome message body.
To do this, you can use ```\n``` within a single line or break lines using triple quotes.

Note that the Toast message type does not support newlines.

Example:
```toml
body = "§3Hello §6{player_name}§3. Welcome to our Minecraft Server."
```

Example with multiline 1:
```toml
body = "This is a\n multiline welcome message"
```

Example with multiline 2:
```toml
body = """This is a
multiline welcome message"""
```

#### ```form_button_text```
Form Button text

Effective only when type is 6 (Form)

Example:
```toml
form_button_text = "OK"
```

#### ```wait_before```
Wait before the welcome message is displayed (in seconds).

Valid values are between 0 and 5.

0 disables waiting.
```toml
wait_before = 0 
```

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
