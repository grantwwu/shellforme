shell_maps =\
    {
        "bash" :
        {
            "username" : r"\u",
            "hostname" : r"\h",
            "fqdn" : r"\H",
            "path" : r"\w",
            "pwd" : r"\W",
            "date" : r"\d",
            "24h" : r"\A",
            "12h" : r"\@",
            "24hs" : r"\t",
            "newline" : r"\n",
            "history" : r"\!",
            "@" : r"@",
            ":" : r":",
            ">" : r">",
            "~" : r"~"
        },
        "zsh" :
        {
            "username" : r"%n",
            "hostname" : r"%m",
            "fqdn" : r"%M",
            "path" : r"%~",
            "pwd" : r"%/",
            "date" : r"%D",
            "24h" : r"%T",
            "12h" : r"%@",
            "24hs" : r"%*",
            "newline" : r"\n",
            "history" : r"%!",
            "@" : r"@",
            ":" : r":",
            ">" : r">",
            "~" : r"~"
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
function shellforme_exit {{
    if [[ $? == 0 ]]; then
        printf "%s" "$(tput setaf {0}){1}"
    else
        printf "%s" "$(tput setaf {2}){3}"
    fi
    printf "%s" "$(tput sgr0)"
}}

"""
# Double {{ }} to escape python formatting!!!

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
                    true_color = color_map[true_color]
                    false_color = args["false_color"]
                    false_color = color_map[false_color]
                except KeyError:
                    raise Error("Exit element missing true/false string/color")
                escaped = r"\$(shellforme_exit)"
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
    prompt_string = "".join(e["escaped"] for e in last_ir)
    functions =\
        "".join(e["additional_function"] for e in last_ir
                if "additional_function" in e)

    ret =\
      "printf '%s\\n\\n%s' 'PS1=\"{0}\"' '{1}' >> ~/.{2}rc".format(prompt_string,
                                                              functions,
                                                              p["shell"])
    return { "status" : "success", "output" : ret }
