# Name of all iRulez topics
iRulezTopic = 'iRulezIO16'

# Name of an relative action topic
# Used to send relative updates to output pins to the relative convertor
relativeTopic = 'relative'

# Name of an action topic
# Used when an action is sent to an arduino. This action contains the absolute need-to-be state of all pins.
# Also used generically for actions
actionTopic = 'action'

# Name of a status topic
# Arduinos will sent their current output pin states when they change.
statusTopic = 'status'

# Name of a button topic
# Arduinos will sent their current input pin states when they change.
buttonTopic = 'button'

# Topic that gets fired when a longdown timer has fired
buttonTimerFiredTopic = 'buttonTimerFired'

# Topic that gets fired when the timer of a multiclick button has fired
buttonMulticlickFiredTopic = 'buttonMulticlickFired'

# Name of the virtual_IO_board
virtual_IO_board_name = 'virtual_IO_Board'
virtual_IO_board_buttons = 20
virtual_IO_board_outputs = 20

# Name of the virtual_dimmer_board
virtual_dimmer_board_name = 'virtual_dimmer_Board'
virtual_dimmer_board_buttons = 20
virtual_dimmer_board_outputs = 20

# Name of  the notification topics
notificationTopic = 'notification'

# Name of  the notification topics for mail
mailTopic = 'mail'

# Name of  the notification topics for telegramTopic
telegramTopic = 'telegram'

# Name of action topic with timer
# Used to sent commands to the timer module.
timerTopic = 'timer'

# Name of the dimmer topic, used by arduino to sent dimmer output status updates.
dimmerStatusTopic = 'dimmerStatus'

# Name of the action topic for a dimmer
# Used to send commands to the dimmer module.
dimmerModuleTopic = 'dimmerModule'

# Used by the timer module to sent action commands to the dimmer module.
dimmerTimerFired = 'dimmerTimerFired'

# Used by button to notify the dimmer module a dimmer action should be cancelled.
dimmerCancelled = 'dimmerCancelled'

# Used to send commands to an arduino to change a dimmer value.
dimAction = 'dimAction'

# Used to send last_light_value updates to the output_status service.
dimLastLightValue = 'dimLastLightValue'

# The amount of message need to be sent every second when dimming.
dim_frequency_per_sec = 5

# dimmer directions
dim_direction_up = 'up'
dim_direction_down = 'down'
