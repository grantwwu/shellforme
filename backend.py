

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
  bashColors = {"black":("0","30"), "gray":("1","30"),
              "blue":("0","34"), "green":("0","32"),
              "cyan":("0","36"), "red":("0","31"),
              "purple":("0","35"), "brown":("0","33"),
              "yellow":("1","33"), "white":("1","37")}
  bashCmd = {"username":"\\u ", "hostname":"\\h ",
             "fqdn":"\\H ", "path":"\\w ", "pwd":"\\W ",
             "date":"\\d ", "24h":"\\A ", "12h":"\\@ ", 
             "24hs":"\\t ", "newline":"\n ", "history":"\\! ",
             "@":"@ ", ":":": ", ">":"> ", "~":"~ "}
  src = ""
  for op in L:
    op_type = op["type"]
    if not op_type in bashCmd:
        raise Exception("This is not a valid command yet")

    cmd = bashCmd[op_type]

    if op["color"] != "none":
      c1, c2 = bashColors[op["color"]]
      cmd = "\\033[{0};{1}m{2}\\e[0m ".format(c1, c2, cmd)

    print("cmd", cmd)
    src += cmd

  return src



def zsh_script(L):
  return



def json_to_script(D):
  if D["shell"] == "zsh":
    return zsh_script(D["options"]) #passes in list options
  else:
    return bash_script(D["options"])






