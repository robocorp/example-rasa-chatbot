# Rasa chatbot with two-way integration to Robocorp digital workers

This is an example how to set your [Rasa](https://rasa.com/) chatbot up to be able to trigger the execution of [Robocorp](https://robocorp.com/) digital workers (aka robots) through Control Room, and how the robot is able to return it's results back to the conversation. This example pairs with the [robot repo](https://github.com/robocorp/example-rasa-robot).

### Further reading

These resources from Rasa were found to be very helpful during the development of the ecxample:
- https://github.com/RasaHQ/rasa/blob/main/examples/reminderbot/README.md
- https://rasa.com/docs/rasa/custom-actions/
- https://rasa.com/docs/rasa/reaching-out-to-user/

Need to have custom actions server running first: `rasa run actions`
Then run `rasa shell` on other terminal.

The sequence that always triggers the bot is:
- hi
- what time is it
