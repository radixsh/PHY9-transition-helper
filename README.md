# Physics 9 transition helper 
This Discord bot was built for the UC Davis Physics 9 Discord server to automate
repetitive admin work done at the end of every quarter, such as archiving the
old channels that used to correspond with a particular professor's class.

Slash commands have been implemented.


# Server Transition Instructions
The main requirement for server transition (other than creating the new
quarter's channels) is that we preserve the previous quarter's channels in case
of academic misconduct concerns, as anything arising at the end of a quarter can
take some time to process. This means that we delete channels on a one
quarter delay. For example, the transition to Spring 2023 would
involve deleting the (archived) Fall 2022 channels, archiving the Winter 2023
channels, and creating new Spring 2023 channels.


## Server Transition Checklist
This checklist was last updated 7 January 2024.

1. Send a message in the announcements channel saying that we are currently in
   the process of transitioning the server for the next quarter. This message
   should contain a note that course specific channels and course selection
   might be unavailable until this process is complete.
2. Edit the permissions for the "Sorting/Selection" category to remove the
   "Student" role's access. This prevents people from randomly reacting as you
   make the changes, which makes things a bit easier to keep track of and also
   means you don't have to worry about leaving someone with an invalid role
   configuration.
3. Perform the **Bot Commands** checklist below.
4. Perform the **Reaction Role Updates** checklist below.
5. Draft a message saying the transition is complete. We basically have a
   template for this, so just grab a previous message and update the term.
   Getting another mod to proofread this is a good idea, but they've certainly
   been sent out without such luxuries at 3am before.
6. Update permissions for the "Sorting/Selection" category to allow people with
   the "Student" role to see it again.
7. Send the message drafted earlier. Make sure to `@everyone`.

### Bot Commands
1. Erase archived channels from two quarters ago using `/erase`.
     a. `/erase 9A Mitchell [Archived]`
2. Archive channels from last quarter using `archive`.
     a. `/archive 9B Mitchell`
3. Remove existing `9A`, `9B`, etc. roles from server members using `/strip`
4. Create categories for new courses with `create`.
     a. `/create 9C Mitchell`

### Reaction Role Updates
The server's reaction roles are set up using [Carl-bot](https://carl.gg). To
update the reaction roles we use for course selection and section selection,
first log in to the Carl-bot website using your Discord account. Then, under
the "Reaction Roles" section (currently in the Utility part of the sidebar),
you will find the previous quarter's reaction roles.

1. Clear *all* reactions on the course selection message in `#course-selection`.
2. Check that all courses offered the current quarter have a configured role
   reaction (e.g., if `9A` and `9B` are being offered, these can be selected).
3. Remove role reactions for any courses not offered this quarter. Add a note at
   the bottom of the `#course-selection` channel saying which courses are *not*
   offered.
4. React with the appropriate reaction roles for the current courses to allow
   people to easily click on them. Please do so in the order that the message in
   the channel shows.
5. For each section being taught other than `PHY 9D`:
     - Remove existing reactions from the message.
     - Remove reaction roles set up in Carl-bot.
     - Edit (or remove and resend) the existing message in this section channel
       to show available sections this quarter (remember, we only care about
       individual professors, not individual professors' individual discussion
       sections).
     - Add reaction roles in Carl-bot for each section.
     - React with each reaction on the message, again in the order that the
       professors appear.
6. For `PHY 9D`, if it is being offered, make sure the global channels are
   working.
7. Try to make sure that everything is set up correctly — this doesn't take long
   to do, and it's much better than students being unable to select the correct
   roles. Just pretend you're a student in each section and make sure the
   correct roles are assigned when you click on the reactions.


# Functionalities
## Commands for server transition between quarters
* `/erase some existing channel category`: Erases channel category.
  Deletes the role associated with the category.
    * Note: the category must end with `[ARCHIVED]`.
* `/archive some existing channel category`: Moves category to bottom of list and
  appends [ARCHIVED] to its name, enabling it to be deleted later.
  Deletes the role associated with the category.
    * Note: the category must start with `9` or `PHY`, and it must not
      contain the string `GLOBAL`.
* `/strip`: Strips roles `9A`, `9B`, `9C`, `9D`, and `9H` from everyone.
* `/create some new channel category`: Creates a custom category and a matching
  custom role, and limits the category to be visible only to that role.


## Technologies used
- [discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
- [discord.ext.commands](https://discordpy.readthedocs.io/en/latest/ext/commands/index.html)
- [Discord API](https://discord.com/developers/docs/intro)


## Usage
To get started, get a bot token and create an `env.py`:
```py
TOKEN = 'your-discord-bot-token-here'
PREFIX = ','
DEBUG_ID = '123456789'
```

Install discordpy if necessary (`python3 -m pip install discord`).

The owner of the bot can sync commands by @ing the bot with command `dev-sync` 
or `global-sync`.

Note: Nothing, not even granting every single other permission, was enough for
the bot to function without admin permissions.

Add our instance
[here](https://discord.com/api/oauth2/authorize?client_id=724415454604689421&permissions=8&scope=bot).


## License
Released under [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html). 
