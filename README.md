## Commands

### active 

```Shell
$ checkio-cli active
Mission: empire2
Interpreter: python_3

```

is showing currently active status. In this examples user is solving mission empire2 using python_3 interpreter

```Shell
$ checkio-cli active crystal-row
$ checkio-cli active
Mission: crystal-row
Interpreter: python_3

```

is changing active mission. Active mission will be change when you are usign mission slug in any other way, like `checkio-cli check crystal-row`

```Shell
$ checkio-cli active crystal-row python_2
$ checkio-cli active
Mission: crystal-row
Interpreter: python_2

```

is changing both, mission and envieroument

## get-git

download a new mission from git repository

```Shell
$ checkio-cli get-git https://github.com/Checkio-Game-Missions/checkio-empire-striped-words striped-words

```

1. checkout a mission into your _missions_folder_ . If folder for this mission is exist already user will be asked about remove this folder first
2. collect all sources in one folder from all parents
3. build a docker image if parameter --wihtout-container wasn't added
4. add a solution file for current interpreter in _solutions_folder_
5. Build a native envieroument for refery and checkio_cli interface
6. set this mission as a currently active

## run and check

both commands run and check have the same interface

```Shell
$ checkio-cli check striped-words
TEST: striped_words(My name is ...)
INCOMPLETE

```

checks mission striped-words using a solution from folder _solutions_folder_

```Shell
$ checkio-cli check
TEST: striped_words(My name is ...)
INCOMPLETE
```

checks a currently active mission.

```Shell
$ checkio-cli check --without-container
TEST: striped_words(My name is ...)
INCOMPLETE

```

check by using local envieroument for referee not a docker container. For simple mission it works faster and for mission creation process it is an easier way to debug a referee

## Config

```Shell
$ cat ~/.checkio_cli.yaml 
main_folder: /home/oduvan/checkio
missions_folder: /home/oduvan/www/checkio/mission-design/missions
solutions_folder: /home/oduvan/www/checkio/mission-design/solutions

```

main_folder - basic folder for all missions, compiled missions, prepared envierouments
missions_folder - where missions sources is stored
solutions_folder - where users solutions is stored

```Shell
$ cat ~/.active_checkio_cli.yaml 
interpreter: python_3
mission: null

```

user can get the same information by command _active_ and can change this file using the same command.
