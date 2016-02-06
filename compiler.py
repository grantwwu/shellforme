shell_maps =\
    {
        "bash" :
        {
            "username" : "\\u ",
            "hostname" : "\\h ",
            "fqdn" : "\\H ",
            "path" : "\\w ",
            "pwd" : "\\W ",
            "date" : "\\d ",
            "24h" : "\\A ",
            "12h" : "\\@ ",
            "24hs" : "\\t ",
            "newline" : "\n ",
            "history" : "\\! ",
            "@" : "@ ",
            ":" : ": ",
            ">" : "> ",
            "~" : "~ "
        },
        "zsh" :
        {

        }
    }

color_schemes =\
   {
       "default" :
       {
            "black" : "0",
            "red" : "1",
            "green" : "2",
            "yellow" : "3",
            "blue" : "4",
            "purple" : "5",
            "cyan" : "6",
            "white" : "7",
            "grey" : "8"
       }
   }

exit_string =\
"""
function shellforme_exit {
    if [[ $? == 0 ]]; then
        echo '$(tput setaf {0}){1}'
    else
        echo '$(tput setaf {2}){3}'
    fi
    echo '$(tput sgr0)'
}

"""

class Error(Exception):
    def __init__(self, msg):
        self.msg = msg
    def as_dict(self):
        return { "status" : "error", "message" : msg }

def compile(p):
    try:
        shell = p["shell"]
    except KeyError:
        raise Error("Shell not specified.")
    try:
        shell_map = shell_maps[shell]
    except KeyError:
        raise Error("Unknown shell: {0}".format(shell))
    try:
        color_scheme = p["color_scheme"]
    except KeyError:
        raise Error("Color scheme not specified.")
    try:
        color_map = color_schemes[color_scheme]
    except KeyError:
        raise Error("Unknown color scheme: {0}".format(color_scheme))

    def mapper(element):
        try:
            t = element["type"]
        except KeyError:
            raise Error("Element without type.")
        try:
            static = element["static"]
        except KeyError:
            raise Error("Element staticness unspecified.")
        if static:
            try:
                c = element["color"]
            except KeyError:
                raise Error("Static element has no color")
            try:
                cnum = color_map[c]
            except KeyError:
                raise Error("Unknown static element color: {0}".format(c))
            try:
                code = shell_map[t]
            except KeyError:
                raise Error("Unknown static element type: {0}".format(t))
            escaped =\
                "$(tput setaf {0}){1}$(tput sgr0)".format(cnum, code)
            return { "escaped" : escaped }
        else:
            try:
                args = element["optional_args"]
            except KeyError:
                raise Error("Dynamic element has no optional_args")
            if t == "exit":
                # Set a different colored string for true and false
                try:
                    true_string = args["true_string"]
                    false_string = args["false_string"]
                    true_color = args["true_color"]
                    false_color = args["false_color"]
                except KeyError:
                    raise Error("Exit element missing true/false string/color")
                escaped = "$(shellforme_exit)"
                fun = exit_string.format(true_color, true_string,
                                         false_color, false_string)
                return { "escaped" : escaped, "additional_function" : fun }
            elif t == "git":
                pass
                # TODO: Implement
            elif t == "chroot":
                pass
                # TODO: Implement
            else:
                raise Error("{0} is not a valid command yet".format(t))
    try:
        elements = p["elements"]
    except KeyError:
        raise Error("Elements not specified.")

    last_ir = [mapper(e) for e in elements]
    prompt_string = [e["escaped"] for e in last_ir]
    functions =\
        [e["additional_function"] for e in last_ir if "additional_function" in e]

    ret = "echo \"export PS1={0}\\n{1}\" >> ~/.{1}rc".format(prompt_string,
                                                             functions,
                                                             p["shell"])
    return { "status" : "success", "output" : ret }

