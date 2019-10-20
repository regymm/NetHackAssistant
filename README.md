# NetHackAssistant
A simple nethack Save/Load automation script(cheater)

I know it's cheating, but you are not able to beat nethack even with those cheating tools, are you?

### Usage

Run the python script as normal user, and enter commands to operate.
You may want to follow the following playing procedure: 

0. Run the script, and see the prompt nha>;

1. `R` to run the nethack game; 

(played for a while, want to save the progress, `Sy` in game to quit)

2. `s` to save the game progress, enter a description if you want to;

3. `R` to continue the game;

(died, quit game, back to prompt)

4. `ls` to list all save files;

5. `a` to apply(load) a saved game, enter the number ID shown in results of `ls`;

6. goto 1. 

Read the script itself for detailed help.

```
#Script cmds
q -- quit
l -- clear screen
h -- show this help msg

#Save Repo Cmds
ll -- list save repos
u -- use a save repo
n -- new save repo
x -- delete a save repo

#Save Cmds(to current save repo)
ls -- list saves
d -- delete a save
s -- save from game(now from /var/games/nethack)
a -- apply a change from saves to game[old save backuped, old backup overwriten]
e -- edit a save description

#Dir Cmds
b -- back up whole game save dir(/var/games/nethack)
tg -- tree game save root /var/games/nethack(tree should be installed)
ts -- tree save dir ~/.nha(tree should be installed)
dd -- delete dir ~/.nha, which includes all saves(rm -rf ~/.nha)[W:rm -rf!!!]

#Game Cmds
S -- show high score(nethack -s -v)
R -- run game(nethack)
X -- run game in discover mode(nethack -X)
D -- run game in wizard(debug) mode, root required
T -- trash current save(trash should be installed)
```

Most error messages shown actually doesn't matter. 
