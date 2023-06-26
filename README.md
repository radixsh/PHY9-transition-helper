# Physics 9 transition helper 
This Discord bot was built for the UC Davis Physics 9 Discord server to automate
repetitive admin work done at the end of every quarter, such as archiving the
old channels that used to correspond with a particular professor's class.

# Server Transition Instructions
The main requirement for server transition is that we preserve the previous
quarter's channels in case of academic misconduct concerns, as anything arising
at the end of a quarter can take some time to process. This means that we
actually delete channels on a one quarter delay. For example, the transition
to Summer Session 1 2023 would involve deleting the (archived) Winter 2023
channels, archiving the Spring 2023 channels, and creating new channels for
the new term.

## Server Transition Checklist
This Checklist was last updated 24 June 2023.

1. Send a message in the announcements channel saying that we are currently in
the process of transitioning the server for the next quarter. This message
should contain a note that course specific channels and course selection might
be unavailable until this process is complete.
2. Edit the permissions for the "Sorting/Selection" category to remove the
"Student" role's access. This prevents people from randomly reacting as you
make the changes, which makes things a bit easier to keep track of and also
means you don't have to worry about leaving someone with an invalid role
configuration.
3. Perform the **Bot Commands** checklist below.
4. Perform the **Reaction Role Updates** checklist below.
5. Draft message saying the transition is complete. We basically have a
template for this, so just grab a previous message and update the term. Getting
another mod to do a quick proofread on this is a good idea, but they've certainly
been sent out without such luxuries at 3am before.
6. Update permissions for the "Sorting/Selection" category to allow people with
the "Student" role to see it again.
7. Send the message drafted earlier. Make sure to `@everyone`, we do 4 of these
a year the ping frequency is fine.

### Bot commands
1. Erase existing archived channels using `erase`, e.g. `,erase 9b mitchell [archived]`
2. Archive channels from the previous quarter using `archive`, e.g. `,archive 9C mitchell`
3. Remove existing `9A`, `9B`, etc. roles from server members using `,strip`
4. Create categories for new courses with `create`, e.g. `,create 9d mitchell`

### Reaction Role Updates
The server's reaction roles are set up using [Carl-bot](https://carl.gg). To
update the reaction roles we use for course selection and section selection,
first log in to the Carl-bot website using your discord account. Then, under
the "Reaction Roles" section (currently in the Utility part of the sidebar),
you will find the previous quarter's reaction roles.


1. Clear *all* reactions on the course selection message in `#course-selection`.
2. Check that all courses offered the current quarter have a configured role
reaction (namely, if `9A` and `9B` are being offered, these can be selected).
3. Remove role reactions for any courses not offered this quarter. Add a note
at the bottom of the `#course-selection` channel saying which courses are
*not* offered.
4. React with the appropriate reaction roles for the current courses to allow
people to easily click on them. Please do so in the order that the message
in the channel shows.
5. For each section being taught other than `PHY 9D`:
    1. Remove existing reactions from the message.
    2. Remove reaction roles set up in Carl-bot.
    3. Edit (or remove and resend) the existing message in this section channel
       to show available sections this quarter (remember, we only care about
       professor teaching, not discussion sections).
    4. Add reaction roles in Carl-bot for each section.
    5. React with each reaction on the message, again in the order that the
       professors appear.
6. For `PHY 9D`, if it is being offered, make sure the global channels work
appropriately.
7. Try to make sure that everything is set up correctly — this doesn't take long
to do, and is much better than students being unable to select the correct roles.
Just pretend you're a student in each section and make sure the correct roles
are assigned when you click on the reactions.

# Functionalities
## Commands for server transition between quarters
* `erase some existing channel category`: Erases channel category.
  Deletes the role associated with the category.
  * Note: the category must end with `[ARCHIVED]`.
* `archive some existing channel category`: Moves category to bottom of list and
  appends [ARCHIVED] to its name, enabling it to be deleted later.
  Deletes the role associated with the category.
  * Note: the category must start with `9` or `PHY`, and it must not
    contain the string `GLOBAL`.
* `create some new channel category`: Creates a custom category and a matching
  custom role, and limits the category to be visible only to that role.
* `strip`: Strips roles `9A`, `9B`, `9C`, `9D`, and `9H` from everyone.

## Other commands that may be useful
* `find some role`: Shows a list of people with the specified role.
* `duplicate some existing channel category`: Duplicates channel category
  and its channels and roles/permissions. To be used only when a certain
  professor is teaching the same class this quarter as last quarter.


## Technologies used
- [discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
- [discord.ext.commands](https://discordpy.readthedocs.io/en/latest/ext/commands/index.html)
- [Discord API](https://discord.com/developers/docs/intro)


## Usage
To get started, get a bot token and create an `env.py`:
```py
TOKEN = 'your-discord-bot-token-here'
PREFIX = ','
```

Install discordpy if necessary (`python3 -m pip install discord`) before running
`python3 index.py`.

Note: Nothing, not even granting every single other permission, was enough for
the bot to function without admin permissions.

Add my instance
[here](https://discord.com/api/oauth2/authorize?client_id=724415454604689421&permissions=8&scope=bot).


## License
Released under [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html). 
