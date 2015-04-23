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
