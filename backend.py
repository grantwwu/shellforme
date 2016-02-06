

# Black       0;30     
# Gray        1;30
# Blue        0;34 
# Green       0;32 
# Cyan        0;36 
# Red         0;31 
# Purple      0;35 
# Brown       0;33     
# Yellow      1;33  
# White       1;37




# color='\033[{0};{1}m{2}\033[00m '
 # "\e[38;5;${i}m#\e[0m"

def bash_script(L):
  bashCmd = {"username":"\\u ", "hostname":"\\h ",
             "fqdn":"\\H ", "path":"\\w ", "pwd":"\\W ",
             "date":"\\d ", "24h":"\\A ", "12h":"\\@ ", 
             "24hs":"\\t ", "newline":"\n ", "history":"\\! ",
             "@":"@ ", ":":": ", ">":"> "}

  #colors for exit codes
  exitColors = {"red":"1", "green":"2", "yellow":"3",
                "blue":"4", "purple":"5", "cyan":"6",
                "white":"7"}

  src = ""
  for op in L:
    op_type = op["type"]
    if not op_type in bashCmd:
      if (op_type == "exit"):
        t_args, f_args = op["args"]
        
      else:
        raise Exception("This is not a valid command yet")
    

    else:
      cmd = bashCmd[op_type]

      if op["color"] != "none":
        c = exitColors[op["color"]]
        print(c)
        # cmd = "\\033[{0};{1}m{2}\\e[0m ".format(c1, c2, cmd)
        cmd = "$(tput setaf {0}) {1} $(tput sgr0)".format(c, cmd)

    src += cmd

  return src

#export PS1='\u \033[0;35m: \033[00m \W \033[0;35m: \e[00m '
#export PS1="\u $(tput setaf 2) : $(tput sgr0) \W $(tput setaf 2) : $(tput sgr0)"



# function success
# {
#     if [[ $? == 0 ]]; then
#         echo $(tput setaf 2)':)'
#     else
#         echo $(tput setaf 1)'D:'
#     fi
# }

# export PS1='\u@\h: \W $(success) $(tput sgr0)>'




def zsh_script(L):
  return



def json_to_script(D):
  if D["shell"] == "zsh":
    return zsh_script(D["options"]) #passes in list options
  else:
    return bash_script(D["options"])






