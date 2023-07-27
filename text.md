Hi guys,
We need to tweak our Python app to take the lead in terms of generating contents.

For now this is how the agent mode flow looks like:

1. User enters their objective.
2. The frontend creates a new session in the Python app.
3. The frontend then asks the Python app to ask questions to the user. This conversations goes on for 5 consecutive times. This questions count it handled in the frontend btw
4. After the questions are answered (without any page reload) the frontend now emits `get-tasks-list` with the `user_id` to the python app.
5. The python app now start to do its thing and emits `get-tasks-list` events to the frontend. It keeps emitting until the tasks list is fully sent to the frontend/fully generated.
6. As this is done the frontend now emits a `get-summarisation` event to the python app.
7. The python app now starts generating summary and keeps emitting them to the frontend until it finishes.
8. Now the frontend asks the user to either click `Yes` to continue or `No` to generate new set of tasks.
9. As the user continues the frontend emits `get-next-task` to the python app and the python app starts working on the first task and keeps sending chunks to the frontend.
10. the frontend keeps receiving the tasks and parses it based on the tokens it has `#start` `#end` `execution_start`.
11. Then the frontend makes ingest request to the node.js server to update the user’s objectives count.

This all is okay. Unless we take the following scenarios

1. What if the user logs in from a different browser and starts generating?
2. What if the internet connection fails i. During task generation & ii. Before the ingest request?
3. What if the user is not using a browser and using only a headless client (i.e. postman) to make the request how do you even know the user is authenticated in the python app?

Before we get to this scenarios, we need to understand that in our current flow the frontend app is the primary driver. And this is not a good solution. We need to make the Python app the driver and the one who commands the frontend app. Let me elaborate this.

1. The python app should emit events that tells the frontend to show or hide things from the ui
2. The python app should send the ingest request to the backend to decrease the objectives count and not the frontend app
3. The python app should finish the tasks execution event if the user disconnects in the middle of the generation. and after that save the info on the db so that when the user comes back they can get what the app has done for them.

The 3. will actually enable us to run the agent mode concurrently with our existing tools. We can even use the this to show in progress tasks in the user's activities dashboard.

So what we need is a complete refactor of how the python app works not the AGI but the peripherals around it.
