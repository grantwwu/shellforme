;
function dummy(){
  return undefined;
};
function returntext(t){
  return function(){
    return t;
  }
};
function getdate() {
  return (new Date()).toISOString().substring(0, 10);
};
function gettime() {
  if (self.state==="24h") {
    return "24:00";
  } else if (self.state === "24h_s") {
    return "24:00:00";
  } else if (self.state === "12h") {
    return "12:00am";
  } else { console.log("state is bad: " + self.state + "\n"); return undefined; }
};
function getret() {
  return $("exit_symbol").val();
};

var promptstate = {
  username: {enabled: true, color: "white", text: (returntext("username"))},
  hostname: {enabled: true, color: "white", text: (returntext("hostname"))},
  domain: {enabled: false, color: "white", text: (returntext("domain"))},
  path: {enabled: true, color: "white", state:"relative", text: (returntext("/path/to/pwd"))},
  date: {enabled: false, color: "white", text: getdate},
  time: {enabled: false, color: "white", state:"24h", text: gettime},
  newline: {enabled: false, color: "white", text: (returntext("\\n"))},
  retcode: {enabled: false, true_color: "green", false_color: "red", text: getret},
  space: {enabled: false, true_color: "green", false_color: "red", text: (returntext(" "))},
  gt: {enabled: false, true_color: "green", false_color: "red", text: (returntext(">"))},
  colon: {enabled: true, true_color: "green", false_color: "red", text: (returntext(":"))},
  at: {enabled: false, true_color: "green", false_color: "red", text: (returntext("@"))}
};

var ordered_prompt = [
  "username",
  "at",
  "hostname",
  "colon",
  "path",
];

var current_selected = "username";

function enabler(prop) {
  return function(e) {
    console.log("enabling " + prop);
    promptstate[prop].enabled = true;
    if (($.inArray(prop, ordered_prompt)) == -1) {
      ordered_prompt.push(prop);
      current_selected = prop;
    }
    console.log(promptstate);
    render(null);
  };
};

function disabler(prop) {
  return function(e) {
    console.log("disabling " + prop);
    promptstate[prop].enabled = false;
    console.log(promptstate);
    var idx = $.inArray(prop, ordered_prompt);
    if (idx != -1) {
      ordered_prompt.splice(idx, 1);
    }
    render(null);
  };
};

function statesetter(prop, val) {
  return function() {
    promptstate[prop].state = val;
    promptstate[prop].enabled = true;
    if (~($.inArray(prop, ordered_prompt))) {
      ordered_prompt.push(prop);
    }
    render(null);
  };
};

function previewselected(which) {
  current_selected = which;
};

function render(e) {
  var parent = $("#terminal-preview");
  parent.empty();
  console.log("I'm rendering!");
  console.log("ordered prompt is: " + ordered_prompt + "\n");
  for (idx in ordered_prompt) {
    var item = ordered_prompt[idx];
    console.log("item is: " + ordered_prompt[item] + "\n");
    if (promptstate[item].enabled) {
      parent.append('<div class="term-elem"'
        + 'onclick="previewselected(' + item + ')">' 
        + promptstate[item].text() + '</div>');
    }
  }
};

$(document).ready(function() {
  console.log("Hello i'm alive\n");
  $('#username_enabled').click(enabler("username"));
  $('#username_disabled').click(disabler("username"));
  $('#hostname_enabled').click(enabler("hostname"));
  $('#hostname_disabled').click(disabler("hostname"));
  $('#Domain_enabled').click(enabler("domain"));
  $('#Domain_disabled').click(disabler("domain"));
  $('#path_absolute').click(statesetter("path", "absolute"));
  $('#path_relative').click(statesetter("path", "relative"));
  $('#path_disabled').click(disabler("path"));
  $('#date_enabled').click(enabler("date"));
  $('#date_disabled').click(disabler("date"));
  $('#12h').click(statesetter("time", "12h"));
  $('#24h').click(statesetter("time", "24h"));
  $('#24h_s').click(statesetter("time", "24h_s"));
  $('#time_disabled').click(disabler("time"));
  $('#NL_enabled').click(enabler("newline"));
  $('#NL_disabled').click(disabler("newline"));
  $('#History_enabled').click(enabler("history"));
  $('#History_disabled').click(disabler("history"));

  $('#exit_enabled').click(enabler("retcode"));
  $('#exit_disabled').click(disabler("retcode"));
  $('#exit_symbol').change(function() {
    promptstate.retcode.chars = this.value;
  });
  $('#moveleft').click(function(){
    console.log("moving left");
    var idx = ordered_prompt.indexOf(current_selected);
    if (idx > 0) {
      var tmp = ordered_prompt[idx-1];
      ordered_prompt[idx-1] = ordered_prompt[idx];
      ordered_prompt[idx] = tmp;
      render(null);
    }
  });
  $('#moveright').click(function(){
    console.log("moving right")
    var idx = ordered_prompt.indexOf(current_selected);
    if (idx < ordered_prompt.length - 1) {
      var tmp = ordered_prompt[idx+1];
      ordered_prompt[idx+1] = ordered_prompt[idx];
      ordered_prompt[idx] = tmp;
      render(null);
    }
  });
  render(null);
});

