example1 = {
    "shell" : "bash",
    "color_scheme" : "default",
    "elements" :
        [
            {
                "type" : "username",
                "color" : "yellow",
                "static" : True
            },
            {
                "type" : "@",
                "color" : "yellow",
                "static" : True
            },
            {
                "type" : "hostname",
                "color" : "yellow",
                "static" : True
            },
            {
                "type" : ":",
                "color" : "yellow",
                "static" : True
            },
            {
                "type" : "exit",
                "static" : False,
                "optional_args":
                {
                    "true_string" : "G",
                    "false_string" : "B",
                    "true_color" : "green",
                    "false_color" : "red"
                }
            },
            {
                "type" : ":",
                "color" : "yellow",
                "static" : True
            },
            {
                "type" : "pwd",
                "color" : "yellow",
                "static" : True
            }
        ]
}
