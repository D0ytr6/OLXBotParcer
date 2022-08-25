from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

#Making the main reply keyboard
Main_Keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
Cancel_Keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

button_make_request = KeyboardButton("/Make_request")
button_track = KeyboardButton("/Track_in_time")
button_my_tracks = KeyboardButton("/My_tracks")
button_history = KeyboardButton("/My_history")

Main_Keyboard.add(button_make_request)
Main_Keyboard.add(button_track).add(button_my_tracks)
Main_Keyboard.add(button_history)

button_cancel = KeyboardButton("/Cancel")
Cancel_Keyboard.add(button_cancel)