

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
  bashColors = {"black":"0", "red":"1", "green":"2",
                "yellow":"3", "blue":"4", "purple":"5",
                "cyan":"6", "white":"7", "grey":"8"}

  src = ""
  for op in L:
    op_type = op["type"]
    if not op_type in bashCmd:
      #exit condition
      if (op_type == "exit"):
        t_args, f_args = op["args"]
        t_color, f_color = bashColors[t_args["color"]], bashColors[f_args["color"]]
        if not (t_args["type"] in bashCmd and f_args["type"] in bashCmd):
          raise Exception("Use a valid command for both args")
        else:
          t_type, f_type = bashCmd[t_args["type"]], bashCmd[f_args["type"]]
        fun = """
function exit
{{
if [[ $? == 0 ]]; then
    echo $(tput setaf {0})'{1}'
else
    echo $(tput setaf {2})'{3}'
fi
}}\n\n""".format(t_color, t_type, f_color, f_type)

        cmd = "$(exit) "
        src = fun + src

      else:
        raise Exception("{0} is not a valid command yet".format(op_type))
    

    else:
      cmd = bashCmd[op_type]

      if op["color"] != "none":
        c = bashColors[op["color"]]
        cmd = "$(tput setaf {0}) {1} $(tput sgr0)".format(c, cmd)

    src += cmd

  #need to wrap export PS1='......' around the last line
  return src

def zsh_script(L):
  return



def json_to_script(D):
  if D["shell"] == "zsh":
    return zsh_script(D["options"]) #passes in list options
  else:
    return bash_script(D["options"])






